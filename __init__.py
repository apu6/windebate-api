from flask import Flask
from flask_cors import CORS
from flask import ( request )
from flask_mail import Mail, Message

import gspread
import json

from oauth2client.service_account import ServiceAccountCredentials
from werkzeug.exceptions import NotFound
 
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'w.indebate2019@gmail.com',
	MAIL_PASSWORD = 'qgucMvK5%3a~nX'
	)
mail = Mail(app)

mentees_index = 2
mentors_index = 2




@app.route('/mentees', methods=['POST', 'GET'])
def mentees():

    global mentees_index
    global mail

    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('win-debate-cb25db181fef.json', scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("win-debate").sheet1
    

    if request.method == 'POST':
        req = request.get_json()
        
        row = [req["email"], req["password"], req["firstName"], req["lastName"], req["age"], req["school"], req["preferences"]]
        sheet.insert_row(row, mentees_index)
        mentees_index += 1

        msg = Message("New mentee signup", sender="w.indebate2019@gmail.com", 
        recipients=[
            "w.indebate2019@gmail.com",
            # "lindseyperlman14@gmail.com",
            # "claire.liu333@gmail.com",
            # "wuxjulia@gmail.com"
            ])
        msg.body = "New mentee: " + req["firstName"] + ' ' + req["lastName"] + " has signed up. Please check the spreadsheet."
        mail.send(msg)

        return json.dumps(row)

    elif request.method == 'GET':
        all_mentees = sheet.get_all_records()
        print(all_mentees)
        return json.dumps(all_mentees)

@app.route('/mentors', methods=['POST', 'GET'])
def mentors():
    
    global mentors_index
    global mail

    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('win-debate-cb25db181fef.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("win-debate").get_worksheet(1)

    if request.method == 'POST':
        req = request.get_json()
        
        row = [req["email"], req["password"], req["firstName"], req["lastName"], req["age"], req["school"], req["experience"]]
        sheet.insert_row(row, mentors_index)
        mentors_index += 1


        msg = Message("New mentor signup", sender="w.indebate2019@gmail.com", 
        recipients=[
            "w.indebate2019@gmail.com",
            # "lindseyperlman14@gmail.com",
            # "claire.liu333@gmail.com",
            # "wuxjulia@gmail.com"
            ])
        msg.body = "New mentor: " + req["firstName"] + ' ' + req["lastName"] + " has applied. Please check the spreadsheet."
        mail.send(msg)

        return json.dumps(row)

    elif request.method == 'GET':
        all_mentors = sheet.get_all_records()
        print(all_mentors)
        return json.dumps(all_mentors)

@app.route('/mentors/<int:id>', methods=['GET'])
def getMentor(id):

    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('win-debate-cb25db181fef.json', scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("win-debate").get_worksheet(1)

    # id_col = sheet.col_values(8)

    mentor_row = sheet.row_values(id)



    return json.dumps(mentor_row)


@app.route('/mentees/<int:id>', methods=['GET'])
def getMentee(id):

    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('win-debate-cb25db181fef.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("win-debate").get_worksheet(0)

    mentee_row = sheet.row_values(id)

    return json.dumps(mentee_row)



@app.route('/login/mentee', methods=['POST'])
def menteeLogin():

    global mentors_index
    global mail
    

    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('win-debate-cb25db181fef.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("win-debate").sheet1

    if request.method == 'POST':
        req = request.get_json()
        if req["email"] == "" or req["password"] == "":
            raise NotFound()

        row = 1
        for email in sheet.col_values(1):
            if email == req["email"]:
                for password in sheet.col_values(2):
                    if password == req["password"]:
                        return json.dumps(sheet.row_values(row))
            else:
                row +=1
        raise NotFound()


    elif request.method == 'GET':
        all_mentors = sheet.get_all_records()
        print(all_mentors)
        return json.dumps(all_mentors)

@app.route('/login/mentor', methods=['POST'])
def mentorLogin():

    global mentors_index
    global mail
    

    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('win-debate-cb25db181fef.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("win-debate").get_worksheet(1)

    if request.method == 'POST':
        req = request.get_json()

        
        row = 2
        for email in sheet.col_values(1):
            if email == req["email"]:
                for password in sheet.col_values(2):
                    if password == req["password"]:
                        return json.dumps(sheet.row_values(row))
                    else:
                        raise NotFound()
            else:
                row +=1
        raise NotFound()


    elif request.method == 'GET':
        all_mentors = sheet.get_all_records()
        print(all_mentors)
        return json.dumps(all_mentors)

@app.errorhandler(NotFound)
def handle_404(err):
    return 'Not found', 404

if __name__ == '__main__':
   app.run()



