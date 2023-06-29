import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import time
import gavt_utilities

os.system('cls')
print('Transcriber started to work. Please wait.')


try:
    credentials_file_path = gavt_utilities.get_credentials_file_path()
    video_file_path = gavt_utilities.get_video_file_path()
    google_spreadsheet_id = gavt_utilities.get_google_spreadsheet_id()
    language_code = gavt_utilities.get_language_code()

    if not credentials_file_path or not video_file_path or not google_spreadsheet_id or not language_code:
        gavt_utilities.no_required_information_message()

    credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
    video_service = build('videointelligence', 'v1', credentials=credentials)

    def transcribe_video(input_content, video_service):
        features = ['SPEECH_TRANSCRIPTION']

        operation = video_service.videos().annotate(body={
            'inputContent': input_content,
            'features': features,
            'videoContext': {
                'speechTranscriptionConfig': {
                    'languageCode': language_code
                }
            }
        }).execute()
        operation_name = operation['name']

        progress_bar = 'Transcriber started to work. Please wait.'
        # Wait for the operation to complete
        while True:
            result = video_service.projects().locations().operations().get(name=operation_name).execute()
            if 'done' in result and result['done']:
                break
            
            time.sleep(1)

            os.system('cls')
            progress_bar = progress_bar + '.'
            print(progress_bar)
        # ToDo timeout

        annotation_results = result['response']['annotationResults'][0]

        if 'speechTranscriptions' in annotation_results:
            transcription_results = annotation_results['speechTranscriptions']
        else:
            transcription_results = []

        return transcription_results


    def send_to_spreadsheet(transcription_results):
        df = pd.DataFrame(columns=['Czas', 'Tekst'])

        for transcription in transcription_results:
            alternatives = transcription['alternatives']
            for alternative in alternatives:
                transcript = alternative['transcript']
                start_time = alternative['words'][0]['startTime']
                end_time = alternative['words'][-1]['endTime']

                new_row = {'Czas': f'{start_time} - {end_time}', 'Tekst': transcript}
                new_df = pd.DataFrame(new_row, index=[0])
                df = pd.concat([df, new_df], ignore_index=True)


        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        sheet.values().append(
            spreadsheetId=google_spreadsheet_id,
            range='A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=dict(
                majorDimension='ROWS',
                values=df.values.tolist()
            )
        ).execute()

        os.system('cls')
        print('Transcriber finished it\'s work !')

    input_content = gavt_utilities.input_video_content(video_file_path)
    transcription_results = transcribe_video(input_content, video_service)
    send_to_spreadsheet(transcription_results)
    gavt_utilities.open_google_spreadsheet(google_spreadsheet_id)

except Exception as e:
    error_message = f"An unexpected error occurred: {str(e)}"
    gavt_utilities.display_error_message(error_message)
    print('Transcriber did not finish its work due to an unexpected error. You may fix the problem and try again.')
    exit()