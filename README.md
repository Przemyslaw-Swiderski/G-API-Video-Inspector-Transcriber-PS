# Video Transcriber
Transcriber is a Python script that transcribes speech from a video file and sends the transcription results to a Google Spreadsheet. It utilizes the Google Cloud Video Intelligence API for speech recognition and the Google Sheets API for interacting with the spreadsheet.

## Prerequisites
Before running the script, make sure you have the following:

1. Python 3.x installed on your system.

2. Google Cloud Platform (GCP) account with the Video Intelligence API and Sheets API enabled.

    Creating a Google Cloud Account
    If you don't have a Google Cloud account yet, create one at https://cloud.google.com/. You will need a Google Cloud account to access the Google Cloud Video Intelligence API.

3. API credentials file (api.json) with appropriate permissions for accessing the Video Intelligence and Sheets APIs.

    Obtaining an API Key
    Sign in to the Google Cloud Console (https://console.cloud.google.com/) using your Google Cloud account. Create a new project if you don't have one already. Then, go to the "Credentials" page (https://console.cloud.google.com/apis/credentials) and generate a new API key for your project. Make sure the Video Intelligence API and Google Sheets API are enabled in the "Library" tab (https://console.cloud.google.com/apis/library).

4. Google Spreadsheet preapared to obtain results of transcription.
    Please make sure that the Service Account has permisssion to edit the Google Spreadsheet preapared to display transcription results.
    You ma check the email address connected with the Service Account here: https://console.cloud.google.com/apis/api/videointelligence.googleapis.com/credentials

    If it is allowed by you confidence policy, you may give permision to view the Spreadsheet by anyone who have the link as weel. It'll be helpful if you want the sript to open the spreedsheet by Google acoount without specific permission to open it.
    Otherwise in order to avoid permission bugs, you need to block openning of the spreedsheet by the script setting OPEN_SPREADSHHEET_WHEN_FINISHED to NO in enviroment variables.

    Please pay attention to get proper ID of the Google Spreadsheet. Here is how to guide:
    - Open the Google Spreadsheet to which you want to obtain the ID.
    - Check the URL in the browser's address bar. It should have the following structure: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit, where "SPREADSHEET_ID" is the actual ID of the spreadsheet.
    - Copy the value of "SPREADSHEET_ID" from the URL.
    For example, if the URL of the Google Spreadsheet looks like this: https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789/edit, then the ID of the spreadsheet is 1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789.

5. FFmpeg installed and available in your system's PATH.
    To check if FFmpeg is installed and available in your system's PATH, you can type ffmpeg and press Enter.
    - If FFmpeg is installed and available in the PATH, it should display the version information and available options.
    - If FFmpeg is not installed or not in the PATH, the command prompt or terminal will display an error message indicating that the command is not recognized.
    - If FFmpeg is not installed or not in the PATH, you will need to install it and make sure it is accessible from the command prompt or terminal.

    Here are the general steps to install FFmpeg on Windows:
    - Download a static build of FFmpeg from the official website: https://ffmpeg.org/download.html#build-windows
    - Extract the downloaded ZIP file to a location on your computer.
    - Add the FFmpeg binary directory to the system's PATH:
    - Open the Start menu and search for "Environment Variables."
    - Select "Edit the system environment variables."
    - Click the "Environment Variables" button.
    - In the "System variables" section, select the "Path" variable and click "Edit."
    - Add the path to the FFmpeg binary directory (the one containing the ffmpeg.exe file) to the list of paths. For example, C:\ffmpeg\bin.
    - Click "OK" to save the changes.

## Setting up the Environment and Installation
To ensure a clean and isolated environment for running the script, it is recommended to create a virtual environment using venv.

### Here are the steps to set up the environment:
Open a terminal or command prompt.
Navigate to the root directory of the project.
On Windows, run the following command to create a virtual environment:
```
python -m venv myenv
```
This command creates a new virtual environment named myenv. You can choose any name for your virtual environment.

Activate the virtual environment:
```
.\myenv\Scripts\activate
```
Activating the virtual environment ensures that the script and its dependencies are installed and executed within the isolated environment.


### Installation
Clone this repository to your local machine or download the source code.

Install the required dependencies by running the following command in the project directory:
```
pip install -r requirements.txt
```


## Usage
1. If you want to use the script for any automation pourposes it may be convenient to set up the necessary environment variables in .env file located in the root directory of the project. Strings are required. Template of the .env file included in the project.

    The required information include:
    Path to the API credentials file (api.json). Example:
    CREDENTIALS_FILE_PATH="C:\Users\Username\G-API-Video-Inspector-Transcriber\static\api.json" as absolute path or relative path: "static/api.json"

    Path to the video file to transcribe. Example: 
    VIDEO_FILE_PATH="C:\Users\Username\G-API-Video-Inspector-Transcriber\static\video.mp4" as absolute path or relative path: "static/video.mp4"

    ID of the Google Spreadsheet where the transcription results will be stored. Example:
    GOOGLE_SPREADSHEET_ID="1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789"

    Language code for the speech in the video (e.g., en-US for English, es-ES for Spanish). Example:
    LANGUAGE_CODE="pl-PL"

    Information if the spreadsheet with results shoud be open automaticaly by script. Example:
    OPEN_OUTPUT_SPREADSHHEET_WHEN_READY="YES"

    If you do not provide them as environment variables you may provide them when prompted by the script. This may be usefull when you need transcription of one or few files from time to time.

2. Run the script using the following command:
    ```
    python gavt_main.py
    ```
    The script will transcribe the speech from the video, display a progress bar, and upload the results to the specified Google Spreadsheet.

## Limitations
Supported video formats.
The Video Intelligence API supports common video formats, including .MOV, .MPEG4, .MP4, .AVI, and the formats decodable by ffmpeg.
For more limitations, please read https://cloud.google.com/video-intelligence/quotas.

## Troubleshooting
If you encounter any issues or errors during the execution of the script, please refer to the following:

Make sure you have provided all the required information correctly (credentials file path, video file path, spreadsheet ID, and language code).
Ensure that the API credentials file (api.json) is in the expected location and has the necessary permissions.
Check your internet connection and ensure that you have access to the Video Intelligence API and Sheets API.
If the error persists, please refer to the error message displayed by the script and consult the Google Cloud API documentation for troubleshooting steps.

## License
This project is licensed under the MIT License.

Feel free to modify and customize the script to fit your specific requirements.

## Responsibility disclaimer
Author of the script do not take any responsibility for any losses made by script and its usage. User uses the sript on own responsibility.

## Acknowledgments
This script utilizes the Google Cloud Video Intelligence API and Google Sheets API.