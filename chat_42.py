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

def get_top_endpoint(question):
    prompt = f"Given the question '{question}' and the list of endpoints: {endpoints}, return the single most valid endpoint, nothing else.\n\n"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.5,
    )

    response_text = completion.choices[0].message.content
    return response_text

def send_request_to_endpoint(question):
    endpoint = get_top_endpoint(question)
    base_url = "https://four2-campus-stats-backend.onrender.com"  # Replace this with your base API URL
    url = base_url + endpoint
    response = requests.get(url)

    if response.status_code == 200:
        answer = answer_question_based_on_data(question, endpoint, response.text)
        return answer
    else:
        return f"Error: Failed to get data from the endpoint '{endpoint}'"

def answer_question_based_on_data(question,endpoint,data):
    prompt = f"Based on the {data} from the '{endpoint}, determine wether there is answer to this {question}. If there is an answer, answer the question with appropriate answer, else say 'Sorry, based on the data from the {endpoint}, there is no relevant answer to your question.\n\n"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.5,
    )

    response = completion
    return response