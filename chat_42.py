import requests
import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")

endpoints = [
    "/api/on-campus/active-users",
    "/api/on-campus/active-user-projects",
    "/api/on-campus/average-user-level",
    "/api/on-campus/average-session-hours",
    "/api/most-recent-submission",
    "/api/on-campus/cadet-pisciner-ratio",
    "/api/on-campus/active-user-skills",
    "/api/on-campus/daily-total-active-students",
    "/api/on-campus/weekly-cadet-xp",
    "/api/weekly-most-active-users",
    "/api/weekly-most-gained-xp"
]

def get_endpoint_scores(question):
    prompt = f"Given the question '{question}' and the list of endpoints: {endpoints}, return the single most valid endpoint, nothing else.\n\n"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.5,
    )

    response_text = completion.choices[0].message.content
    scores = [int(line.split(':')[-1].strip()) for line in response_text.split('\n')]
    return scores

def get_best_endpoint(question):
    scores = get_endpoint_scores(question)
    best_index = scores.index(max(scores))
    return endpoints[best_index]

def send_request_to_endpoint(endpoint):
    base_url = "https://example.com"  # Replace this with your base API URL
    url = base_url + endpoint
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Failed to get data from the endpoint '{endpoint}'"