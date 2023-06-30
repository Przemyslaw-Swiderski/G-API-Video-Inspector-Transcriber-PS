import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import time
import pandas as pd
from googleapiclient.discovery import build
import webbrowser
import subprocess

load_dotenv()

def get_credentials_file_path() -> str:
    try:
        credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH')
        if not credentials_file_path:
            root = tk.Tk()
            root.withdraw()
            credentials_file_path = filedialog.askopenfilename(title='Select Credentials File')
        return credentials_file_path
    except Exception as e:
        exception_message(e)


def get_video_file_path() -> str:
    try:
        video_file_path = os.environ.get('VIDEO_FILE_PATH')
        if not video_file_path:
            root = tk.Tk()
            root.withdraw()
            video_file_path = filedialog.askopenfilename(title='Select Video File')
        return video_file_path
    except Exception as e:
        exception_message(e)


def is_video_decodable(video_file_path: str) -> bool:
    try:
        command = ['ffmpeg', '-v', 'error', '-i', video_file_path, '-f', 'null', '-']
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


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


def input_video_content(video_file_path: str) -> str:
    with open(video_file_path, 'rb') as video_file:
        input_content = base64.b64encode(video_file.read()).decode('utf-8')
    return input_content


def open_google_spreadsheet(spreadsheet_id: str):
    try:
        url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
        webbrowser.open(url)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        exception_message(e)


def error_information_message(msg_text_1: str, msg_text_2: str):
    messagebox.showerror('Error', msg_text_1)
    print(msg_text_2)
    exit()


def exception_message(e): 
    messagebox.showerror('Error', f'An unexpected error occurred: {str(e)}')
    print(f'Transcriber did not finish its work due to an unexpected error. You may fix the error {e} and try again.')
    exit()

def transcribe_video(input_content: str, credentials: object, language_code: str) -> list:
    try:
        video_service = build('videointelligence', 'v1', credentials=credentials)
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
        while True:
            result = video_service.projects().locations().operations().get(name=operation_name).execute()
            if 'done' in result and result['done']:
                break
            time.sleep(1)
            os.system('cls')
            progress_bar = progress_bar + '.'
            print(progress_bar)

        annotation_results = result['response']['annotationResults'][0]
        if 'speechTranscriptions' in annotation_results:
            transcription_results = annotation_results['speechTranscriptions']
        else:
            transcription_results = []
        return transcription_results
    except Exception as e:
        exception_message(e)


def send_to_spreadsheet(transcription_results: list, credentials: object, google_spreadsheet_id: str):
    try:
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
        print('Transcriber finished its work !')
    except Exception as e:
        exception_message(e)