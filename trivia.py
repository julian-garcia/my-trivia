import requests, html, random

def save_question_answer(username, question, actual_answer, category, difficulty):
    with open("data/" + username + ".txt", "a") as userfile:
        userfile.writelines("1. Question: " + question + "\n" +
                            "2. Correct Answer: " + actual_answer + "\n" +
                            "3. Category: " + category + "\n" +
                            "4. Difficulty: " + difficulty + "\n")

def get_question_answer(username, api_url):
    question_answer = {}
    json_data = requests.get(api_url).json()
    json_status = json_data['response_code']
    if json_status == 0:
        question_answer = json_data['results'][0]
        # Translate html characters e.g. &copy; back to readable text
        question_answer['question'] = html.unescape(question_answer['question'])
        question_answer['incorrect_answers'] = [html.unescape(x) for x in question_answer['incorrect_answers']]
        question_answer['correct_answer'] = html.unescape(question_answer['correct_answer'])

        # Combine correct answer and incorrect answers to facilitate rendering
        # all possible answers on the web page. Also randomise so that the position
        # of the correct answer does not follow a pattern
        question_answer['all_answers'] = list(question_answer['incorrect_answers'])
        question_answer['all_answers'].append(question_answer['correct_answer'])
        random.shuffle(question_answer['all_answers'])

        save_question_answer(username, question_answer['question'],
                             question_answer['correct_answer'],question_answer['category'],
                             question_answer['difficulty'])
    return question_answer

def correct_answer(correct_answer, user_answer):
    if correct_answer == user_answer:
        return True
    else:
        return False

def calculate_user_score(username):
    pass

def save_user_answer(username, user_answer):
    with open("data/" + username + ".txt", "a") as userfile:
        userfile.writelines("5. User Answer: " + user_answer + "\n")

def read_user_question_answer(username):
    pass

def choose_category_icon(category):
    fa_icon_prefix = '<i class="fas '
    fa_icon_suffix = '"></i>'

    if category == "General Knowledge":
        fa_class = "fa-question"
    elif category == "Sports":
        fa_class = "fa-table-tennis"
    elif "Music" in category:
        fa_class = "fa-music"
    elif "Video Games" in category:
        fa_class = "fa-gamepad"
    elif "Vehicles" in category:
        fa_class = "fa-bus"
    elif "Computers" in category:
        fa_class = "fa-desktop"
    elif "Science" in category:
        fa_class = "fa-flask"
    elif "Animals" in category:
        fa_class = "fa-kiwi-bird"
    elif category.startswith("Entertainment"):
        fa_class = "fa-film"
    else:
        fa_class = "fa-question"

    fontawesome_icon = fa_icon_prefix + fa_class + fa_icon_suffix
    return fontawesome_icon
