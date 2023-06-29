import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import webbrowser

load_dotenv()

def get_credentials_file_path():
    credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH')
    if not credentials_file_path:
        root = tk.Tk()
        root.withdraw()
        credentials_file_path = filedialog.askopenfilename(title='Select Credentials File')
    return credentials_file_path


def get_video_file_path():
    video_file_path = os.environ.get('VIDEO_FILE_PATH')
    if not video_file_path:
        root = tk.Tk()
        root.withdraw()
        video_file_path = filedialog.askopenfilename(title='Select Video File')
    return video_file_path


def get_google_spreadsheet_id():
    google_spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    if not google_spreadsheet_id:
        dialog = tk.Toplevel()
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


def get_language_code():
    language_code = os.environ.get('LANGUAGE_CODE')
    if not language_code:
        dialog = tk.Toplevel()
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


def get_open_output_spreadsheet_when_ready():
    open_output_spreadsheet_when_ready = os.environ.get('OPEN_OUTPUT_SPREADSHEET_WHEN_READY')
    if not open_output_spreadsheet_when_ready:
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askquestion("Open transription autoamatically ?", "Do you want to open the output spreadsheet when transcription is ready?")
        open_output_spreadsheet_when_ready = 'YES' if result == 'yes' else 'NO'
    return open_output_spreadsheet_when_ready


def input_video_content(video_file_path):
    with open(video_file_path, 'rb') as video_file:
        input_content = base64.b64encode(video_file.read()).decode('utf-8')
    return input_content


def open_google_spreadsheet(spreadsheet_id):
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
    webbrowser.open(url)


def no_required_information_message():
    msg_text='''Missing required information.
You may start again and provide credentials file path, video file path, Google Spreadsheet ID and language code.'''
    messagebox.showerror('Error', msg_text)
    print('Transcriber did not finish his work, because of missing input data. You may try again providing necessary data.')
    exit()


def display_error_message(message):
    messagebox.showerror('Error', message)