import pytest
import gavit_utilities as gu
from unittest import mock


def test_get_credentials_file_path():
    # Test when environment variable is set
    with mock.patch.dict('os.environ', {'CREDENTIALS_FILE_PATH': 'path/to/credentials.json'}):
        assert gu.get_credentials_file_path() == 'path/to/credentials.json'

    # Test when environment variable is not set
    with mock.patch('tkinter.filedialog.askopenfilename', return_value='path/to/credentials.json'):
        assert gu.get_credentials_file_path() == 'path/to/credentials.json'


def test_get_video_file_path():
    # Test when environment variable is set
    with mock.patch.dict('os.environ', {'VIDEO_FILE_PATH': 'path/to/video.mp4'}):
        assert gu.get_video_file_path() == 'path/to/video.mp4'

    # Test when environment variable is not set
    with mock.patch('tkinter.filedialog.askopenfilename', return_value='path/to/video.mp4'):
        assert gu.get_video_file_path() == 'path/to/video.mp4'


def test_is_video_decodable():
    # Test with a decodable video file
    with mock.patch('subprocess.run', return_value=mock.Mock(returncode=0)):
        assert gu.is_video_decodable('path/to/video.mp4') == True

    # Test with a non-decodable video file
    with mock.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, '')):
        assert gu.is_video_decodable('path/to/video.mp4') == False


def test_get_google_spreadsheet_id():
    # Test when environment variable is set
    with mock.patch.dict('os.environ', {'GOOGLE_SPREADSHEET_ID': 'spreadsheet_id'}):
        assert gu.get_google_spreadsheet_id() == 'spreadsheet_id'

    # Test when user input is required
    with mock.patch('tkinter.StringVar.get', return_value='spreadsheet_id'), mock.patch('tkinter.Tk'), \
         mock.patch('tkinter.Entry'), mock.patch('tkinter.Button'), mock.patch('tkinter.messagebox') as mock_messagebox:
        assert gu.get_google_spreadsheet_id() == 'spreadsheet_id'
        mock_messagebox.assert_not_called()