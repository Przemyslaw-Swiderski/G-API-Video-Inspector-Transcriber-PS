from flask import(
    Flask, jsonify, render_template,
    request, session, redirect, url_for
)
import datetime
import os
import bcrypt
from dotenv import load_dotenv
from waitress import serve
import re

load_dotenv()

app = Flask(__name__)
app.secret_key= os.environ.get('SECRET_KEY')


# REST API endpoint
@app.route('/gavit', methods=['POST'])
def gavit():
    if request.method == "POST":
        gavit_data = request.form

    print(gavit_data)

    return "Echo test funkcji niestandardowej: " + gavit_data["content"]


if __name__ == "__main__":

    app.run(
            host = '0.0.0.0',
            port = 8892,
            debug=True
        )
    
    # serve(app, port=8892, host="0.0.0.0")