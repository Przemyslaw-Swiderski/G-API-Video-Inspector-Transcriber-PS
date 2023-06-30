import pytest
from unittest import mock
from gavit_main import main

@pytest.mark.parametrize("input_values, expected_output", [
    (['path/to/credentials.json', 'path/to/video.mp4', 'spreadsheet_id', 'en-US', 'YES'], None),
    (['', 'path/to/video.mp4', 'spreadsheet_id', 'en-US', 'YES'], 'Missing required information'),
    (['path/to/credentials.json', '', 'spreadsheet_id', 'en-US', 'YES'], 'Missing required information'),
    (['path/to/credentials.json', 'path/to/video.mp4', '', 'en-US', 'YES'], 'Missing required information'),
    (['path/to/credentials.json', 'path/to/video.mp4', 'spreadsheet_id', '', 'YES'], 'Missing required information'),
    (['path/to/credentials.json', 'path/to/video.mp4', 'spreadsheet_id', 'en-US', ''], 'Missing required information'),
])
@mock.patch('builtins.input')
def test_main(mock_input, input_values, expected_output):
    mock_input.side_effect = input_values
    
    with mock.patch('gavit_main.gavit_utilities.error_information_message') as mock_error_message:
        main()

        if expected_output:
            mock_error_message.assert_called_with(expected_output, expected_output)
        else:
            mock_error_message.assert_not_called()
