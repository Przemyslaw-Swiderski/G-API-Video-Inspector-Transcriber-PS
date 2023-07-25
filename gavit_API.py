
from google.oauth2 import service_account
import os
from google.cloud import videointelligence
from googleapiclient.discovery import build
import tkinter as tk
from tkinter import filedialog, messagebox
import time
from flask import(
    Flask, jsonify, request, json)
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()


def transcription(video_link, language_code, spreadsheet_id, sheet_name, cell_address):

    print(video_link)
    print(language_code)
    print(spreadsheet_id)
    print(sheet_name)
    print(cell_address)

    # log1_data = {
    #     'video_link': video_link,
    #     'language_code': language_code,
    #     'spreadsheet_id': spreadsheet_id,
    #     'sheet_name': sheet_name,
    #     'cell_address': cell_address
    # }
    # output_file = "static/log1.json"
    # if os.path.exists(output_file):
    #     os.remove(output_file)
    # with open(output_file, 'w') as json_file:
    #     json.dump(log1_data, json_file, indent=4)

    credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH')
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
    # bucket_name = os.environ.get('YOUR_GOOGLE_CLOUD_STORAGE_BUCKET_NAME')

    input_content=''
    video_uri = video_link
    language_code = language_code
    google_spreadsheet_id = spreadsheet_id

    transcription_results = transcribe_video_API(input_content,
                                                video_uri,
                                                credentials,
                                                language_code,
                                                google_spreadsheet_id,
                                                sheet_name,
                                                cell_address,
                                                credentials_file_path
                                                )

    send_to_spreadsheet_API(transcription_results, google_spreadsheet_id, sheet_name, cell_address, credentials_file_path)



def transcribe_video_API(input_content: str,
                        video_uri: str,
                        credentials: object,
                        language_code: str,
                        google_spreadsheet_id: str,
                        sheet_name: str,
                        cell_address: str,
                        credentials_file_path: str
                        ) -> list:
    video_client = videointelligence.VideoIntelligenceServiceClient(credentials=credentials)
    features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]
    config = videointelligence.SpeechTranscriptionConfig(language_code=language_code, enable_automatic_punctuation=True)
    video_context = videointelligence.VideoContext(speech_transcription_config=config)

    if video_uri != '':
        request={
        "features": features,
        "input_uri": video_uri,
        "video_context": video_context,
        }
    if input_content != '':
        request={
        "features": features,
        'input_content': input_content,
        "video_context": video_context,
        }
    try:
        operation = video_client.annotate_video( request=request,)
        operation_name = operation.operation.name
    except Exception as e:
        e_message = str(e) + " in: \"operation = ...\" in def transcribe_video(input_content: str, credentials: object, language_code: str) -> list"
        exception_message_API(e_message)

    check_if_gc_is_ready_with_transcription_API(credentials,
                                                operation_name,
                                                google_spreadsheet_id,
                                                sheet_name,
                                                cell_address,
                                                credentials_file_path)

    try:
        result = operation.result()

    except Exception as e:
        e_message = str(e) + " in: \" result = ...\" in def transcribe_video(input_content: str, credentials: object, language_code: str) -> list"
        exception_message_API(e_message)

    annotation_results = result.annotation_results[0]
    print(annotation_results.speech_transcriptions)
    transcription_data = process_transcription_data_API(annotation_results)
    # if video_uri != '':
        # delete_file_from_cloud(video_uri, credentials)
    return transcription_data


def check_if_gc_is_ready_with_transcription_API(credentials: object,
                                                operation_name: str,
                                                google_spreadsheet_id: str,
                                                sheet_name: str,
                                                cell_address: str,
                                                credentials_file_path: str):
    
    video_service = build('videointelligence', 'v1', credentials=credentials)
    time_elapsed = 10
    while True:
        result = video_service.projects().locations().operations().get(name=operation_name).execute()
        if 'done' in result and result['done']:
            break
        time.sleep(5)
        os.system('cls')
        print(f'Transcription in progress. Please wait. Time elapsed: {str(time_elapsed)} seconds')
        short_message_for_user = "Time elapsed: " + str(time_elapsed) + "s. Transcription in progress, please wait..."
        send_short_message_to_spreadsheet_API(short_message_for_user,
                                            google_spreadsheet_id,
                                            sheet_name,
                                            cell_address,
                                            credentials_file_path)
        time_elapsed = time_elapsed + 5



def process_transcription_data_API(annotation_results):
    processed_transcription_data = []
    for speech_transcription in annotation_results.speech_transcriptions:
        for alternative in speech_transcription.alternatives:
            alternative_data = {
                "transcript": alternative.transcript,
                "confidence": alternative.confidence,
                "word_level_info": []
            }

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.seconds + word_info.start_time.microseconds * 1e-6
                end_time = word_info.end_time.seconds + word_info.end_time.microseconds * 1e-6

                word_info_data = {
                    "word": word,
                    "start_time": start_time,
                    "end_time": end_time
                }

                alternative_data["word_level_info"].append(word_info_data)
            processed_transcription_data.append(alternative_data)
    # output_file = "C:/Code/APIIntTool/static/result_temp_file.json"
    output_file = os.environ.get('TRANSCRIPTION_OUTPUT_FILE_PATH')
    if os.path.exists(output_file):
        os.remove(output_file)
    with open(output_file, 'w') as json_file:
        json.dump(processed_transcription_data, json_file, indent=4)
    return processed_transcription_data


def send_to_spreadsheet_API(transcription_results: list, google_spreadsheet_id: str, sheet_name: str, cell_address: str, credentials_file_path: str):
    try:
        cell_value = ""
        for i, transcription in enumerate(transcription_results, start=1):
            transcript = transcription['transcript']
            cell_value += f"{i}. {transcript}\n"

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file_path, scope)
        gc = gspread.authorize(credentials)

        # gc = gspread.authorize(credentials)

        # Open the specified spreadsheet by ID
        sh = gc.open_by_key(google_spreadsheet_id)

        # Select the specified sheet by name
        worksheet = sh.worksheet(sheet_name)

        # Clear the existing data from the specified cell
        worksheet.update(cell_address, '')

        # Write the concatenated transcriptions to the specified cell
        worksheet.update(cell_address, cell_value)

        os.system('cls')
        print('Transcriber finished its work!')
    except Exception as e:
        e_message = str(e) + " in: def send_to_spreadsheet(transcription_results: list, credentials: object, google_spreadsheet_id: str, sheet_name: str, cell_address: str)"
        exception_message_API(e_message)


def send_short_message_to_spreadsheet_API(short_message_for_user: str, google_spreadsheet_id: str, sheet_name: str, cell_address: str, credentials_file_path: str):
    try:

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file_path, scope)
        gc = gspread.authorize(credentials)

        # Open the specified spreadsheet by ID
        sh = gc.open_by_key(google_spreadsheet_id)

        # Select the specified sheet by name
        worksheet = sh.worksheet(sheet_name)

        # Clear the existing data from the specified cell
        worksheet.update(cell_address, '')

        cell_value = ""

        # Write the concatenated transcriptions to the specified cell
        worksheet.update(cell_address, short_message_for_user)

        # os.system('cls')
        # print('Transcriber finished its work!')
    except Exception as e:
        e_message = str(e) + " in: def send_to_spreadsheet(transcription_results: list, credentials: object, google_spreadsheet_id: str, sheet_name: str, cell_address: str)"
        exception_message_API(e_message)


def create_formatting_requests_to_spreadsheet_API():
    sheetId = 0
    formatting_requests = [
    {
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheetId,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': 1
            },
            'properties': {
                'pixelSize': 100
            },
            'fields': 'pixelSize'
        }
    },
    {
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheetId,
                'dimension': 'COLUMNS',
                'startIndex': 1,
                'endIndex': 2
            },
            'properties': {
                'pixelSize': 600
            },
            'fields': 'pixelSize'
        }
    },
    {
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheetId,
                'dimension': 'COLUMNS',
                'startIndex': 2,
                'endIndex': 3
            },
            'properties': {
                'pixelSize': 100
            },
            'fields': 'pixelSize'
        }
    }
]
    return formatting_requests


def get_credentials_file_path_API() -> str:
    try:
        credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH')
        if not credentials_file_path:
            root = tk.Tk()
            root.withdraw()
            credentials_file_path = filedialog.askopenfilename(title='Select Credentials File')
        return credentials_file_path
    except Exception as e:
        e_message = str(e) + " in: get_credentials_file_path() -> str"
        exception_message_API(e_message)

def error_information_message_API(msg_text_1: str, msg_text_2: str):
    messagebox.showerror('Error', msg_text_1)
    print(msg_text_2)

    # error_information_message = {
    #     'msg_text_1': msg_text_1,
    #     'msg_text_2': msg_text_2
    # }
    # output_file = "static/error_information_message.json"
    # if os.path.exists(output_file):
    #     os.remove(output_file)
    # with open(output_file, 'w') as json_file:
    #     json.dump(error_information_message, json_file, indent=4)

    exit()


def exception_message_API(e_message): 
    messagebox.showerror('Error', f'Transcriber did not finish its work due to an unexpected error. You may fix the error and try again. Error description: {e_message}')
    print(f'Transcriber did not finish its work due to an unexpected error. You may fix the error and try again. Error description: {e_message}')
    
    # exception_message = {
    #     'e_message': e_message
    # }
    # output_file = "static/exception_message.json"
    # if os.path.exists(output_file):
    #     os.remove(output_file)
    # with open(output_file, 'w') as json_file:
    #     json.dump(exception_message, json_file, indent=4)
    
    
    exit()



# def main():

#     # video_link = 'gs://gavit-bucket/short-video.mkv'
#     video_link = 'gs://gavit-bucket/wideo.mkv'
#     # language_code = 'en-US'
#     language_code = 'pl-PL'
#     # spreadsheet_id = '1d-2vH2ny3o_ZXKuODSx4WKyv2XTabMd6gkomGneizdg'
#     spreadsheet_id = '1i9ek5vkEsaY0v8Bw0sLgT_A3diFNqDLiD8nabPywy24'
#     cell_address = 'C2'
#     sheet_name = 'Arkusz5'


#     transcription(video_link, language_code, spreadsheet_id, sheet_name, cell_address)


# if __name__ == '__main__':
#     main()