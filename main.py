from fastapi import FastAPI, HTTPException
from test import strava_oauth2
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.post("/strava")
def authorize():
    try:
        authorization = strava_oauth2(client_id=110799, client_secret='8bac955bd9f61f2ce630f446dc594682afe3901a')
        return  authorization
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
