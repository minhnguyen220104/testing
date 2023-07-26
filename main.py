from fastapi import FastAPI
from stravaio import StravaIO

app = FastAPI()

@app.get("/activities")
def strava_activities():
    client = StravaIO(access_token='07691bb1188eca9c01ccdb69f8b1f36a0d596a57')
    list_activities = client.get_logged_in_athlete_activities()
    return {"Activities": list_activities}
