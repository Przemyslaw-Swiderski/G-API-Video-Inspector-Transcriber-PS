import os
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account


video_file_path = "ścieżka/do/pliku/wideo.mp4"


credentials_file_path = "api.json"


spreadsheet_id = "1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI"


credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
video_service = build('videointelligence', 'v1', credentials=credentials)


def transcribe_video(video_file_path):
    with open(video_file_path, 'rb') as video_file:
        input_content = video_file.read()

    features = ['SPEECH_TRANSCRIPTION']
    operation = video_service.videos().annotate(body={
        'inputContent': input_content,
        'features': features,
    }).execute()

    operation_name = operation['name']


    result = video_service.operations().get(name=operation_name).execute()
    transcription_results = result['annotationResults'][0]['speechTranscriptions']

    return transcription_results


def send_to_spreadsheet(transcription_results):
    df = pd.DataFrame(columns=['Czas', 'Tekst'])

    for transcription in transcription_results:
        alternatives = transcription['alternatives']
        for alternative in alternatives:
            transcript = alternative['transcript']
            start_time = alternative['words'][0]['startTime']
            end_time = alternative['words'][-1]['endTime']

            df = df.append({'Czas': f"{start_time} - {end_time}", 'Tekst': transcript}, ignore_index=True)

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range='A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=dict(
            majorDimension='ROWS',
            values=df.values.tolist()
        )
    ).execute()


transcription_results = transcribe_video(video_file_path)
send_to_spreadsheet(transcription_results)