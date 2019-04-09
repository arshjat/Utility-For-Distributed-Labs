

#                     --------------------ARSH PANGHAL---------------------



# IMPORT PACKAGES                    ---------------------------------------------------------------------------
from flask import Flask, flash, redirect, url_for, jsonify
from flask import render_template, request
from werkzeug import secure_filename
from datetime import datetime
import pyrebase
import summary
import KeyWord
import os
import tempfile
import csv
import json
import ppt
from pusher import Pusher
import similarity
import operator



#  CONFIGURE FIREBASE API-------------------------------------------------------------------------------------------

# We are using a 3rd party library 'PYREBASE' for connecting firebase to our project
# Requirements : A firebase account and API credentials.

config = {
    "apiKey": "...",
    "authDomain": "...",
    "databaseURL": "...",
    "projectId": "...",
    "storageBucket": "...",
    "messagingSenderId": "..."
  }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
email = "..."
password = "..."
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()               

#  CONGIGURE PUSHER API--------------------------------------------------------------------------------------------

# This API may be helpful in dynamic searching of queries in the database and showing them on frontend interactively, 
# though there is no significant contibution of this API in this project even after a significant number of attempts.

import pusher
pusher_client = pusher.Pusher(
  app_id='...',
  key='...',
  secret='...',
  cluster='ap2',
  ssl=True
)


# START  APP-----------------------------------------------------------------------------------------------------
app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['ppt','pptx'])

# CONFIGURE UPLOAD FOLDER
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

# CONFIGURE SECURITY KEY
SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SECRET_KEY'] = SECRET_KEY


def allowed_file(filename):
        """
        This function checks if the input file has an extension and if it has one, does it belong to one of the 
        allowed extensions.
        Input :        Filename
        Output :       Boolean
        Requirements : ALLOWES_EXTENSIONS
        """
        return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


# CONFIGURING ROUTES--------------------------------------------------------------------------------------------

#1 INDEX
@app.route('/')
def upload():
        """
        This function renders the index.html file.
        """
        return render_template('index.html')

#2 UPLOADER
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
        """
        This function takes a post request from the 'Form' on index.html page and first uploads the file locally
        (so that the text is extracted from it without the hassle of contacting Firebase again and again),
        and the sends the file to another route where text is extracted from it. It is also thouroghly
        checked if the type of file submitted is relevent and that NULL is not supplied, otherwise an error is produced.
        """
        if request.method == 'POST':
                # check if the post request has the file part
                if 'ppt' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                file = request.files['ppt']
                var = request.form['name']

                # if user does not select file, browser also submit an empty part without filename
                if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)

                if file :
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return redirect(url_for("extract"))
                
        return "unsuccessful operation"

#3 EXTRACTER
@app.route("/extract")
def extract():
        """
        This function extracts the text from the slides and sends to another route where it is saved in FireBase.
        """
        my_list = ppt.extract_text()
        with open('extracted.txt', 'w') as f:
                for item in my_list:
                        f.write("%s " % item)
        return redirect(url_for('feed_to_database'))
        

#4 SEND TO DATABASE
@app.route("/to_database")
def feed_to_database():
        """
        This function first arranges the input into suitable json format and then feeds the schema to the Data Base
        """
        summarized_text = summary.summarize()
        key_words = KeyWord.extract_doc()
        date = str(datetime.now())
        data = {
                # "name":var,
                "summary":summarized_text,
                "key_words":key_words,
                "date_time":date,
        }
        db.child("DATA").push(data);
        
        return render_template("search.html")


#5 ADD DYNAMIC RESULTS TO THE SEARCH SCREEN
@app.route('/add',methods=['POST'])
def add():
        """
        THIS IS THE MOST IMPORTANT FUNCTION !

        This function extracts the query from the 'FORM' on the Search.html page and then sends the query for
        kew word extraction. Then this list of key words is compared to the keywords of all the entries present
        in the database and a dictionary of corresponding scores is made using similarity_score metric that uses
        both the cosine_similarity and the length_similarity metrics.

        The dictionary is then sorted in descending order of scores and is keys are stored in a list to present 
        dynamically on the Search.html page.

        The list is sent through jinja templating to the html file.
        There are quite some improvements to be made in this dynamic presentation and overall UI as a whole.
        """
        if request.method == 'POST':
                query =request.form['query']
                list_q = KeyWord.extract(query)
                values = db.child("DATA").get()
                rows = json.loads(json.dumps(db.child("DATA").get().val()))

                l  = {}
                for key,value in rows.items():
                        l[key] =  value['summary']

                scores = {}
                for i,j in l.items():
                        scores[i] = similarity.similarity_score(list_q,j)
                sorted_x = sorted(scores.items(), key=lambda kv: kv[1])
                p = []
                for i in sorted_x:
                        p.append(l[i[0]])
                return render_template("search.html", p=p)

# CONFIGURE ERROR HANDLING---------------------------------------------------------------------------------------
def errorhandler(e):
    """
    Show error
    """
    return render_template("error.html", eName=e.name, eCode=e.code)


# MAIN ---------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)