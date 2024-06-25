import random

def random_word():
    with open('hangman_words.txt', 'r') as wordfile:
        random_word = random.choice(wordfile.readlines()).strip()
    return random_word
    
def print_statements():
    print("Lets play an interesting game............")
    print("I have a secret word for you.....")
    print("Can you guess the ecret_word,blanks,chances,choiceword????")
    answer=input("Y/N????")
    if(answer.lower()=="y"):
        print("You have only 7 chances..........")
        print("Are you ready?")
        answer=input("Y/N???")
        if(answer.lower()=="y"):
            print("Lets Start")
        else:
            print("Oops..")
            exit()
    else:
        print("Oops..")
        exit()
def masking(secret_word):
    blanks=""
    for letter in range(len(secret_word)):
        blanks=blanks+"-"
    print("Guess this",len(secret_word),"letter secret word :",blanks)
    print(secret_word)
    return blanks,secret_word

def guess_letter(secret_word):
    secret_word=random_word()
    blanks, secret_word = masking(secret_word)
    chances = 7
    choice_check = []
    
    while chances > 0 and '-' in blanks:
        choice = input("Enter your guess : ").lower()
        
        # Check if the input is a single alphabetic character
        if not choice.isalpha() or len(choice) != 1:
            print("Enter a valid single alphabet")
            continue
        
        if not checking_duplications(choice, choice_check):
            continue
        
        if choice in secret_word:
            blanks = unmasking(secret_word, choice, blanks)
            print(blanks)
        else:
            chances -= 1
            death(chances)
            print(f"You have {chances} chances left.")
    
    result(blanks)
    return blanks

def checking_duplications(choice,choice_check):
    if choice in choice_check:
        print("You have already guessed",{choice},"Try a new alphabet.")
        return False
    else:
        choice_check.append(choice)
        return True




def unmasking(secret_word,choice,blanks):
    new_blanks=list(blanks)
    for index in range(len(secret_word)):
        if(secret_word[index] == choice):
            new_blanks[index]=choice
    return "".join(new_blanks)


def result(blanks):
    if "-" not in blanks:
        print("Congratulations..You guessed the word correctly")
    else:
        print("Ooops..You ran out of chances")


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
    print(deathh[chances])


if __name__ == '__main__':
    print_statements()
    secret_word=random_word()
    guess_letter(secret_word)