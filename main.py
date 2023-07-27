from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI()

# Replace this with your actual reCAPTCHA v3 secret key
RECAPTCHA_SECRET_KEY = "6Lfv4kwnAAAAAA9PQw7wNkyRo6o4BtP_mT6bj66Q"

@app.post("/verify-recaptcha")
async def verify_recaptcha(token: str = Form(...)):
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                      data = {'secret' : "6Lfv4kwnAAAAAA9PQw7wNkyRo6o4BtP_mT6bj66Q",
                              'response' :token})
        google_response = json.loads(r.text)
        return  google_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)
