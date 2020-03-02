from stravalib.client import Client
import datetime
from datetime import datetime
from sqlalchemy import delete
from lib.sqlalchemy_declarative import db_connect, apiTokens
import configparser
from dash_app import dash_app
import ast
import time

config = configparser.ConfigParser()
config.read('./config.ini')

client_id = config.get('strava', 'client_id')
client_secret = config.get('strava', 'client_secret')
redirect_uri = config.get('strava', 'redirect_uri')

# Retrieve current tokens from db
def current_token_dict():
    try:
        session, engine = db_connect()
        token_dict = session.query(apiTokens.tokens).filter(apiTokens.service == 'Strava').first()
        token_dict = ast.literal_eval(token_dict[0]) if token_dict else {}
        engine.dispose()
        session.close()
    except BaseException as e:
        dash_app.server.logger.error(e)
        token_dict = {}
    return token_dict


# Function for auto saving strava token_dict to db
def save_strava_token(token_dict):
    session, engine = db_connect()
    # Delete current key
    dash_app.server.logger.debug('Deleting current strava tokens')
    session.execute(delete(apiTokens).where(apiTokens.service == 'Strava'))
    # Insert new key
    dash_app.server.logger.debug('Inserting new strava tokens')
    session.add(apiTokens(date_utc=datetime.utcnow(), service='Strava', tokens=str(token_dict)))
    session.commit()
    engine.dispose()
    session.close()


def get_strava_client():
    token_dict = current_token_dict()
    if token_dict:
        client = Client()
        client.access_token = token_dict['access_token']
        client.refresh_token = token_dict['refresh_token']
        # If token is old, refresh it
        if time.time() > token_dict['expires_at']:
            dash_app.server.logger.debug('Strava tokens expired, refreshing...')
            refresh_response = client.refresh_access_token(client_id=client_id, client_secret=client_secret,
                                                           refresh_token=client.refresh_token)
            # Save to db
            save_strava_token(refresh_response)
            # Update client
            client.access_token = refresh_response['access_token']
            client.refresh_token = refresh_response['refresh_token']
    else:
        client = Client()

    return client


# Refreshes tokens with refresh token if available in db
def strava_connected():
    try:
        client = get_strava_client()
        test = client.get_athlete()
        dash_app.server.logger.debug('Strava connected')
        return True
    except BaseException as e:
        dash_app.server.logger.error('Strava not connected')
        dash_app.server.logger.error(e)
        return False


## Provide link for button on settings page
def connect_strava_link(auth_client):
    url = auth_client.authorization_url(client_id=client_id, redirect_uri=redirect_uri,
                                        scope=['read', 'read_all', 'profile:read_all', 'profile:write', 'activity:read',
                                               'activity:read_all', 'activity:write'])
    return url


# def check_data_insert():
# If data found in db later than data that is being insert, delete all data after earliest date being insert

# NOTE: Strava removes stopped periods in calculations, TrainingPeaks and Garmin Connect does not. Leaving non-moving periods in calculations
# https://github.com/mtraver/python-fitanalysis


# TODO: Look into ways to auto import LTHR similar to oura rest heart rate
# TODO: Auto delete db entires if importing earlier data and re enter later data


# def test_strava():
#     # Parsing for Strava_Samples
#     client = get_strava_client()
#     streams = GetStreams(client, 3110471562, types)
#     df_samples = pd.DataFrame()
#
#     # # Write each row to a dataframe
#     for item in types:
#         if item in streams.keys():
#             df_samples[item] = pd.Series(streams[item].data, index=None)
#
#     df_samples.to_csv('test_samples.csv')
#
# # Testing Summary
# activities = GetActivities(client, '2019-09-20T00:00:00Z', limit)
# for act in activities:
#     ParseActivitySummary(get_strava_client(), act).to_csv('df.csv',sep=',')
