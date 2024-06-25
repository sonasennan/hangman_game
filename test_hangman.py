import unittest
from unittest.mock import patch,mock_open
import sys
from io import StringIO
from hangman import random_word,masking,unmasking,checking_duplications,guess_letter,result
from unittest import TestCase,mock


def print_statements_y_y():  
    print("Lets play an interesting game............")
    print("I have a secret word for you.....")
    print("Can you guess the word????")
    print("Y/N????")
    print("You have only 7 chances..........")
    print("Are you ready?")
    print("Y/N???")
    print("Lets Start")

def print_statements_n():
    print("Lets play an interesting game............")
    print("I have a secret word for you.....")
    print("Can you guess the word????")
    print("Y/N????")
    print("Oops..")

def print_statements_y_n():
    print("Lets play an interesting game............")
    print("I have a secret word for you.....")
    print("Can you guess the word????")
    print("Y/N????")
    print("You have only 7 chances..........")
    print("Are you ready?")
    print("Y/N???")
    print("Oops..")

def death(chances):          
    deathh={                             
    6:"|_______\n|  |\n|\n|\n|\n|\n|_",
    5:"|_______\n|  |\n|  0\n|\n|\n|\n|_",
    4:"|_______\n|  |\n|  0\n| / \n|\n|\n|_",
    3:"|_______\n|  |\n|  0\n| / \\ \n|\n|\n|_",
    2:"|_______\n|  |\n|  0\n| /|\\ \n|\n|\n|_",
    1:"|_______\n|  |\n|  0\n| /|\\ \n| /\n|\n|_",
    0:"|_______\n|  |\n|  0\n| /|\\ \n| / \\\n|\n|_"
    }  
    return deathh.get(chances, "")       
    

class TestRandomWord(unittest.TestCase):

    def test_random_word(self):
        result = random_word()
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

class TestPrintStatements(unittest.TestCase):
    @patch('builtins.input',side_effect=['y','y'])
    def test_play_and_start(self,mock_input):
        captured_output=StringIO()
        sys.stdout=captured_output

        print_statements_y_y()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output="\n".join(["Lets play an interesting game............" , "I have a secret word for you....." ,"Can you guess the word????",
        "Y/N????",
        "You have only 7 chances..........",
        "Are you ready?",
        "Y/N???",
        "Lets Start" ])
        self.assertEqual(output,expected_output)


    @patch('builtins.input', side_effect=['N'])
    def test_decline_to_play(self, mock_input):
        captured_output=StringIO()
        sys.stdout=captured_output

        print_statements_n()

        sys.stdout=sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output = "\n".join(["Lets play an interesting game............",
            "I have a secret word for you.....",
            "Can you guess the word????",
            "Y/N????",
            "Oops.."])
        self.assertEqual(output, expected_output)


    @patch('builtins.input', side_effect=['Y', 'N'])
    def test_play_and_cancel_start(self, mock_input):
        captured_output=StringIO()
        sys.stdout=captured_output

        print_statements_y_n()

        sys.stdout=sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output = "\n".join([
            "Lets play an interesting game............",
            "I have a secret word for you.....",
            "Can you guess the word????",
            "Y/N????",
            "You have only 7 chances..........",
            "Are you ready?",
            "Y/N???",
            "Oops.."
        ])
        self.assertEqual(output, expected_output)


class TestDeathFunction(unittest.TestCase):
    def test_death(self):
        self.assertEqual(death(6),"|_______\n|  |\n|\n|\n|\n|\n|_")
        self.assertEqual(death(5),"|_______\n|  |\n|  0\n|\n|\n|\n|_")


class TestMaskingFunction(unittest.TestCase):
    def test_empty_word(self):
        word=""
        expected_output=""
        blanks,result=masking(word)
        self.assertEqual(blanks,expected_output, "Expected output does not match")

    def test_word(self):
        word="python"
        expected_output="------"
        blanks,result=masking(word)
        self.assertEqual(len(blanks), len(expected_output), "Expected output does not match")


class TestUnmaskingFunction(unittest.TestCase):

    def test_unmasking_single_match(self):
        secret_word = "python"
        choice = "o"
        blanks = "------"
        expected_output = "----o-"

        result = unmasking(secret_word, choice, blanks)
        self.assertEqual(result, expected_output)

    def test_unmasking_multiple_matches(self):
        secret_word = "python"
        choice = "p"
        blanks = "------"
        expected_output = "p-----"

        result = unmasking(secret_word, choice, blanks)
        self.assertEqual(result, expected_output)

    def test_unmasking_no_match(self):
        secret_word = "python"
        choice = "z"
        blanks = "------"
        expected_output = "------"

        result = unmasking(secret_word, choice, blanks)
        self.assertEqual(result, expected_output)

    def test_unmasking_empty_word(self):
        secret_word = ""
        choice = "a"
        blanks = ""
        expected_output = ""

        result = unmasking(secret_word, choice, blanks)
        self.assertEqual(result, expected_output)

    def test_unmasking_long_word(self):
        secret_word = "elephant"
        choice = "e"
        blanks = "--------"
        expected_output = "e-e-----"

        result = unmasking(secret_word, choice, blanks)
        self.assertEqual(result, expected_output)

class TestCheckingDuplicationsFunction(unittest.TestCase):

    def test_first_guess(self):
        choice_check = [] 
        choice = 'a' 
        result = checking_duplications(choice, choice_check)
        self.assertTrue(result)
        self.assertIn(choice, choice_check)

    def test_duplicate_guess(self):
        choice_check = ['b']  # Predefined list with 'b' already guessed
        choice = 'b' 
        result = checking_duplications(choice, choice_check)
        self.assertFalse(result)   #Should return False for duplicate guess
        self.assertEqual(len(choice_check),1)     # Ensure 'b' is not added again

class TestResult(unittest.TestCase):
    def setUp(self):
        self.held_output=StringIO
        sys.stdout=self.held_output
    
    def tearDown(self):
        sys.stdout=sys.__stdout__

    def test_without_blanks(self):
        blanks="Hangman"
        result(blanks)
        self.assertEqual(self.held_output.getvalue(),"Congratulations..You guessed the word correctly")

class TestResult(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
    
    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_without_blanks(self):
        blanks = "Hangman"
        result(blanks)
        self.assertEqual(self.held_output.getvalue().strip(), "Congratulations..You guessed the word correctly")


    def test_with_blanks(self):
        blanks="Han-man"
        result(blanks)
        self.assertEqual(self.held_output.getvalue().strip(),"Ooops..You ran out of chances")


class TestGuessLetter(unittest.TestCase):
    @patch('hangman.random_word',return_value="python")
    @patch('hangman.masking',return_value=("------","python"))
    @patch('hangman.result')
    @patch('hangman.input',side_effect=['p','y','t','h','o','n'])
    def test_guess_correct_letter(self,mock_input,mock_result,mock_masking,mock_random_word):
        with patch('builtins.print') as mock_print:
            blanks="python"
            result(blanks)
        self.assertIn("Congratulations..",mock_print.call_args.args[0])



    @patch('hangman.random_word',return_value='python')
    @patch('hangman.masking',return_value=("------","python"))
    @patch('hangman.result')
    @patch('hangman.input',side_effect=['p','y','t','h','o','z','a','b','c','v','j','l'])
    def test_guess_incorrect_letter(self,mock_input,mock_result,mock_masking,mock_random_word):
        with patch('builtins.print') as mock_print:
            blanks="pytho-"
            result(blanks)
        self.assertIn("Ooops..",mock_print.call_args.args[0])


    
    @patch('hangman.random_word',return_value="python")
    @patch('hangman.masking',return_value=("------","python"))
    @patch('hangman.result')
    @patch('hangman.input',side_effect=['p','y','t','1','o','n'])
    def test_guess_correct_letter(self,mock_input,mock_result,mock_masking,mock_random_word):
        with patch('builtins.print') as mock_print:
            blanks="pyt_on"
            result(blanks)
        self.assertIn("Congratulations..",mock_print.call_args.args[0])




if __name__ == '__main__':
    unittest.main()

