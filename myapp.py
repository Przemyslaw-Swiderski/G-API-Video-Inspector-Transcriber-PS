from flask import(
    Flask, jsonify, render_template,
    request, session, redirect, url_for)
import os
from dotenv import load_dotenv
from waitress import serve
import gavit_API
import threading

load_dotenv()

app = Flask(__name__)
app.secret_key= os.environ.get('SECRET_KEY')


# REST API endpoint funkcji niestandardowej
@app.route('/gavit', methods=['POST'])
def gavit():
    if request.method == "POST":
        gavit_data = request.form

    print(gavit_data)

    return "Echo test funkcji niestandardowej: " + str(gavit_data["content"])



# REST API endpoint onEdit
@app.route('/gavit-onedit', methods=['POST'])
def gavit_onedit():
    if request.method == "POST":
        gavit_data = request.get_json()

    print(gavit_data)

    # You can access the data using gavit_data["content"], gavit_data["cellAddress"], and gavit_data["oldValue"]
    # For example, to echo back the content:
    response_data = "Echo test funkcji onEdit. Test pozytywny. Przesłano dane: " + str(gavit_data["content"])

    return jsonify(response_data)



# REST API endpoint nsd
@app.route('/gavit-nsd', methods=['POST'])
def gavit_nsd():
    if request.method == "POST":
        gavit_data = request.get_json()
        video_link = gavit_data['videoLink']
        language_code = gavit_data['languageCode']
        spreadsheet_id = gavit_data['spreadsheetId']
        sheet_name =  gavit_data['sheetName']
        cell_address = gavit_data['cellAddress']

        print(video_link)
        print(language_code)
        print(spreadsheet_id)
        print(sheet_name)
        print(cell_address)


        task_thread = threading.Thread(target=gavit_API.transcription, args=(
                                            video_link,
                                            language_code,
                                            spreadsheet_id,
                                            sheet_name,
                                            cell_address
                                            )
                                        )
        task_thread.start()

    # gavit_API.transcription(video_link,
    #     language_code,
    #     spreadsheet_id,
    #     sheet_name,
    #     cell_address
    #     )


    response_data = "Transcription in progress, please wait ..."
    return jsonify(response_data)

# ten

if __name__ == "__main__":

    app.run(
            host = '0.0.0.0',
            port = 8894,
            debug=True
        )
    
    # serve(app, port=8894, host="0.0.0.0")