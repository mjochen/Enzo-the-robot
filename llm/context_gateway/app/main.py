from fastapi import FastAPI
import requests
import json
from pathlib import Path
import os

app = FastAPI()

CONTEXT_DIR = Path(os.getenv("CONTEXT_DIR", "../context"))
# LLM_URL = "http://llm:11434/api/generate"
LLM_URL = os.getenv("LLM_URL", "http://127.0.0.1:11434/api/generate")
MODEL =  os.getenv("MODEL", "gemma2:2b")


@app.get("/")
@app.get("/hello")
def hello():
    return {"message": "Yes, I'm on."}

@app.get("/test_read")
def hello():
    ct = load_context()
    return {"message": ct}

@app.get("/test_llm")
def ask_llm():
    # print("am here!")
    prompt = "Who's living here?"

    response = requests.post(
        LLM_URL,
        json={
            "model": MODEL,
            "prompt": build_prompt(prompt),
            "stream": False
        }
    )

    return response.json()

def load_context():
    print("hello!")
    print(CONTEXT_DIR)
    context = ""
    # with open("../context/robot.txt") as f:
    #     context += "".join(f.readlines())

    for file in CONTEXT_DIR.glob("*.txt"):
        print(file)
        with open(file) as f:
            context += "".join(f.readlines()) + "\n"
    return context


def build_prompt(user_prompt):
    context = load_context()

    system = f"""
You have the following information:

{load_context()}

Use this information when answering.
"""

    return system + "\nUser question:\n" + user_prompt


# @app.post("/ask")
# def ask_llm(data: dict):

#     prompt = build_prompt(data["question"])

#     response = requests.post(
#         LLM_URL,
#         json={
#             "model": MODEL,
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     return response.json()