import os
from dotenv import load_dotenv
from google.cloud import videointelligence
from google.cloud import storage
import json
import uuid
import base64
import time
import pandas as pd
from googleapiclient.discovery import build
import webbrowser
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


load_dotenv()


def transcribe_video(input_content: str, video_uri: str, credentials: object, language_code: str) -> list:
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
        exception_message(e_message)

    check_if_gc_is_ready_with_transcription(credentials, operation_name)

    try:
        result = operation.result()

    except Exception as e:
        e_message = str(e) + " in: \" result = ...\" in def transcribe_video(input_content: str, credentials: object, language_code: str) -> list"
        exception_message(e_message)

    annotation_results = result.annotation_results[0]
    print(annotation_results.speech_transcriptions)
    transcription_data = process_transcription_data(annotation_results)
    if video_uri != '':
        delete_file_from_cloud(video_uri, credentials)
    return transcription_data


def check_if_gc_is_ready_with_transcription(credentials: object, operation_name: str):
    video_service = build('videointelligence', 'v1', credentials=credentials)
    time_elapsed = 0
    while True:
        result = video_service.projects().locations().operations().get(name=operation_name).execute()
        if 'done' in result and result['done']:
            break
        time.sleep(5)
        os.system('cls')
        print(f'Transcription in progress. Please wait. Time elapsed: {str(time_elapsed)} seconds')
        time_elapsed = time_elapsed + 5


def process_transcription_data(annotation_results):
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
    output_file = "static/result_temp_file.json"
    if os.path.exists(output_file):
        os.remove(output_file)
    with open(output_file, 'w') as json_file:
        json.dump(processed_transcription_data, json_file, indent=4)
    return processed_transcription_data


def send_to_spreadsheet(transcription_results: list, credentials: object, google_spreadsheet_id: str):
    try:
        rows = []
        for transcription in transcription_results:
            transcript = transcription['transcript']
            confidence = transcription['confidence']
            word_level_info = transcription['word_level_info']
            start_time = word_level_info[0]['start_time']
            end_time = word_level_info[-1]['end_time']
            new_row = {'Czas': f'{start_time} - {end_time}', 'Tekst': transcript, 'Confidence': confidence}
            rows.append(new_row)

        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        sheet.values().clear(spreadsheetId=google_spreadsheet_id, range='A:Z').execute()
        formatting_requests = create_formatting_requests_to_spreadsheet()
        sheet.batchUpdate(spreadsheetId=google_spreadsheet_id, body={'requests': formatting_requests}).execute()
        
        df = pd.DataFrame(rows, columns=['Czas', 'Tekst', 'Confidence'])
        header_values = [df.columns.tolist()]
        sheet.values().update(
            spreadsheetId=google_spreadsheet_id,
            range='A1',
            valueInputOption='RAW',
            body=dict(
                majorDimension='ROWS',
                values=header_values
            )
        ).execute()

        sheet.values().append(
            spreadsheetId=google_spreadsheet_id,
            range='A2',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=dict(
                majorDimension='ROWS',
                values=df.values.tolist()
            )
        ).execute()

        os.system('cls')
        print('Transcriber finished its work!')
    except Exception as e:
        e_message = str(e) + " in: def send_to_spreadsheet(transcription_results: list, credentials: object, google_spreadsheet_id: str)"
        exception_message(e_message)

def create_formatting_requests_to_spreadsheet():
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


def upload_video_to_cloud(video_file_path, credentials, bucket_name):
    storage_client = storage.Client(credentials=credentials)
    filename = os.path.basename(video_file_path)
    basename, extension = os.path.splitext(filename)
    blob_name = basename + '-' + str(uuid.uuid4()) + extension

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    print("Uploading video to Google Cloud Storage...")
    blob.upload_from_filename(video_file_path)

    video_uri = f"gs://{bucket_name}/{blob_name}"
    print("Video uploaded successfully.")

    return video_uri


def delete_file_from_cloud(video_uri, credentials):
    split_uri = video_uri.split("/")
    bucket_name = split_uri[2]
    blob_name = "/".join(split_uri[3:])

    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print(f"File '{video_uri}' deleted successfully.")


def input_video_content(video_file_path: str) -> str:
    with open(video_file_path, 'rb') as video_file:
        input_content = base64.b64encode(video_file.read()).decode('utf-8')
    return input_content


def is_video_decodable(video_file_path: str) -> bool:
    try:
        command = ['ffmpeg', '-v', 'error', '-i', video_file_path, '-f', 'null', '-']
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_credentials_file_path() -> str:
    try:
        credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH')
        if not credentials_file_path:
            root = tk.Tk()
            root.withdraw()
            credentials_file_path = filedialog.askopenfilename(title='Select Credentials File')
        return credentials_file_path
    except Exception as e:
        e_message = str(e) + " in: get_credentials_file_path() -> str"
        exception_message(e_message)


def get_video_file_path() -> str:
    try:
        video_file_path = os.environ.get('VIDEO_FILE_PATH')
        if not video_file_path:
            root = tk.Tk()
            root.withdraw()
            video_file_path = filedialog.askopenfilename(title='Select Video File')
        return video_file_path
    except Exception as e:
        e_message = str(e) + " in: def get_video_file_path() -> str"
        exception_message(e_message)


def get_google_spreadsheet_id() -> str:
    google_spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    if not google_spreadsheet_id:
        dialog = tk.Tk()
        dialog.title('Google spreadsheet ID necessary')
        dialog.geometry('400x120')

        label = tk.Label(dialog, text='Enter Google spreadsheet ID:')
        label.pack(pady=10)

        google_spreadsheet_id_var = tk.StringVar()

        entry = tk.Entry(dialog, width=60, textvariable=google_spreadsheet_id_var)
        entry.pack(pady=5)

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=5)

        ok_button = tk.Button(button_frame, text='OK', command=dialog.destroy)
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text='Cancel', command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        dialog.focus_set()
        dialog.wait_window()

        google_spreadsheet_id = google_spreadsheet_id_var.get()
    return google_spreadsheet_id


def get_language_code() -> str:
    language_code = os.environ.get('LANGUAGE_CODE')
    if not language_code:
        dialog = tk.Tk()
        dialog.title('Language code necessary')
        dialog.geometry('400x120')

        label = tk.Label(dialog, text='Enter language code:')
        label.pack(pady=10)

        language_code_var = tk.StringVar()

        default_value = 'pl-PL'
        entry = tk.Entry(dialog, width=20, textvariable=language_code_var)
        entry.insert(0, default_value)
        entry.pack(pady=5)

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=5)

        ok_button = tk.Button(button_frame, text='OK', command=dialog.destroy)
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text='Cancel', command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        dialog.focus_set()
        dialog.wait_window()

        language_code = language_code_var.get()
    return language_code


def get_open_output_spreadsheet_when_ready() -> str:
    open_output_spreadsheet_when_ready = os.environ.get('OPEN_OUTPUT_SPREADSHEET_WHEN_READY')
    if not open_output_spreadsheet_when_ready:
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askquestion("Open transription autoamatically ?", "Do you want to open the output spreadsheet when transcription is ready?")
        open_output_spreadsheet_when_ready = 'YES' if result == 'yes' else 'NO'
    return open_output_spreadsheet_when_ready


def open_google_spreadsheet(spreadsheet_id: str):
    try:
        url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
        webbrowser.open(url)
    except Exception as e:
        e_message = str(e) + " in: def open_google_spreadsheet(spreadsheet_id: str)"
        exception_message(e_message)


def error_information_message(msg_text_1: str, msg_text_2: str):
    messagebox.showerror('Error', msg_text_1)
    print(msg_text_2)
    exit()


def exception_message(e_message): 
    messagebox.showerror('Error', f'Transcriber did not finish its work due to an unexpected error. You may fix the error and try again. Error description: {e_message}')
    print(f'Transcriber did not finish its work due to an unexpected error. You may fix the error and try again. Error description: {e_message}')
    exit()