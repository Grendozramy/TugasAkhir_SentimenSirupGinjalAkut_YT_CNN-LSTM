import requests
import json
import pandas as pd

def analyze_sentiment(api_key, text_to_analyze):
    url = "https://api.prosa.ai/v2/text/doc-sentiment"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    data = {
        "text": text_to_analyze
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        sentiment_data = response.json()
        return sentiment_data["sentiment"][0]["sentiment"]
    elif response.status_code == 500:
        return "skipped"
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


api_key = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5XSTBNemRsTXprdE5tSmtNaTAwTTJZMkxXSTNaamN0T1dVMU5URmxObVF4Wm1KaSIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9pZCI6MTQ1ODEzLCJsaWNlbnNlX2tleSI6IjdiOWI5ZjU3LWVhN2ItNDQ5Zi05N2Y0LTBiNjQ1NmQwMjY3MSIsInVuaXF1ZV9rZXkiOiJiYmY1NGZmMi0yNTEzLTQ2YjQtOWJiNy04YTVlZmFhODMxYTMiLCJwcm9kdWN0X2lkIjoxNCwiYXVkIjoiYXBpLXNlcnZpY2UiLCJzdWIiOiIyMGEyMThiZC00ZWYyLTQxZjEtYTFiNi00ZTNjMzNiYWEzMzYiLCJpc3MiOiJjb25zb2xlIiwiaWF0IjoxNjgwNTc1Nzk3fQ.SlwU6jPGHM7t2yYixkL-84FiWxmi9-b6w_ubAXObrSYmjv4zt-QPp4uu2ZXZwm6OESHuUB1yPvcid0KAPuirY9GClYCWgitjxa0B5uxGDUgWbAbjlRRi8iZU_oqw8NrEK0h_oiqiTxmXXtslXUDBHiXgqtdJ0Pw_cAXrM-7xB1kd268_gxbHDhWfZ6i64JHCU-CjqeBhcreeGktRhjlDUtyZktfDE7bxaWrGuzeGITR59Wyf0Uqz5xs1daNngVSqOsZ4pJm7_aZTV4ZXhp4VZJ6iMkyvgVsDu_eghV0LWtfN2zRdyEiGDpUT1AlSK4IdG505fQGve2CsQ0SyWu20fA'

dataset = pd.read_csv('../../Data/2. Clean/clean.csv')

# Analyze the sentiment of each row in the 'text_normalized' column
sentiments = []
skipped_indices = []
for index, text_normalized in enumerate(dataset['text_manual_replaced']):
    sentiment_value = analyze_sentiment(api_key, text_normalized)
    if sentiment_value == "skipped":
        skipped_indices.append(index)
    sentiments.append(sentiment_value)

# Print the skipped indices
print(f"Skipped indices due to 500 error: {skipped_indices}")

# Add the sentiments to the dataset
dataset['label'] = sentiments

# Save the dataset to a new CSV file with the sentiment analysis results
dataset.to_csv('../../Data/3. labeling/labeling-prosa1.csv', index=False)
