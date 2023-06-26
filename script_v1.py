import os
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import base64
import time

credentials_file_path = "api.json"
video_file_path = "static/wideo.mkv"
spreadsheet_id = "1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI"

credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
video_service = build('videointelligence', 'v1', credentials=credentials)


# def transcribe_video(video_file_path):
#     with open(video_file_path, 'rb') as video_file:
#         input_content = base64.b64encode(video_file.read()).decode('utf-8')

#     features = ['SPEECH_TRANSCRIPTION']
#     language_code = 'pl-PL'  # Replace with your desired language code
#     operation = video_service.videos().annotate(body={
#         'inputContent': input_content,
#         'features': features,
#         'videoContext': {
#             'speechTranscriptionConfig': {
#                 'languageCode': language_code
#             }
#         }
#     }).execute()

#     operation_name = operation['name']

#     # Wait for the operation to complete
#     while True:
#         result = video_service.projects().locations().operations().get(name=operation_name).execute()
#         if 'done' in result and result['done']:
#             break
#         time.sleep(5)

#     # print(result)


#     annotation_results = result['response']['annotationResults'][0]

#     if 'speechTranscriptions' in annotation_results:
#         transcription_results = annotation_results['speechTranscriptions']
#     else:
#         transcription_results = []

#     # print('================')
#     # print(transcription_results)
#     # print('================')
#     return transcription_results




def send_to_spreadsheet(transcription_results):
    df = pd.DataFrame(columns=['Czas', 'Tekst'])

    for transcription in transcription_results:
        alternatives = transcription['alternatives']
        for alternative in alternatives:
            transcript = alternative['transcript']
            start_time = alternative['words'][0]['startTime']
            end_time = alternative['words'][-1]['endTime']
            # df = df.append({'Czas': f"{start_time} - {end_time}", 'Tekst': transcript}, ignore_index=True)
            # df = df.values.({'Czas': f"{start_time} - {end_time}", 'Tekst': transcript})
    
            new_row = {'Czas': f"{start_time} - {end_time}", 'Tekst': transcript}
            new_df = pd.DataFrame(new_row, index=[0])
            df = pd.concat([df, new_df], ignore_index=True)

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


# transcription_results = transcribe_video(video_file_path)
transcription_results = [
    {'alternatives': [{'transcript': 'to jest ten najdłuższy album tak też masz nie to nie zrobione spoko i ostatnia rzecz to jest to że tutaj mamy łączną długość i to jest',
                    'confidence': 0.9338637,
                    'words': [{'startTime': '0s', 'endTime': '0.700s', 'word': 'to'},
                                {'startTime': '0.700s', 'endTime': '0.900s', 'word': 'jest'},
                                {'startTime': '0.900s', 'endTime': '1.300s', 'word': 'ten'},
                                {'startTime': '1.300s', 'endTime': '1.600s', 'word': 'najdłuższy'},
                                {'startTime': '1.600s', 'endTime': '2.700s', 'word': 'album'},
                                {'startTime': '2.700s', 'endTime': '5.400s', 'word': 'tak'},
                                {'startTime': '5.400s', 'endTime': '7.200s', 'word': 'też'},
                                {'startTime': '7.200s', 'endTime': '7.500s', 'word': 'masz'},
                                {'startTime': '7.500s', 'endTime': '7.600s', 'word': 'nie'},
                                {'startTime': '7.600s', 'endTime': '7.700s', 'word': 'to'},
                                {'startTime': '7.700s', 'endTime': '7.900s', 'word': 'nie'},
                                {'startTime': '7.900s', 'endTime': '8.400s', 'word': 'zrobione'},
                                {'startTime': '8.400s', 'endTime': '8.800s', 'word': 'spoko'},
                                {'startTime': '8.800s', 'endTime': '9.700s', 'word': 'i'},
                                {'startTime': '9.700s', 'endTime': '10.300s', 'word': 'ostatnia'},
                                {'startTime': '10.300s', 'endTime': '10.700s', 'word': 'rzecz'},
                                {'startTime': '10.700s', 'endTime': '11s', 'word': 'to'},
                                {'startTime': '11s', 'endTime': '11.300s', 'word': 'jest'},
                                {'startTime': '11.300s', 'endTime': '11.600s', 'word': 'to'},
                                {'startTime': '11.600s', 'endTime': '11.900s', 'word': 'że'},
                                {'startTime': '11.900s', 'endTime': '12.500s', 'word': 'tutaj'},
                                {'startTime': '12.500s', 'endTime': '13.200s', 'word': 'mamy'},
                                {'startTime': '13.200s', 'endTime': '14.100s', 'word': 'łączną'},
                                {'startTime': '14.100s', 'endTime': '14.400s', 'word': 'długość'},
                                {'startTime': '14.400s', 'endTime': '15.200s', 'word': 'i'},
                                {'startTime': '15.200s', 'endTime': '15.900s', 'word': 'to'},
                                {'startTime': '15.900s', 'endTime': '16.800s', 'word': 'jest'}]}],
                                'languageCode': 'pl-pl'},
    {'alternatives': [{'transcript': ' też nie zrobią No dobra przyjdziesz generalnie czego nie zrobiłeś tak dobra jest tak jest spoko to teraz skoro masz u siebie ten kod to możemy spróbować podział Zobacz co tam tak naprawdę jest więc teraz ja przestaje udostępniać',
                    'confidence': 0.92278457,
                    'words': [{'startTime': '18.200s', 'endTime': '19.700s', 'word': 'też'},
                                {'startTime': '19.700s', 'endTime': '19.800s', 'word': 'nie'},
                                {'startTime': '19.800s', 'endTime': '20.100s', 'word': 'zrobią'},
                                {'startTime': '20.100s', 'endTime': '20.400s', 'word': 'No'},
                                {'startTime': '20.400s', 'endTime': '20.700s', 'word': 'dobra'},
                                {'startTime': '20.700s', 'endTime': '21.300s', 'word': 'przyjdziesz'},
                                {'startTime': '21.300s', 'endTime': '21.700s', 'word': 'generalnie'},
                                {'startTime': '21.700s', 'endTime': '21.900s', 'word': 'czego'},
                                {'startTime': '21.900s', 'endTime': '22s', 'word': 'nie'},
                                {'startTime': '22s', 'endTime': '22.300s', 'word': 'zrobiłeś'},
                                {'startTime': '22.300s', 'endTime': '22.600s', 'word': 'tak'},
                                {'startTime': '22.600s', 'endTime': '23s', 'word': 'dobra'},
                                {'startTime': '23s', 'endTime': '23.400s', 'word': 'jest'},
                                {'startTime': '23.400s', 'endTime': '23.700s', 'word': 'tak'},
                                {'startTime': '23.700s', 'endTime': '24s', 'word': 'jest'},
                                {'startTime': '24s', 'endTime': '26.300s', 'word': 'spoko'},
                                {'startTime': '26.300s', 'endTime': '26.600s', 'word': 'to'},
                                {'startTime': '26.600s', 'endTime': '26.900s', 'word': 'teraz'},
                                {'startTime': '26.900s', 'endTime': '27.100s', 'word': 'skoro'},
                                {'startTime': '27.100s', 'endTime': '27.400s', 'word': 'masz'},
                                {'startTime': '27.400s', 'endTime': '27.500s', 'word': 'u'},
                                {'startTime': '27.500s', 'endTime': '27.600s', 'word': 'siebie'},
                                {'startTime': '27.600s', 'endTime': '28s', 'word': 'ten'},
                                {'startTime': '28s', 'endTime': '28.300s', 'word': 'kod'},
                                {'startTime': '28.300s', 'endTime': '28.600s', 'word': 'to'},
                                {'startTime': '28.600s', 'endTime': '29s', 'word': 'możemy'},
                                {'startTime': '29s', 'endTime': '29.200s', 'word': 'spróbować'},
                                {'startTime': '29.200s', 'endTime': '30.100s', 'word': 'podział'},
                                {'startTime': '30.100s', 'endTime': '31.100s', 'word': 'Zobacz'},
                                {'startTime': '31.100s', 'endTime': '31.300s', 'word': 'co'},
                                {'startTime': '31.300s', 'endTime': '31.500s', 'word': 'tam'},
                                {'startTime': '31.500s', 'endTime': '31.700s', 'word': 'tak'},
                                {'startTime': '31.700s', 'endTime': '32.200s', 'word': 'naprawdę'},
                                {'startTime': '32.200s', 'endTime': '32.600s', 'word': 'jest'},
                                {'startTime': '32.600s', 'endTime': '33.600s', 'word': 'więc'},
                                {'startTime': '33.600s', 'endTime': '33.800s', 'word': 'teraz'},
                                {'startTime': '33.800s', 'endTime': '34s', 'word': 'ja'}, 
                                {'startTime': '34s', 'endTime': '34.400s', 'word': 'przestaje'},
                                {'startTime': '34.400s', 'endTime': '34.800s', 'word': 'udostępniać'}]}],
                                'languageCode': 'pl-pl'}]


send_to_spreadsheet(transcription_results)





# r_without_error={'name': 'projects/713923880291/locations/europe-west1/operations/6174833596140466263',
#                  'metadata': {'@type': 'type.googleapis.com/google.cloud.videointelligence.v1.AnnotateVideoProgress',
#                               'annotationProgress': [{'progressPercent': 100, 'startTime': '2023-06-26T20:39:26.620975Z', 'updateTime': '2023-06-26T20:39:48.598949Z'}]},
#                               'done': True,
#                               'response': {'@type': 'type.googleapis.com/google.cloud.videointelligence.v1.AnnotateVideoResponse',
#                                            'annotationResults': [{'segment': {'startTimeOffset': '0s', 'endTimeOffset': '34.986666s'},
#                                                                   'speechTranscriptions': [{'alternatives': [{'transcript': 'to jest ten najdłuższy album tak też masz nie to nie zrobione spoko i ostatnia rzecz to jest to że tutaj mamy łączną długość i to jest',
#                                                                                                               'confidence': 0.9338637,
#                                                                                                               'words': [{'startTime': '0s', 'endTime': '0.700s', 'word': 'to'},
#                                                                                                                         {'startTime': '0.700s', 'endTime': '0.900s', 'word': 'jest'},
#                                                                                                                         {'startTime': '0.900s', 'endTime': '1.300s', 'word': 'ten'},
#                                                                                                                         {'startTime': '1.300s', 'endTime': '1.600s', 'word': 'najdłuższy'},
#                                                                                                                         {'startTime': '1.600s', 'endTime': '2.700s', 'word': 'album'},
#                                                                                                                         {'startTime': '2.700s', 'endTime': '5.400s', 'word': 'tak'},
#                                                                                                                         {'startTime': '5.400s', 'endTime': '7.200s', 'word': 'też'},
#                                                                                                                         {'startTime': '7.200s', 'endTime': '7.500s', 'word': 'masz'},
#                                                                                                                         {'startTime': '7.500s', 'endTime': '7.600s', 'word': 'nie'},
#                                                                                                                         {'startTime': '7.600s', 'endTime': '7.700s', 'word': 'to'},
#                                                                                                                         {'startTime': '7.700s', 'endTime': '7.900s', 'word': 'nie'},
#                                                                                                                         {'startTime': '7.900s', 'endTime': '8.400s', 'word': 'zrobione'},
#                                                                                                                         {'startTime': '8.400s', 'endTime': '8.800s', 'word': 'spoko'},
#                                                                                                                         {'startTime': '8.800s', 'endTime': '9.700s', 'word': 'i'},
#                                                                                                                         {'startTime': '9.700s', 'endTime': '10.300s', 'word': 'ostatnia'},
#                                                                                                                         {'startTime': '10.300s', 'endTime': '10.700s', 'word': 'rzecz'},
#                                                                                                                         {'startTime': '10.700s', 'endTime': '11s', 'word': 'to'},
#                                                                                                                         {'startTime': '11s', 'endTime': '11.300s', 'word': 'jest'},
#                                                                                                                         {'startTime': '11.300s', 'endTime': '11.600s', 'word': 'to'},
#                                                                                                                         {'startTime': '11.600s', 'endTime': '11.900s', 'word': 'że'},
#                                                                                                                         {'startTime': '11.900s', 'endTime': '12.500s', 'word': 'tutaj'},
#                                                                                                                         {'startTime': '12.500s', 'endTime': '13.200s', 'word': 'mamy'},
#                                                                                                                         {'startTime': '13.200s', 'endTime': '14.100s', 'word': 'łączną'},
#                                                                                                                         {'startTime': '14.100s', 'endTime': '14.400s', 'word': 'długość'},
#                                                                                                                         {'startTime': '14.400s', 'endTime': '15.200s', 'word': 'i'},
#                                                                                                                         {'startTime': '15.200s', 'endTime': '15.900s', 'word': 'to'},
#                                                                                                                         {'startTime': '15.900s', 'endTime': '16.800s', 'word': 'jest'}]}],
#                                                                                                               'languageCode': 'pl-pl'},
#                                                                                                               {'alternatives': [{'transcript': ' też nie zrobią No dobra przyjdziesz generalnie czego nie zrobiłeś tak dobra jest tak jest spoko to teraz skoro masz u siebie ten kod to możemy spróbować podział Zobacz co tam tak naprawdę jest więc teraz ja przestaje udostępniać',
#                                                                                                                                  'confidence': 0.92278457,
#                                                                                                                                  'words': [{'startTime': '18.200s', 'endTime': '19.700s', 'word': 'też'},
#                                                                                                                                             {'startTime': '19.700s', 'endTime': '19.800s', 'word': 'nie'},
#                                                                                                                                             {'startTime': '19.800s', 'endTime': '20.100s', 'word': 'zrobią'},
#                                                                                                                                             {'startTime': '20.100s', 'endTime': '20.400s', 'word': 'No'},
#                                                                                                                                             {'startTime': '20.400s', 'endTime': '20.700s', 'word': 'dobra'},
#                                                                                                                                             {'startTime': '20.700s', 'endTime': '21.300s', 'word': 'przyjdziesz'},
#                                                                                                                                             {'startTime': '21.300s', 'endTime': '21.700s', 'word': 'generalnie'},
#                                                                                                                                             {'startTime': '21.700s', 'endTime': '21.900s', 'word': 'czego'},
#                                                                                                                                             {'startTime': '21.900s', 'endTime': '22s', 'word': 'nie'},
#                                                                                                                                             {'startTime': '22s', 'endTime': '22.300s', 'word': 'zrobiłeś'},
#                                                                                                                                             {'startTime': '22.300s', 'endTime': '22.600s', 'word': 'tak'},
#                                                                                                                                             {'startTime': '22.600s', 'endTime': '23s', 'word': 'dobra'},
#                                                                                                                                             {'startTime': '23s', 'endTime': '23.400s', 'word': 'jest'},
#                                                                                                                                             {'startTime': '23.400s', 'endTime': '23.700s', 'word': 'tak'},
#                                                                                                                                             {'startTime': '23.700s', 'endTime': '24s', 'word': 'jest'},
#                                                                                                                                             {'startTime': '24s', 'endTime': '26.300s', 'word': 'spoko'},
#                                                                                                                                             {'startTime': '26.300s', 'endTime': '26.600s', 'word': 'to'},
#                                                                                                                                             {'startTime': '26.600s', 'endTime': '26.900s', 'word': 'teraz'},
#                                                                                                                                             {'startTime': '26.900s', 'endTime': '27.100s', 'word': 'skoro'},
#                                                                                                                                             {'startTime': '27.100s', 'endTime': '27.400s', 'word': 'masz'},
#                                                                                                                                             {'startTime': '27.400s', 'endTime': '27.500s', 'word': 'u'},
#                                                                                                                                             {'startTime': '27.500s', 'endTime': '27.600s', 'word': 'siebie'},
#                                                                                                                                             {'startTime': '27.600s', 'endTime': '28s', 'word': 'ten'},
#                                                                                                                                             {'startTime': '28s', 'endTime': '28.300s', 'word': 'kod'},
#                                                                                                                                             {'startTime': '28.300s', 'endTime': '28.600s', 'word': 'to'},
#                                                                                                                                             {'startTime': '28.600s', 'endTime': '29s', 'word': 'możemy'},
#                                                                                                                                             {'startTime': '29s', 'endTime': '29.200s', 'word': 'spróbować'},
#                                                                                                                                             {'startTime': '29.200s', 'endTime': '30.100s', 'word': 'podział'},
#                                                                                                                                             {'startTime': '30.100s', 'endTime': '31.100s', 'word': 'Zobacz'},
#                                                                                                                                             {'startTime': '31.100s', 'endTime': '31.300s', 'word': 'co'},
#                                                                                                                                             {'startTime': '31.300s', 'endTime': '31.500s', 'word': 'tam'},
#                                                                                                                                             {'startTime': '31.500s', 'endTime': '31.700s', 'word': 'tak'},
#                                                                                                                                             {'startTime': '31.700s', 'endTime': '32.200s', 'word': 'naprawdę'},
#                                                                                                                                             {'startTime': '32.200s', 'endTime': '32.600s', 'word': 'jest'},
#                                                                                                                                             {'startTime': '32.600s', 'endTime': '33.600s', 'word': 'więc'},
#                                                                                                                                             {'startTime': '33.600s', 'endTime': '33.800s', 'word': 'teraz'},
#                                                                                                                                             {'startTime': '33.800s', 'endTime': '34s', 'word': 'ja'},
#                                                                                                                                             {'startTime': '34s', 'endTime': '34.400s', 'word': 'przestaje'},
#                                                                                                                                             {'startTime': '34.400s', 'endTime': '34.800s', 'word': 'udostępniać'}]}],
#                                                                                                                                             'languageCode': 'pl-pl'}]}]}}



    # r_with_error={
    #     'name': 'projects/713923880291/locations/europe-west1/operations/4464405670710480087',
    #     'metadata': {'@type': 'type.googleapis.com/google.cloud.videointelligence.v1.AnnotateVideoProgress',
    #                  'annotationProgress': [{'progressPercent': 100, 'startTime': '2023-06-26T20:15:17.723023Z', 'updateTime': '2023-06-26T20:15:32.270556Z'}]},
    #     'done': True,
    #     'response': {'@type': 'type.googleapis.com/google.cloud.videointelligence.v1.AnnotateVideoResponse',
    #                  'annotationResults': [{'error': {'code': 3, 'message': 'Invalid SpeechTranscription request argument(s).'},
    #                                         'segment': {'startTimeOffset': '0s', 'endTimeOffset': '34.986666s'}}]
    #                 }
    #             }