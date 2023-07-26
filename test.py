from stravaio import strava_oauth2, StravaIO


# Create a stravaio client object and authenticate
authorization = strava_oauth2(client_id=110799, client_secret='8bac955bd9f61f2ce630f446dc594682afe3901a')
print(authorization)

client = StravaIO(access_token=authorization["access_token"])
"""
athlete = client.get_logged_in_athlete()
athlete_dict = athlete.to_dict()
print(athlete_dict)
"""
list_activities = client.get_logged_in_athlete_activities()
for a in list_activities:
    print(a, "\n")

