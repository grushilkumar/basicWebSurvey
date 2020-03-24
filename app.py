from flask import Flask, session, app, render_template, request, Markup
import sys, io, re
import os, base64
from io import StringIO
from datetime import datetime
import time

app = Flask(__name__)

# get root path for account in cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# survey page
@app.route("/", methods=['POST', 'GET'])
def survey_page():
    message = ''
    first_name = ''
    last_name = ''
    email = ''
    gender = ''
    are_you_happy = 'Choose one...'
    tell_us_more = ''
    Family_checked = ''
    Friends_checked = ''
    Colleagues_checked = ''
    # this is a list so create a string to append into csv file
    recommend_this_to_string = ''


    if request.method == 'POST':

        # check that we have all the required fields to append to file
        are_you_happy = request.form['are_you_happy']
        recommend_this_to = request.form.getlist('recommend_this_to')
        tell_us_more = request.form['tell_us_more']
        # remove special characters from input for security
        tell_us_more = re.sub(r"[^a-zA-Z0-9]","",tell_us_more)

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']

        # optional fields
        if date_of_birth=='':
            date_of_birth = 'NA'
        if 'gender' in request.form:
            gender = request.form['gender']
        else:
            gender = 'NA'


        # check that essential fields have been filled
        message = ''
        missing_required_answers_list = []
        if are_you_happy == 'Choose one...':
            missing_required_answers_list.append('Are you happy?')
        if len(recommend_this_to) == 0:
            missing_required_answers_list.append('Who would you recommend this survey to?')
        else:

            for val in recommend_this_to:
                recommend_this_to_string += val + ' '
                if val == 'Family':
                    Family_checked = 'checked'
                if val == 'Friends':
                    Friends_checked = 'checked'
                if val == 'Colleagues':
                    Colleagues_checked = 'checked'

        if tell_us_more == '':
            missing_required_answers_list.append('Tells us more')
        if first_name == '':
            missing_required_answers_list.append('First name')
        if last_name == '':
            missing_required_answers_list.append('Last name')
        if email == '':
            missing_required_answers_list.append('Email')


        if len(missing_required_answers_list) > 0:
            # return back a string with missing fields
            message = '<div class="w3-row-padding w3-padding-16 w3-center"><H3>You missed the following question(s):</H3><font style="color:red;">'
            for ms in missing_required_answers_list:
                message += '<BR>' + str(ms)
            message += '</font></div>'
        else:
            # append survey answers to file

            # create a unique timestamp for this entry
            entry_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


            # save to file and send thank you note
            with open(BASE_DIR + '/surveys/survey_samp_1.csv','a+') as myfile: # use a+ to append and create file if it doesn't exist
                myfile.write(
                    str(entry_time) + ',' +
                    str(last_name) + ',' +
                    str(email) + ',' +
                    str(date_of_birth) + ',' +
                    str(are_you_happy) + ',' +
                    str(recommend_this_to_string) + ',' +
                    str(tell_us_more) + ','
                    + '\n')

            # return thank-you message
            message = '<div class="w3-row-padding w3-padding-16 w3-center"><H2><font style="color:blue;">Thank you for taking the time to complete this survey</font></H2></div>'


    return render_template('survey.html',
        message = Markup(message),
        first_name = first_name,
        last_name = last_name,
        email = email,
        gender = gender,
        tell_us_more = tell_us_more,
        Family_checked = Family_checked,
        Friends_checked = Friends_checked,
        Colleagues_checked = Colleagues_checked,
        are_you_happy = are_you_happy)


# used only in local mode
if __name__=='__main__':
    app.run(debug=True)
