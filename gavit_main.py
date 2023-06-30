import os
from google.oauth2 import service_account
import gavit_utilities

def main():
    os.system('cls')
    print('Transcriber started to work. Please wait.')
    credentials_file_path = gavit_utilities.get_credentials_file_path()
    video_file_path = gavit_utilities.get_video_file_path()
    if not gavit_utilities.is_video_decodable(video_file_path):
        msg_text_1 = 'The video file is not decodable by FFmpeg. Please provide proper file and start again'
        gavit_utilities.error_information_message(msg_text_1, msg_text_1)

    google_spreadsheet_id = gavit_utilities.get_google_spreadsheet_id()
    language_code = gavit_utilities.get_language_code()
    open_output_when_ready = gavit_utilities.get_open_output_spreadsheet_when_ready()

    if not credentials_file_path or not video_file_path or not google_spreadsheet_id or not language_code or not open_output_when_ready:
        msg_text_1 = 'Missing required information. You may start again and provide credentials file path, video file path, Google Spreadsheet ID and language code.'
        msg_text_2 = 'Transcriber did not finish his work, because of missing input data. You may try again providing necessary data.'
        gavit_utilities.error_information_message(msg_text_1, msg_text_2)

    credentials = service_account.Credentials.from_service_account_file(credentials_file_path)

    input_content = gavit_utilities.input_video_content(video_file_path)
    transcription_results = gavit_utilities.transcribe_video(input_content, credentials, language_code)
    gavit_utilities.send_to_spreadsheet(transcription_results, credentials, google_spreadsheet_id)

    if open_output_when_ready == 'YES':
        gavit_utilities.open_google_spreadsheet(google_spreadsheet_id)

if __name__ == '__main__':
    main()