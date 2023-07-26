from fastapi import FastAPI
from stravaio import strava_oauth2

app = FastAPI()

@app.get("/auth")
def strava_auth():
    authorization = strava_oauth2(client_id=110799, client_secret='8bac955bd9f61f2ce630f446dc594682afe3901a')
    return {"Authorization": authorization}
