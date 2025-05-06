import openai

openai.api_key = "your_api_key_here"  # Ersetzen Sie dies durch Ihren tatsächlichen API-Schlüssel
openai.api_base = "https://api.openai.com/v1"  # Basis-URL für die OpenAI-API
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": "Wie lautet die Hauptstadt von Frankreich?"}
        ]
    )
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ Ein Fehler ist aufgetreten:", e)
