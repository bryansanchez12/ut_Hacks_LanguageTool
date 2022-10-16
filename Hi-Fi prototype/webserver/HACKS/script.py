from bisect import bisect_left
from autocorrect import Speller
import language_tool_python
import difflib
import json

spell = Speller(lang='en')

#       List of checked documents
documents_spelling = ["", "", ""]
documents_grammar = ["", "", ""]


#                   Score Lists
#  layout:  [ Score, Previous_Score, Average_Score ]
score_list_Grammar = [100, 0, 0]
score_list_Spelling = [100, 0, 0]
score_list_Punctuation = [100, 0, 0]
score_list_Formality = [100, 0, 0]
score_list_Readability = [100, 0, 0]
score_list_Total = [100, 0, 0]

#                   Global Counters
# mistakes = [ grammar_mistakes,  spelling_mistakes ]
mistakes = [0, 0]

#       List of Grammar mistakes
grammar_mistakes = []
spelling_mistakes = []

# Function that adds a mistake into a list in order to access to them on the Grammar Page
def addGrammarMistake(mistake, solution):
    temp = True
    for word in grammar_mistakes:
        if word == mistake:
            temp = False

    if temp:
        words = [mistake, solution]
        grammar_mistakes.append(words)

# Function that adds a mistake into a list in order to access to them on the Spelling Page
def addSpellingMistake(mistake, solution):
    temp = True
    for word in spelling_mistakes:
        if word == mistake:
            temp = False

    if temp:
        words = [mistake, solution]
        spelling_mistakes.append(words)


# Function that stores the filename and the score of such a document
def addDocument(filename):
    #   Update Document list based on Spelling Feedback
    var1 = documents_spelling[0]
    var2 = documents_spelling[1]
    temp = [filename, score_list_Spelling[0]]
    documents_spelling[2] = var2
    documents_spelling[1] = var1
    documents_spelling[0] = temp

    #   Update Document list based on Grammar Feedback
    var3 = documents_grammar[0]
    var4 = documents_grammar[1]
    temp2 = [filename, score_list_Grammar[0]]
    documents_grammar[2] = var4
    documents_grammar[1] = var3
    documents_grammar[0] = temp2



def get_dictionary():
    dictionary = []
    with open("HACKS/files/words.txt", 'r') as f:
        dictionary = f.read().lower().splitlines()
    return dictionary


def convert_string_to_array(string):
    return string.split(" ")


def remove_punctuation(string):
    punc = '!()-[]{};:\'"\\, <>./?@#$%^&*_~'

    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")

    return string


def NO_errors(array):
    errors = ""
    dictionary = get_dictionary()

    for word in array:
        if remove_punctuation(word.lower()) not in dictionary:
            errors += " " + word + "-" + spell(word)

    return errors


# Function that calculate the total number of words in a text
def totalNumberOfWords(text):
    list = text.split()
    number_of_words = len(list)
    return number_of_words


# Function that takes all values of all score lists and return a JSON object
def globalScores():
    list = []
    list.append(score_list_Grammar)
    list.append(score_list_Spelling)
    list.append(score_list_Punctuation)
    list.append(score_list_Formality)
    list.append(score_list_Readability)
    list.append(score_list_Total)

    temp = {'scores': []}
    for x in list:
        y = {"score": str(x[0]),
             "prev_score": str(x[1]),
             "avg_score": str(x[2])}
        temp['scores'].append(y)

    json.dumps(temp, sort_keys=True, indent=4)
    return temp

# Function that return the counters of grammar and spelling for the overview
def getCounters():
    temp = {}
    temp['counters'] = []
    x = {"grammar": mistakes[0], "spelling":  mistakes[1]}
    temp['counters'].append(x)
    json.dumps(temp, sort_keys=True, indent=4)
    return temp

# Function that returns the grammar mistakes
def getGrammarMistakes():
    temp = {}
    temp['mistakes'] = []
    for x in grammar_mistakes:
        y = {"mistake": x[0],
             "solution":x[1]}
        temp['mistakes'].append(y)

    json.dumps(temp, sort_keys=True, indent=4)
    return temp

# Function that return the spelling mistakes
def getSpellingMistakes():
    temp = {}
    temp['mistakes'] = []
    for x in spelling_mistakes:
        y = {"mistake": x[0],
             "solution":x[1]}
        temp['mistakes'].append(y)

    json.dumps(temp, sort_keys=True, indent=4)
    return temp


# Function that takes the name of the improved documents so far, as well as their scores
def getDocumentsSpelling():
    list = documents_spelling
    temp = {}
    temp['scores'] = []
    i = 0
    while i < 3:
        if list[i] == "":
            y = {"name": "-",
                 "value": str(0)}
            temp['scores'].append(y)
        else:
            y = {"name": str(list[i][0]),
                 "value": str(list[i][1])}
            temp['scores'].append(y)
        i += 1
    json.dumps(temp, sort_keys=True, indent=4)
    return temp

# Function that takes the name of the improved documents so far, as well as their scores
def getDocumentsGrammar():
    list = documents_grammar
    temp = {}
    temp['scores'] = []
    i = 0
    while i < 3:
        if list[i] == "":
            y = {"name": "-",
                 "value": str(0)}
            temp['scores'].append(y)
        else:
            y = {"name": str(list[i][0]),
                 "value": str(list[i][1])}
            temp['scores'].append(y)
        i += 1
    json.dumps(temp, sort_keys=True, indent=4)
    return temp


# Function that updates the score at Spelling as well as the total score
def updateScoreSpelling(percentage):
    state = True
    try:
        score = score_list_Spelling[0]
        new_score = percentage
        average = round((score + new_score) / 2)
        #           Update list
        score_list_Spelling[0] = new_score
        score_list_Spelling[1] = score
        score_list_Spelling[2] = average
        #           Update Total Score
        t_score = (score_list_Grammar[0] + score_list_Spelling[0] + score_list_Punctuation[0]
                   + score_list_Formality[0] + score_list_Readability[0]) / 5
        t_prev_score = (score_list_Grammar[1] + score_list_Spelling[1] + score_list_Punctuation[1]
                        + score_list_Formality[1] + score_list_Readability[1]) / 5
        t_avg_score = (score_list_Grammar[2] + score_list_Spelling[2] + score_list_Punctuation[2]
                       + score_list_Formality[2] + score_list_Readability[2]) / 5
        score_list_Total[0] = round(t_score)
        score_list_Total[1] = round(t_prev_score)
        score_list_Total[2] = round(t_avg_score)
    except:
        state = False

    return state

# Function that updates the score at Grammar as well as the total score
def updateScoreGrammar(percentage):
    state = True
    try:
        score = score_list_Grammar[0]
        new_score = percentage
        average = round((score + new_score) / 2)
        #           Update list
        score_list_Grammar[0] = new_score
        score_list_Grammar[1] = score
        score_list_Grammar[2] = average
        #           Update Total Score
        t_score = (score_list_Grammar[0] + score_list_Spelling[0] + score_list_Punctuation[0]
                   + score_list_Formality[0] + score_list_Readability[0]) / 5
        t_prev_score = (score_list_Grammar[1] + score_list_Spelling[1] + score_list_Punctuation[1]
                        + score_list_Formality[1] + score_list_Readability[1]) / 5
        t_avg_score = (score_list_Grammar[2] + score_list_Spelling[2] + score_list_Punctuation[2]
                       + score_list_Formality[2] + score_list_Readability[2]) / 5
        score_list_Total[0] = round(t_score)
        score_list_Total[1] = round(t_prev_score)
        score_list_Total[2] = round(t_avg_score)
    except:
        state = False

    return state

def updateGrammarCounter(value):
    temp = mistakes[0] + value
    mistakes[0] = temp

def updateSpellingCounter(value):
    temp = mistakes[1] + value
    mistakes[1] = temp

def checkDifferences(wrong_text, improved_text):
    words1 = convert_string_to_array(wrong_text)
    words2 = convert_string_to_array(improved_text)
    result = []
    i = 0

    while i < len(words1):
        if words1[i] != words2[i]:
            result.append(words1[i])
        i += 1

    return result

def grammar_checker(string):
    # Mention the language keyword
    tool = language_tool_python.LanguageToolPublicAPI('en')

    # Check for errors:
    matches = tool.check(string)
    total = totalNumberOfWords(string)
    errorsCounter = len(matches)

    print("Errors in grammar: " + str(errorsCounter))
    updateGrammarCounter(errorsCounter)

    improved_string = tool.correct(string)
    output_list = checkDifferences(string, improved_string)
    output_listRight = checkDifferences(improved_string, string)

    # Add all mistakes into the respective list
    index = 0
    while index < len(output_list):
        addGrammarMistake(output_list[index], output_listRight[index])
        index += 1

    # Calculate the percentage of good words/total words and update the spelling score
    percentage = round(((total - errorsCounter) / total) * 100)
    if updateScoreGrammar(percentage):
        print("The grammar score was updated successfully")
    else:
        print("The grammar score could not be updated")


    # prints mistake one by one
    #for mistake in matches:
    #    print("************")
    #    print(mistake)
    #    print("************")
    #    print()

    return improved_string


def fix(string):
    total = totalNumberOfWords(string)
    result = spell(string)

    # Finds difference between strings in order to known how many errors such string had
    output_list = checkDifferences(string, result)
    errorsCounter = len(output_list)
    print("Errors in spelling: " + str(errorsCounter))
    updateSpellingCounter(errorsCounter)
    output_listRight = checkDifferences(result, string)

    # Add all mistakes into the respective list
    index = 0
    while index < len(output_list):
        addSpellingMistake(output_list[index], output_listRight[index])
        index += 1

    # Calculate the percentage of good words/total words and update the spelling score
    percentage = round(((total - errorsCounter) / total) * 100)
    if updateScoreSpelling(percentage):
        print("The spelling score was updated successfully")
    else:
        print("The spelling score could not be updated")

    return result
