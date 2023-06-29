import os
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import base64
import time
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from dotenv import load_dotenv

os.system('cls')
print('Transcriber started to work. Please wait.')

load_dotenv()


def get_credentials_file_path():
    root = tk.Tk()
    root.withdraw()
    credentials_file_path = filedialog.askopenfilename(title="Select Credentials File")
    return credentials_file_path


def get_spreadsheet_id():
    root = tk.Tk()
    root.withdraw()

    dialog = tk.Toplevel(root)
    dialog.title("Spreadsheet ID")
    dialog.geometry("450x120")  # Adjust the width and height as needed

    label = tk.Label(dialog, text="Enter Spreadsheet ID:")
    label.pack(pady=10)

    default_value = "1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI"
    entry = tk.Entry(dialog, width=60)  # Adjust the width as needed
    entry.insert(0, default_value)  # Set default value
    entry.pack(pady=5)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=5)

    ok_button = tk.Button(button_frame, text="OK", command=dialog.destroy)
    ok_button.pack(side=tk.LEFT, padx=5)

    cancel_button = tk.Button(button_frame, text="Cancel", command=root.destroy)
    cancel_button.pack(side=tk.LEFT, padx=5)

    dialog.focus_set()
    dialog.wait_window()

    spreadsheet_id = entry.get()
    return spreadsheet_id



def get_video_file_path():
    root = tk.Tk()
    root.withdraw()
    video_file_path = filedialog.askopenfilename(title="Select Video File")
    return video_file_path



credentials_file_path = get_credentials_file_path()
video_file_path = get_video_file_path()
spreadsheet_id = get_spreadsheet_id()


# credentials_file_path = "api.json"
# video_file_path = "static/wideo.mkv"
# spreadsheet_id = "1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI"

credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
video_service = build('videointelligence', 'v1', credentials=credentials)


def input_video_content(video_file_path):
    with open(video_file_path, 'rb') as video_file:
        input_content = base64.b64encode(video_file.read()).decode('utf-8')
    return input_content


def transcribe_video(input_v_content):
    features = ['SPEECH_TRANSCRIPTION']
    language_code = 'pl-PL'  # Replace with your desired language code

    operation = video_service.videos().annotate(body={
        'inputContent': input_v_content,
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

    os.system('cls')
    print('Transcriber finished it\'s work !')


input_v_content = input_video_content(video_file_path)
transcription_results = transcribe_video(input_v_content)
send_to_spreadsheet(transcription_results)