import argparse
import sys

from collections import defaultdict
from os import system
from pathlib import Path
from random import randint

QUIT = 'q'

def main():
    # Clear the terminal, print welcome, run game
    system('clear')
    print('\n' + "~WELCOME TO MASTERMIND. PRESS Q AT ANY TIME TO QUIT~" + '\n')
    game = Game()
    game.run_until_finished()

def check_quit(input_var):
    if input_var.casefold() == QUIT:
        system('clear')
        quit()


class Game():

    def __init__(self, mode='auto', easy=False):
        self.mode = mode
        self.easy = easy
        self.word_list = []
        self.num_guesses = 0
        self.correct_word = None

        # CLI args can be used to turn on manual mode or make the game easier
        parser = argparse.ArgumentParser(description='Plays a game of Mastermind.')
        parser.add_argument('--manual', dest='manual', action='store_true', required=False)
        parser.add_argument('--easy', dest='easy', action='store_true', required=False)
        args = parser.parse_args()

        if args.manual:
            self.mode = 'manual'
        
        if args.easy:
            self.easy = True

    def import_words(self):
        word_length = 0

        while word_length < 1 or self.num_guesses < 1:
            try:
                word_length = input("How long would you like the words to be? ")
                check_quit(word_length)

                self.num_guesses = input("How many guesses should the player get? ")
                check_quit(self.num_guesses)

                word_length = int(word_length)
                self.num_guesses = int(self.num_guesses)
                assert word_length > 0 and self.num_guesses > 0

            except EOFError:
                system('clear')
                quit()

            except Exception:
                print()
                print("Word length and number of guesses must be positive integers. "
                      "Please re-enter." +'\n')
                word_length = 0
                self.num_guesses = 0

        # Manual mode allows for 2 players to play a game together...or perhaps more?
        if self.mode == 'manual':
            word = None
            print('\n' + "Enter words to guess from one at a time." + '\n'
                "Words should be the same length." + '\n'
                "Press ENTER without entering a new word when you're done." + '\n')
            while word != '' or self.word_list == []:
                try:
                    word = input("New word (ENTER to finish): ").lower()
                    check_quit(word)

                    if word == '' and self.word_list != []:
                        print()
                        break

                    if word == '' and self.word_list == []:
                        print("You can't play without picking some words first. "
                              "Please re-enter." + '\n')

                    if word in self.word_list:
                        print("Why don't you try picking a new word instead?")

                    elif len(word) == word_length:
                        self.word_list.append(word)

                    elif len(word) != word_length:
                        print(f"Words must be {word_length} characters long. "
                               "Please re-enter." + '\n')

                except EOFError:
                    system('clear')
                    quit()

            while self.correct_word == None:
                response = input('Which word is the secret password? ')
                check_quit(response)

                self.correct_word = response if response in self.word_list else None
                if self.correct_word == None:
                    print("Please select one of the words to be the secret password." + '\n')

        # Auto is the default game mode for 1 player
        if self.mode == 'auto':
            try:
                num_words = input("How many random words should I pick? ")
                check_quit(num_words)

                num_words = int(num_words)
                assert num_words > 0

            except EOFError:
                system('clear')
                quit()

            except Exception:
                print("Number of words must be a positive integer. Please re-enter." +'\n')

            # Words are chosen at random from words.txt in the same directory
            word_dict = defaultdict(list)
            with open(Path.cwd().joinpath("words.txt"), "r") as source:
                for word in source:
                    word_dict[len(word.strip())].append(word.strip())

            try:
                # Using '_' for unreferenced generic vars is a Scala habit,
                # Not sure if this is considered "best practice" in Python
                for _ in range(num_words):
                    possible_words = word_dict[word_length]
                    self.word_list.append(
                        possible_words[randint(0,len(possible_words))]
                        )

                self.correct_word = self.word_list[randint(0, len(self.word_list)-1)]

            # IndexError happens when Mastermind can't find enough words of a
            # given length in words.txt
            except IndexError:
                print()
                print("Sorry, I couldn't find enough words of that length. "
                      "Let's start over." + '\n')
                self.import_words()

        system('clear')

    def game_loop(self):
        game_over = False

        # If failure is impossible, does victory mean anything?
        challenging = True if self.num_guesses < len(self.word_list) else False

        # Game opening script
        print("~PRESS Q AT ANY TIME TO QUIT~" + '\n'*2 +
              "Alright! Let's play!" + '\n'*2 +
             f"Your opponent has selected {len(self.word_list)} words, and they are: " + '\n')

        # Print words to guess from
        [print(word.upper()) for word in self.word_list]

        if self.easy == True:
            print('\n' + "Only one is the secret password, all the rest are fakes." + '\n' +
                  "Each time you make a guess, I'll tell you which letters you got right! " +
                  "Pretty easy, huh?" + '\n')
        
        else:
            print('\n' + "Only one is the secret password, all the rest are fakes." + '\n' +
                  "Each time you make a guess, I'll tell you how many letters you got right " +
                  "(but not which ones)!" + '\n')
        
        while not game_over:
            try:
                guess = input(f"Take a guess? ({self.num_guesses} remaining) \n").casefold()
                check_quit(guess)

            except EOFError:
                system('clear')
                quit()

            print()
            if guess not in self.word_list:
                print("Oh come on! The words are right in front of you! Pick one!" + '\n')

            elif guess == self.correct_word:
                game_over = True
                # Looks like you found an easter egg ;)
                if self.correct_word.casefold() == 'beijing':
                    print("哇塞~ 你果然看了我写的代码！太高兴了！那我就跟你开门见山地讲："
                    "你就是我喜欢的那种老板！我们合作吧！" + '\n')
                elif challenging:
                    print("Wow, you're good at this! You beat the Mastermind "
                         f"with {self.num_guesses-1} guess(es) remaining!" + '\n')
                else:
                    print("Well, you won, but was it really even a challenge? "
                          "Why don't you try again with fewer guesses allowed." + '\n')

                print("This game was made by Bill Edwards (bill@popstack.io). "
                      "If your playthrough was fun and bug-free, "
                      "you should really think about hiring him! :)")

            else:
                correct_letters = []
                correct_count = 0

                for i in range(len(self.correct_word)):
                    correct_letters.append(
                        self.correct_word[i] if guess[i] == self.correct_word[i] else '_'
                        )
                    correct_count += 1 if guess[i] == self.correct_word[i] else 0

                if self.easy == True:
                    print("Not quite, but here's what you got correct: "
                         f"{''.join(correct_letters)}" + '\n')
                else:
                    print("Oh no! That wasn't it! You only got "
                         f"{correct_count}/{len(self.correct_word)} "
                          "letter(s) correct!" + '\n')

                self.num_guesses -= 1
                if self.num_guesses <= 0:
                    game_over = True
                    if challenging:
                        print("The secret password was "
                             f"{self.correct_word.upper()}. Better luck next time!")
                    else:
                        print("The secret password was "
                             f"{self.correct_word.upper()}. How did you lose? "
                              "Did you forget which words you already guessed?")

        print('\n' + "GAME OVER" + '\n')
        play_again = None
        while play_again != 'y' and play_again != 'n':
            try:
                play_again = input("Play again? y/n ")
                check_quit(play_again)

            except EOFError:
                system('clear')
                quit()

            if play_again.casefold() == 'y':
                main()
            elif play_again.casefold() == 'n':
                system('clear')
                quit()

    def run_until_finished(self):
        self.import_words()
        self.game_loop()


if __name__ == "__main__":
    main()