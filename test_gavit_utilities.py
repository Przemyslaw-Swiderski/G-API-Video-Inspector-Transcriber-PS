import pytest
import gavit_utilities as gu
from unittest import mock
import subprocess


def test_get_credentials_file_path():
    # Test when environment variable is set
    with mock.patch.dict('os.environ', {'CREDENTIALS_FILE_PATH': 'static/api.json'}):
        assert gu.get_credentials_file_path() == 'static/api.json'

    # Test when environment variable is not set
    with mock.patch('tkinter.filedialog.askopenfilename', return_value='static/api.json'):
        assert gu.get_credentials_file_path() == 'static/api.json'


def test_get_video_file_path():
    # Test when environment variable is set
    with mock.patch.dict('os.environ', {'VIDEO_FILE_PATH': 'static/wideo.mkv'}):
        assert gu.get_video_file_path() == 'static/wideo.mkv'

    # Test when environment variable is not set
    with mock.patch('tkinter.filedialog.askopenfilename', return_value='static/wideo.mkv'):
        assert gu.get_video_file_path() == 'static/wideo.mkv'


def test_is_video_decodable():
    # Test with a decodable video file
    with mock.patch('subprocess.run', return_value=mock.Mock(returncode=0)):
        assert gu.is_video_decodable('static/wideo.mkv') == True

    # Test with a non-decodable video file
    with mock.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, '')):
        assert gu.is_video_decodable('static/wideo.mkv') == False


def test_get_google_spreadsheet_id():
    # Test when environment variable is set
    with mock.patch.dict('os.environ', {'GOOGLE_SPREADSHEET_ID': '1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI'}):
        assert gu.get_google_spreadsheet_id() == '1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI'

    # Test when user input is required
    with mock.patch('tkinter.StringVar.get', return_value='1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI'), mock.patch('tkinter.Tk'), \
         mock.patch('tkinter.Entry'), mock.patch('tkinter.Button'), mock.patch('tkinter.messagebox') as mock_messagebox:
        assert gu.get_google_spreadsheet_id() == '1XedGFXQbfyBUuaS5g4Uwq1V1BDbCzu40VooF4cFjVbI'
        mock_messagebox.assert_not_called()