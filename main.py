import cv2
from ultralytics import YOLO
import requests
import time
from tkinter import Tk, filedialog
import os

# 📁 1. Datei-Dialog öffnen
def select_video_file():
    root = Tk()
    root.withdraw()  # Versteckt das Hauptfenster
    file_path = filedialog.askopenfilename(
        title="Wähle ein Video aus",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
    )
    return file_path

VIDEO_PATH = select_video_file()

if not VIDEO_PATH or not os.path.exists(VIDEO_PATH):
    print("[ERROR] Kein gültiges Video ausgewählt. Skript wird beendet.")
    exit()

print(f"[INFO] Verwendetes Video: {VIDEO_PATH}")

# 📦 2. Konfiguration
YOLO_MODEL = 'yolov8n.pt'  # YOLOv8 Modell
# Mistral API Konfiguration
OLLAMA_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'mistral-custom'

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps * 1)  # Alle 1 Sekunde ein Frame

model = YOLO(r"C:\Users\dasgo\Projects\.venv\yolov8n.pt")  # YOLOv8 Modell laden
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_interval == 0:
        results = model.predict(frame)
        for result in results:
            for box in result.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = box
                if score > 0.5:
                    label = model.names[int(class_id)]
                    
                    # Filter für Schilder – passe das bei Bedarf an
                    print(f"[DEBUG] Erkanntes Label: {label}")
                    if True:  # Zum Test alle Objekte an Mistral schicken
                        # Mistral API Anfrage
                        print(f"[INFO] Erkanntes Schild: {label}")
                    
                        prompt = f"Erkläre das Verkehrsschild '{label}' in einfacher Sprache. Welche Konsequenzen hat ein Verstoß?"
                        response = requests.post(
                            OLLAMA_URL,
                            json={"model": OLLAMA_MODEL, "prompt": prompt}
                        )
                        antwort = response.json().get("response", "Keine Antwort von Mistral.")
                        print(f"[Mistral]: {antwort}\n")

    frame_count += 1

cap.release()
import pyttsx3

# Sprachengine initialisieren
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Geschwindigkeit (optional)

# In der Schleife, nach dem Mistral-Response:
antwort = response.json().get("response", "Keine Antwort von Mistral.")
print(f"[Mistral]: {antwort}\n")

# Sprachausgabe:
engine.say(antwort)
engine.runAndWait()
