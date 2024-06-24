import unittest
from unittests.sut_ingestor import SUTIngestor
from deepdiff import DeepDiff

class TestDemo(unittest.TestCase):
    def setUp(self):
        self.SUT_ingestor = SUTIngestor('./mock_database.csv')
    def test_calculate_states_mean(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        res = self.SUT_ingestor.calculate_states_mean(question)
        exp_res = {'Ohio': 29.025, 'Washington': 37.599, 'Massachusetts': 28.95, 'New Hampshire': 35.3, 'Rhode Island': 19.7, 'Vermont': 37.9}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_state_mean(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        state = 'Ohio'
        res = self.SUT_ingestor.calculate_state_mean(state, question)
        exp_res = {'Ohio': 29.025}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_best5_states(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        res = self.SUT_ingestor.calculate_best5_states(question)
        exp_res = {'Vermont': 37.9, 'Washington': 37.599999999999994, 'New Hampshire': 35.3, 'Ohio': 29.025, 'Massachusetts': 28.95}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_worst5_states(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        res = self.SUT_ingestor.calculate_worst5_states(question)
        exp_res = {'Rhode Island': 19.7, 'Massachusetts': 28.95, 'Ohio': 29.025, 'New Hampshire': 35.3, 'Washington': 37.599}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_global_mean(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        res = self.SUT_ingestor.calculate_global_mean(question)
        exp_res = {'global_mean': 31.09}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_diff_from_mean(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        res = self.SUT_ingestor.calculate_diff_from_mean(question)
        exp_res = {'Ohio': 2.075, 'Washington': -6.5, 'Massachusetts': 2.145, 'New Hampshire': -4.20, 'Rhode Island': 11.4, 'Vermont': -6.8}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_state_diff_from_mean(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        state = 'Ohio'
        res = self.SUT_ingestor.calculate_state_diff_from_mean(state, question)
        exp_res = {'Ohio': 2.075}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_mean_by_category(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        res = self.SUT_ingestor.calculate_mean_by_category(question)
        exp_res = {"('Ohio', 'Income', '$75,000 or greater')": 29.09, 
                   "('Washington', 'Income', '$75,000 or greater')": 37.59, 
                   "('Massachusetts', 'Income', '$75,000 or greater')": 31.4, 
                   "('New Hampshire', 'Gender', 'Female')": 35.3, 
                   "('Rhode Island', 'Income', '$75,000 or greater')": 19.7, 
                   "('Ohio', 'Race/Ethnicity', 'Non-Hispanic Black')": 28.8, 
                   "('Massachusetts', 'Education', 'Some college or technical school')": 26.5, 
                   "('Vermont', 'Education', 'Less than high school')": 37.9}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    def test_calculate_state_mean_by_category(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        state = 'Ohio'
        res = self.SUT_ingestor.calculate_state_mean_by_category(state, question)
        exp_res = {'Ohio': {"('Income', '$75,000 or greater')": 29.099, 
                   "('Race/Ethnicity', 'Non-Hispanic Black')": 28.8}}
        d = DeepDiff(res, exp_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))