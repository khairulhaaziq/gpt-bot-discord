import requests
import openai
import os
import json
import re

openai.api_key = os.getenv("OPENAI_KEY")

endpoints = [
    "/api/on-campus/active-users", "/api/on-campus/active-user-projects",
    "/api/on-campus/average-user-level", "/api/on-campus/average-session-hours",
    "/api/most-recent-submission", "/api/on-campus/cadet-pisciner-ratio",
    "/api/on-campus/active-user-skills",
    "/api/on-campus/daily-total-active-students",
    "/api/on-campus/weekly-cadet-xp", "/api/weekly-most-active-users",
    "/api/weekly-most-gained-xp"
]

endpoints_str = json.dumps(endpoints)


async def get_top_endpoint(question):
    prompt = f"Given the question '{question}' and the list of endpoints: {endpoints_str}, return the single most valid endpoint, E.g.: Question: list most recent submissions./api/most-recent-submission .\n\n"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        max_tokens=100,
        temperature=0.5,
    )

    response_text = completion.choices[0].message.content
    return parse_response(response_text)


def parse_response(response):
    pattern = r'\/[^\s"\'\\]*'
    match = re.search(pattern, response)

    if match:
        return match.group()
    else:
        return ""


def send_request_to_endpoint(endpoint):
    base_url = "https://four2-campus-stats-backend.onrender.com"
    url = base_url + endpoint
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Failed to get data from the endpoint '{endpoint}'"


def get_answer_from_data(question, data, endpoint):
    data_str = json.dumps(data)
    print(data_str)
    prompt = f"Based on the data:{data_str}, gotten from the endpoint:{endpoint}. Determine wether there is an answer for this question: {question}. If there is any, answer the question appropriately. Else, answer: I don't know. Based on the data from the endpoint {endpoint}, there is no relevant answer. Some context on the data: login is the usernames, they are the most important part of the data.\n\n"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
    )

    completion = completion.choices[0].message.content
    return completion
