import unittest
import trivia

class TestTrivia(unittest.TestCase):
    '''
    Testing suite for the "My Trivia" flask app
    '''
    def test_question_answer_retrieved(self):
        # Check that a question and answer are successfully retrieved from the API
        username = "abcd"
        api_url = "https://opentdb.com/api.php?amount=1"
        qa = trivia.get_question_answer(username, api_url)
        print('Check that a question and answer are successfully retrieved from the API', qa)
        self.assertIsNotNone(qa)

    def test_correct_answers_identified(self):
        # Check that correct answers can be identified
        username = "abcd"
        user_qas = trivia.read_user_question_answer(username)
        print('Check that correct answers can be identified')
        for list_element in user_qas:
            if list_element[1] == list_element[4]:
                self.assertEqual(list_element[1], list_element[4])

    def test_incorrect_answers_identified(self):
        # Check that incorrect answers can be identified
        username = "abcd"
        user_qas = trivia.read_user_question_answer(username)
        print('Check that incorrect answers can be identified')
        for list_element in user_qas:
            if list_element[1] != list_element[4]:
                self.assertNotEqual(list_element[1], list_element[4])

    def test_category_icon(self):
        # Verify that the correct icon class is selected according to the question category
        icon = trivia.choose_category_icon("Sports")
        print('Verify that the correct icon class is selected according to the question category', icon)
        self.assertIn("tennis", icon)

    def test_duplicate_questions(self):
        # Check that there are no duplicate questions for a user
        all_questions = [question[0] for question in trivia.read_user_question_answer("abcd")]
        number_questions = len(all_questions)
        number_unique_questions = len(set(all_questions))
        print('Check that there are no duplicate questions for a user', number_questions, number_unique_questions)
        self.assertEqual(number_questions, number_unique_questions)

    def test_previous_question_available(self):
        # Check that we are able to access the previously asked/answered question
        # so that it can be rendered on the main quiz page
        latest_qa = trivia.read_user_question_answer("abcd")[-1]
        print('Check that we are able to access the previously asked/answered question', latest_qa)
        self.assertEqual(len(latest_qa), 5)

    def test_score_calculation(self):
        # Manually calculate the score and check that the function calculated score matches
        username = "abcd"
        correct_score = 18

        calculated_score = trivia.calculate_user_scores(username)
        calculated_score_overall = calculated_score['overall']
        calculated_score_rest = sum(calculated_score.values()) - calculated_score_overall

        print('Manually calculate the score and check that the function calculated score matches',
              correct_score, calculated_score_overall, calculated_score_rest)

        self.assertEqual(calculated_score_overall, correct_score)
        self.assertEqual(calculated_score_overall, calculated_score_rest)

    def test_leaderboard_number(self):
        '''
        Check that the right number of users appear on the leader board
        '''
        lboard = trivia.leader_board(3)
        print('Check that the right number of users appear on the leader board', lboard)
        self.assertEqual(len(lboard), 3)
