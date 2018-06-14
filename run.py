from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin
from flask_login import current_user
import os, trivia

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

API_URL = 'https://opentdb.com/api.php?amount=1'

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Define minimal User data-model for basic user sign in
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

# Create all database tables
db.create_all()

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

@app.route('/', methods=['POST','GET'])
@login_required    # User must be authenticated
def index():
    # Check user supplied answer and save if correct or render on screen if incorrect
    if request.method == "POST":
        trivia.save_user_answer(current_user.username,
                                 request.form["answers"])
        # print(request.form["answers"] , qa_dict['correct_answer'])
        # if trivia.correct_answer(qa_dict['correct_answer'], request.form["answers"]):
        #     print('Blah')
        # else:
        #     print('value')

    qa_dict = trivia.get_question_answer(current_user.username, API_URL)
    cat_icon = trivia.choose_category_icon(qa_dict['category'])

    return render_template('index.html', question_answer = qa_dict, cat_icon = cat_icon)

# The Members page is only accessible to authenticated users via the @login_required decorator
@app.route('/scores')
@login_required    # User must be authenticated
def scores():
    # String-based templates
    return render_template('scores.html')

if __name__ == "__main__":
    # int(os.getenv('PORT'))
    app.run(host=os.getenv('IP'), port=5000, debug=True)
