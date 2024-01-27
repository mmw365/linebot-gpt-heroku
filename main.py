import os
import time
import json
import requests
from openai import OpenAI
from fastapi import FastAPI, Request

access_token = os.environ.get("LINE_ACCESS_TOKEN")
system_message = "あなたは100文字程度で分かりやすく答えてくれます。"

def send_json_with_auth_token(url, data, auth_token):
    json_data = json.dumps(data)
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def send_reply_message(reply_token, response_text):
    message = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": response_text}]
    }
    send_json_with_auth_token("https://api.line.me/v2/bot/message/reply", message, access_token)

def send_chatgpt(message):
    client = OpenAI()
    response = client.chat.completions.create(
        messages=message,
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content

def make_request_message(input_text, filename):
    message = [{"role": "system", "content": system_message}]
    if os.path.exists(filename):
        with open(filename, "r") as f:
            role = "user"
            for line in f:
                message.append({"role": "user", "content": line.replace("\\n", "\n")})
                role = "assistant" if role == "user" else "assistant"
    message.append({"role": "user", "content": input_text})
    return message

def delete_old_file(filename):
    if os.path.exists(filename):
        current_time = time.time()
        last_modified_time = os.path.getmtime(filename)
        if current_time - last_modified_time > 300:
            os.remove(filename)
        
def save_talk(filename, text, response_text):
    with open(filename, "a") as f:
        f.write(text.replace("\n","\\n") + "\n")
        f.write(response_text.replace("\n","\\n") + "\n")

app = FastAPI()

@app.post("/")
async def root(request: Request):
    input_msg = await request.json()
    event = input_msg["events"][0]

    if event["type"] != "message" or event["message"]["type"] != "text":
        return {}

    reply_token = event["replyToken"]
    text = event["message"]["text"]
    user_id = event["source"]["userId"]
    filename = user_id + ".txt"
    delete_old_file(filename)
    message = make_request_message(text, filename)
    response_text = send_chatgpt(message)
    save_talk(filename, text, response_text)
              
    send_reply_message(reply_token, response_text)

    return {}