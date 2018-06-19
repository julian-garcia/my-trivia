# My Trivia
A Flask based website to deliver random trivia questions to users, log their
answers, calculate a score for the user and display a top scorer league table.

# Usage Instructions
## Installation
```
git clone https://github.com/julian-garcia/my-trivia.git
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
## Running Locally
```
python run.py
http://localhost:5000
```
## Deployment (Heroku)
```
heroku login
heroku apps:create my-app-name
git push -u heroku master
heroku ps:scale web=1
```
Don't forget to add config vars: IP 0.0.0.0 and PORT 5000
Restart dynos

# Languages and Frameworks
The python micro framework Flask was used to implement this trivia quiz app. The
following languages/libraries were used:
- HTML5
- CSS3
- Javascript
- jQuery 3.3.1
- Python 3.6.5
- SASS
- Bootstrap 4
- Fontawesome 5.0.13
- Google fonts

# Branding and Colour Scheme
The colour scheme was set using Adobe Color CC ([color.adobe.com](https://color.adobe.com)), using
the predefined colour scheme, "Bahamas".

# Wireframing
The wireframe xml file was generated using draw.io so to view the wireframes you
should open the file "Mockup.xml" via [draw.io](https://draw.io).

# Testing
Unit testing results are in unit_tests.txt
- [x] Question and answer is available
- [x] Incorrect answer being correctly identified
- [x] Category icon class corresponds to question category
- [x] Question has not already been asked previously
- [x] Score calculation is correct
- [x] Category scores add up to total score
- [x] Previous question/answer is accessible for rendering
- [x] Top n scorers identified for the leaderboard

# APIs
For trivia question and answer content the "Open Trivia Database" API is being
used: https://opentdb.com - free for commercial use creative commons licence
