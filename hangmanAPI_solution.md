# Hangman API

Hangman is a guessing game for two or more players. One player thinks of a word, phrase or sentence and the other(s) tries to guess it by suggesting letters within a certain number of guesses.
This API is a HTTP API creating a hangman game. The player (you)  should guess a hidden word, letter by letter, to win the game. Each player has a maximum of 5 lives. If you manage to guess the hidden word, you are congratulated with a cookie. 

## Create a new hangman game

To create a new hangman game you should make the following **request**:

    POST /hangman
Giving the following **response**:  

    {'my_word': my_word, 'lives': lives, 'letters_to_guess': letters_to_guess}

## Guess a letter
To guess a letter from the hidden word you should make the following **request**:

    PUT /hangman/guess/<string:letter>
This request will check several aspects: 

 - If you have enough lives to check another letter, if not, it will give the following **response**: 
   
       {'my_word': my_word, 'lives': lives,     'message': "no more lives, please make a request for a new word"}
 - If the input is correct, if not, it will give the following **response**: 
   
       {'my_word': my_word, 'lives': lives, 'message': "please type only one letter"}
       
 - If the letter has already been tried, if not, it will give the following **response**: 
   
       {'my_word': my_word, 'lives': lives, 'alphabet': alphabet), 'message': "letter already guessed" }
       
 - If the letter is a wrong solution, it will give the following **response**: 
   
       {'my_word': "".join(my_word), 'lives': lives, 'message': "letter not in word", 'letters_to_guess': letters_to_guess}
       
 - If the letter is a correct solution, it will give the following **response**:
   
       {'my_word': "".join(my_word), 'lives': lives, 'message': "letter found", 'letters_to_guess': letters_to_guess}
       
 - If the word got guessed, it will give the following **response**:
   
       {'word_to_guess': word_to_guess, 'my_word': my_word, 'lives': lives, 'message': "CONGRATULATION YOU FOUND THE HIDDEN WORD. YOU DESERVE A COOKIE"}

## Get status of game
To get the status of the current game, you should make the following **request**:

    GET /hangman/
Giving the following **response**:

    {'my_word': my_word, 'lives': lives, 'letters_to_guess': letters_to_guess, 'alphabet': alphabet}

   
## Get solution
To get the solution of the hangman game, you should make the following **request**:

    GET /hangman/solution
Giving the following **response**:  

    {'word_to_guess': word_to_guess, 'my_word': my_word}