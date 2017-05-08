import logging
import json
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, logger
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

from twilio.rest import Client

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def prompt_welcome():
    msg = render_template('prompt_welcome')
    return question(msg)


@ask.intent("GetMoodIntent", convert={'mood':str})
def prompt_get_mood(mood):
    session.attributes['mood'] = mood
    msg = render_template('prompt_get_mood', mood = mood)
    # return statement("I'm sorry I don't recognize that mood")


    myRes = "Response "+str(session.attributes['mood'])
    return question("You are feeling " + str(session.attributes['mood']) +", want to do something?" )

    # if moodResponse is None:
    # return statement("")


@ask.intent("RespondToMoodIntent")
def great_intent():
    moodResponse =  session.attributes['mood']

    happyMoods = ['happy', 'good', 'fine', 'excellent', 'well', 'splendid', 'well','okay', 'blessed', 'joyful', 'Content', 'Decent', 'Healthy', 'Pleased', 'Untroubled' ]
    
    sickMoods = ['hurting', 'unwell', 'bad', 'under-the- weather', 'under the weather', 'suffering', 'unhealthy','weak', 'feverish', 'poor', 'lousy', 'queasy', 'nauseous', 'weird', 'funny', 'uncomfortable' ]
    
    lonelyMoods = ['so-so', 'so so' 'alone', 'sad', 'down', 'upset', 'bored', 'angry', 'tired', 'depressed', 'fair', 'run-of- the-mill', 'run of  the mill', 'mad', 'blue', 'down-in the-dumps', 'down in the dumps', 'homesick', 'agitated', 'confused', 'dismayed', 'distressed', 'distressed', 'shocked', 'worried', 'frantic', 'lost', 'run down', 'run-down']


    r  = None
    if moodResponse in happyMoods:
        r = happyFunction()
        return statement(r)

    elif moodResponse in sickMoods:
        # r = sadFunction()
        # return statement(r)
        return question("Can I play you some music? Or would you rather hear a joke?")


    elif moodResponse in lonelyMoods:
        # r = lonelyFunction()
        return question("Can I play you some music? Or would you rather hear a joke?")

        # sendEmail()
        # return statement(r)

    else:
        return question("sorry, didnt get that")
    # print moodResponse

    if r is None:
        return statement("I'm sorry I don't recognize that mood")

    # return statement("You feel great")

    # if r is not None:
    #     print "*"*50
    #     print r
    #     return statement("got it")
communityCalendar = ["Adult Coloring at The Public Library at 2pm", "The Mummies show at The MET at 4pm"]

def happyFunction():
    suggestion = ""
    for event in communityCalendar:
        suggestion += event
    finalsuggestion = "Let's get the day started. Here are the available events in your area," + suggestion
    return finalsuggestion

def sadFunction():
    return question("Can I play you some music? Or would you rather hear a joke?" )
    
def lonelyFunction():
    return question("Can I play you some music? Or would you rather hear a joke?")

def sickFunction():
    return 'Oh no! What wrong? Would you like to be connected to Teledoc?'
    # return 'Would you like to talk to'


@ask.intent("TellAJokeIntent")
def tellAJokeIntent():
    return statement("Why does 6 hate 7? Because 7 ate 9")

def sendEmail():
    textfile = 'myfile.txt'
    fp = open(textfile, 'rb')
    # Create a text/plain message
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] = 'The contents of %s' % textfile
    msg['From'] = "ofure.ukpebor@gmail.com"
    msg['To'] = "ofure.ukpebor@gmail.com"

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail("ofure.ukpebor@gmail.com", ["ofure.ukpebor@gmail.com"], msg.as_string())
    s.quit()

if __name__ == '__main__':
    app.run(debug=True)