import os, requests, html, random, pickle, glob
from operator import itemgetter

def save_question_answer(username, question, actual_answer, category, difficulty):
    '''
    Save the current question, correct answer, category and difficulty level
    so that we can later add these details to the user file of all answered questions.
    We need to store this in a file so that the data persists after the answer is
    submitted/posted
    '''
    with open("data/" + username + "_current.txt", "w") as userfile:
        userfile.writelines(question + "\n" +
                            actual_answer + "\n" +
                            category + "\n" +
                            difficulty + "\n")

def save_user_answer(username, user_answer):
    '''
    Append the user's answer to the current question so that it can later be
    used to compare to the correct answer and calculate a score
    '''
    with open("data/" + username + "_current.txt", "a") as userfile:
        userfile.writelines(user_answer + "\n")

def commit_user_data(username):
    '''
    Store question and answer details in the user file in the form of one list per line.
    The list structure facilitates parsing the file later on when calculating scores
    '''
    user_data = []
    with open("data/" + username + "_current.txt", "r") as userfile:
        user_data = [line.strip() for line in userfile.readlines()]

    # The current user file should contain five lines if the user has attempted an answer,
    # any less and it means the user has refreshed the page without answering, in which
    # case we don't need to record the interaction in the user file
    if len(user_data) == 5:
        with open("data/" + username + ".txt", "ab") as fp:   #Pickling
            pickle.dump(user_data, fp)

        with open("data/" + username + ".txt", "a") as fp:
            fp.write("\n")

def get_category_list(api_url):
    '''
    Get category list - to be used to build a drop down in the suggestions form
    '''
    categories = []
    json_data = requests.get(api_url).json()
    categories = [element['name'] for element in json_data['trivia_categories']]
    return categories;

def get_question_answer(username, api_url):
    '''
    Query the opentdb API to retrieve a single random question and answer.
    The API is publicly available under the Creative Commons Attribution-ShareAlike 4.0
    International License
    '''
    question_answer = {}
    previous_questions = []
    json_data = requests.get(api_url).json()
    json_status = json_data['response_code']
    if json_status == 0:
        question_answer = json_data['results'][0]
        # Translate html characters e.g. &copy; back to readable text
        question_answer['question'] = html.unescape(question_answer['question'])
        question_answer['incorrect_answers'] = [html.unescape(x) for x in question_answer['incorrect_answers']]
        question_answer['correct_answer'] = html.unescape(question_answer['correct_answer'])

        # Check that the current question hasn't been previously answered by the logged in user
        # If it has been, then re-query the API by recursion until we have an unasked question
        previous_questions = [question[0] for question in read_user_question_answer(username)]
        if question_answer['question'] in previous_questions:
            get_question_answer(username, api_url)
        else:
            pass

        # Combine correct answer and incorrect answers to facilitate rendering
        # all possible answers on the web page. Also randomise the order so that
        # the position of the correct answer does not follow a pattern
        question_answer['all_answers'] = list(question_answer['incorrect_answers'])
        question_answer['all_answers'].append(question_answer['correct_answer'])
        random.shuffle(question_answer['all_answers'])

        save_question_answer(username, question_answer['question'],
                             question_answer['correct_answer'],question_answer['category'],
                             question_answer['difficulty'])
    return question_answer

def calculate_user_scores(username):
    '''
    Calculate overall and category scores based on the user file which holds a
    full history of answered questions for the specified user.
    '''
    scores = {}
    score = 0
    score_music = 0
    score_sports = 0
    score_science = 0
    score_vehicles = 0
    score_computers = 0
    score_entertainment = 0
    score_general = 0
    score_other = 0

    # Each list in the list of lists returned by read_user_question_answer
    # represents a question, correct answer and user answer. By looping through
    # these we can accumulate scores for the logged in user.
    for list_element in read_user_question_answer(username):
        # Scores awarded for each question are weighted according to difficulty
        if list_element[3] == "hard":
            score_value = 5
        elif list_element[3] == "medium":
            score_value = 3
        else:
            score_value = 1

        # Given a correct answer, established by comparing the actual answer with the
        # user supplied answer, accumulate scores according to the weighted value.
        # Split scores by category as well as an overall score.
        if list_element[1] == list_element[4]:
            score += score_value
            if "Music" in list_element[2]:
                score_music += score_value
            elif "Sports" in list_element[2]:
                score_sports += score_value
            elif "Science" in list_element[2]:
                score_science += score_value
            elif "Vehicles" in list_element[2]:
                score_vehicles += score_value
            elif "Computers" in list_element[2]:
                score_computers += score_value
            elif "Entertainment" in list_element[2]:
                score_entertainment += score_value
            elif "General Knowledge" in list_element[2]:
                score_general += score_value
            else:
                score_other += score_value

    scores = {"overall": score,
              "entertainment": score_entertainment,
              "music": score_music,
              "sports": score_sports,
              "science": score_science,
              "vehicles": score_vehicles,
              "computers": score_computers,
              "general": score_general,
              "other": score_other}

    return scores

def read_user_question_answer(username):
    '''
    Bring the full history of questions and answers for a specific user
    in to a list. Each question/answer set is a list in its own right
    for easier referencing for the score calculation.
    '''
    user_qa = []
    if os.path.isfile("data/" + username + ".txt"):
        with open("data/" + username + ".txt", "rb") as fp:   # Unpickling
            user_qa.append(pickle.load(fp))
            for line in fp:
                try:
                    user_qa.append(pickle.load(fp))
                except:
                    pass
    return user_qa

def leader_board(n):
    '''
    Collate the top n scorers in descending order of their overall score.
    These will then be tabulated on the leaderboad page and in the footer
    '''
    top_scores = []
    for filename in glob.iglob('data/*.txt'):
        if "_current" not in filename:
            uname = filename.split('/')[1].split('.')[0]
            uscore = calculate_user_scores(uname)['overall']
            top_scores.append({"username":uname, "score":uscore})
    # Sorting by 2 keys: descending score (primary) and ascending username (secondary)
    descending_top_scores = sorted(top_scores, key=lambda k: (-k['score'], k['username']))
    return descending_top_scores[:n]

def choose_category_icon(category):
    fa_icon_prefix = '<i class="fas '
    fa_icon_suffix = '"></i>'

    if category == "General Knowledge":
        fa_class = "fa-question"
    elif category == "Sports":
        fa_class = "fa-table-tennis"
    elif category == "Art":
        fa_class = "fa-image"
    elif "Music" in category:
        fa_class = "fa-music"
    elif "Video Games" in category:
        fa_class = "fa-gamepad"
    elif "Vehicles" in category:
        fa_class = "fa-bus"
    elif "Geography" in category:
        fa_class = "fa-globe"
    elif "History" in category:
        fa_class = "fa-history"
    elif "Politics" in category:
        fa_class = "fa-users"
    elif "Computers" in category:
        fa_class = "fa-desktop"
    elif "Science" in category:
        fa_class = "fa-flask"
    elif "Animals" in category:
        fa_class = "fa-kiwi-bird"
    elif "Entertainment" in category:
        fa_class = "fa-film"
    else:
        fa_class = "fa-question"

    fontawesome_icon = fa_icon_prefix + fa_class + fa_icon_suffix
    return fontawesome_icon
