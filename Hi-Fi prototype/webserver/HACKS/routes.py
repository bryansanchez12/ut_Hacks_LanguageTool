from flask import render_template, request, redirect, url_for

from HACKS import app
from HACKS.script import fix, globalScores, addDocument, getDocumentsSpelling, getDocumentsGrammar, grammar_checker, getCounters, getGrammarMistakes, getSpellingMistakes

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['inputEmail'] == "admin@admin.com" and request.form['inputPassword'] == "password":
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/create_user')
def create_user():
    return render_template('create_user.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/close')
def close():
    return render_template('close.html')

@app.route('/settings/submit_settings')
def settingsSubmit():
    return "hello"

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        file = request.files['file']
        text = file.read().decode()

        # Check for Spelling errors
        improved = fix(text)

        # Check for Grammar errors
        improved = grammar_checker(improved)

        # Store the name of the file
        addDocument(file.filename)
        return render_template('check.html', text=text, improved=improved)
    else:
        return render_template('check.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create/check', methods=['POST'])
def check_text_from_Create():
    text = request.form['text']

    # Check for Spelling errors
    improved = fix(text)

    # Check for Grammar errors
    improved = grammar_checker(improved)

    return improved

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

#Inside Feedback Routes
@app.route('/feedback/grammar')
def grammar():
    return render_template('grammar.html')

@app.route('/feedback/spelling')
def spelling():
    return render_template('spelling.html')

@app.route('/feedback/punctuation')
def punctuation():
    return render_template('punctuation.html')

@app.route('/feedback/formality')
def formality():
    return render_template('formality.html')

@app.route('/feedback/readability')
def readability():
    return render_template('readability.html')

@app.route('/feedback/getGlobalScores', methods = ["GET"])
def getGlobalScores():
    return globalScores()

@app.route('/feedback/spelling/getScoreList', methods = ["GET"])
def getScoreSpelling():
    return getDocumentsSpelling()

@app.route('/feedback/grammar/getScoreList', methods = ["GET"])
def getScoreGrammar():
    return getDocumentsGrammar()

@app.route('/home/getCounters', methods = ["GET"])
def getGlobalCounters():
    return getCounters()

@app.route('/feedback/grammar/getMistakes', methods = ["GET"])
def getMistakesListGrammar():
    return getGrammarMistakes()

@app.route('/feedback/spelling/getMistakes', methods = ["GET"])
def getMistakesListSpelling():
    return getSpellingMistakes()
