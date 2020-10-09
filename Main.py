# using flask_restful
from flask import Flask, jsonify
from flask_restful import Resource, Api

import random

app = Flask(__name__)       # creating the flask app
api = Api(app)              # creating an API object

word_to_guess = list("")    # the word that the user has to guess
my_word = list("")          # the word that the user has created by guessing letters
letters_to_guess = 0        # the length of the hidden word
alphabet = list("")         # the list of tried letters
lives = 0                   # number of lives


class Hangman(Resource):
    """
    Create a new hangman game, by choosing a word and creating 5 lives
    """
    def post(self):
        global word_to_guess
        global my_word
        global lives
        global letters_to_guess
        global alphabet

        # getting a random word from the file
        lines = open("words.txt").readlines()
        line = lines[0]
        words = line.split()

        word_to_guess = random.choice(words)
        my_word = "_" * len(word_to_guess)

        # setting number of lives and letters_to_guess
        lives = 5
        letters_to_guess = len(word_to_guess)

        # resetting the alphabet
        alphabet = list("")

        return jsonify({'my_word': "".join(my_word), 'lives': lives, 'letters_to_guess': letters_to_guess})

    """
    Getting a status of current game, returning: word_to_guess, my_word, lives
    """
    def get(self):
        global my_word
        global lives
        global letters_to_guess
        global alphabet
        return jsonify({'my_word': "".join(my_word), 'lives': lives, 'letters_to_guess': letters_to_guess,
                        'alphabet': "".join(sorted(alphabet))})


class Guess(Resource):
    """
    Guessing a letter
    """
    def put(self, letter):
        global word_to_guess
        global my_word
        global lives
        global alphabet
        global letters_to_guess

        # check number of lives
        if lives == 0:
            return jsonify({'my_word': "".join(my_word), 'lives': lives,
                            'message': "no more lives, please make a request for a new word"})

        # check correct input
        if len(letter) != 1:
            return jsonify({'my_word': "".join(my_word), 'lives': lives,
                            'message': "please type only one letter"})

        # check if letter already guessed
        if letter in alphabet:
            return jsonify({'my_word': "".join(my_word), 'lives': lives, 'alphabet': "".join(sorted(alphabet)),
                            'message': "letter already guessed"})

        # check letter in the word
        if letter not in word_to_guess:
            lives -= 1
            alphabet.append(letter)
            return jsonify({'my_word': "".join(my_word), 'lives': lives, 'message': "letter not in word",
                            'letters_to_guess': letters_to_guess})

        # put occurrences of letter in my_word
        for i in range(len(word_to_guess)):
            if word_to_guess[i] == letter:
                my_word = my_word[:i] + letter + my_word[i + 1:]
                letters_to_guess -= 1

        # check if the word got guessed
        if word_to_guess == my_word:
            return jsonify({'word_to_guess': "".join(word_to_guess), 'my_word': "".join(my_word), 'lives': lives,
                            'message': "CONGRATULATION YOU FOUND THE HIDDEN WORD. YOU DESERVE A COOKIE"})

        alphabet.append(letter)
        return jsonify({'my_word': "".join(my_word), 'lives': lives, 'message': "letter found",
                        'letters_to_guess': letters_to_guess})


class Solution(Resource):
    """
    Getting solution of the game
    """
    def get(self):
        global word_to_guess
        global my_word
        return jsonify({'word_to_guess': "".join(word_to_guess), 'my_word': "".join(my_word)})


# paths to api calls
api.add_resource(Hangman, '/hangman/')
api.add_resource(Guess, '/hangman/guess/<string:letter>')
api.add_resource(Solution, '/hangman/solution/')

# driver function
if __name__ == '__main__':
    app.run(debug=True)

