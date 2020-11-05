import random
import re

dictionary = {}
hs_file = "highscore.txt"
word_file = "memo.txt"


class MemoryGame:
    """
    Attributes:
    user: The user's name (a string)
    size: The size of the A x A matrix (an integer)
    list_of_words: All the words in the file (a list)
    words_for_game: The words used in the game (a list)
    board: The A x A matrix (lists within a list)
    """

    def __init__(self, user, size):
        """
        Creates the memory game
        :param user: The user's name (a string)
        :param size: The size of the A x A matrix (an int)
        """

        self.user = user
        self.size = size
        self.list_of_words = []
        self.words_for_game = []
        self.board = []

    def get_words_from_file(self, file_name):
        """
        Used to get words from file and to create a randomly shuffled list.
        where each line in the file is an object in the list.
        :return: Shuffled list of words
        """

        file = open(file_name, "r")

        # Strips each line off of whitespaces and adds them to the list

        for line in file.readlines():
            stripped_line = line.strip("\n")
            self.list_of_words.append(stripped_line)
        file.close()

        # Shuffles all items in the list

        random.shuffle(self.list_of_words)
        return self.list_of_words

    def create_list_for_game(self):
        """
        Creates a list with the right amount of words, each word appearing
        twice.
        :return: A list of words.
        """

        # Calculates the amount of items (words) needed in game

        amount_of_cards = self.size * self.size
        amount_of_words = int(amount_of_cards / 2)

        # Appends the right amount of items (words) to a list, twice.

        for word in range(0, amount_of_words):
            for times in range(2):
                self.words_for_game.append(self.list_of_words[word])

        # Shuffles the items in the list

        random.shuffle(self.words_for_game)

        return self.words_for_game

    def dictionary_for_game(self, words_for_game):
        """
        Creates a dictionary with positions as keys and
        the words used in the game as values.
        :param words_for_game: Shuffled list of words
        :return: A dictionary
        """

        # Creates the right amount of keys

        for row in range(0, self.size):
            column_number = 0
            for column in range(0, self.size + 1):
                # Calling the keys A0, A1, A2, ..., B0, B1, B2, ...
                row_letter = chr(row + 65)
                dictionary[row_letter + str(column_number)] = []
                column_number += 1

        # Creates the values

        for key in dictionary:
            # Does not add value to keys with a 0 in the key name
            if "0" in key:
                pass
            else:
                # Adds the last element (a word) in the list of words
                # Removes the element from the list so that it isn't added twice
                dictionary[key] = words_for_game.pop()

        return dictionary

    def create_board(self):
        """
        Used to get words from a list (the amount corresponding with the
        user’s choice), putting them into a board (an A x A matrix).
        :return: A x A matrix
        """

        # Creates right amount of columns

        for row in range(0, self.size + 1):
            self.board.append([])

        # Creates right amount of rows

            for column in range(0, self.size + 1):
                # in each row you have to append "size" number of elements
                self.board[row].append(column)

                # Creates blank left corner

                if row == 0 and column == 0:
                    self.board[row][column] = "  "

                # Creates column numbers

                elif row == 0 and column != 0:
                    self.board[row][column] = str(column) + "  "

                # Creates row numbers

                elif row != 0 and column == 0:
                    self.board[row][column] = chr(row + 64)

                # All other positions in matrix are "---"

                else:
                    self.board[row][column] = "---"

    def reveal_card(self, choice, coordinates):
        """
        Used to print a word in a given position in the board
        :param choice: The user's choice (A string)
        :param coordinates: A list with two items corresponding with the
        position of a card
        :return: nothing
        """
        row = coordinates[0]
        column = coordinates[1]
        self.board[row][column] = dictionary[choice]
        display_board(self.board)

        return

    def hide_card(self, coordinates):
        """
        Used to print --- in a given position in the board
        :param coordinates: A list with two items corresponding with the
        position of a card
        :return: nothing
        """
        row = coordinates[0]
        column = coordinates[1]
        self.board[row][column] = "---"

        return


# FUNCTIONS

def get_int_input(prompt_string):
    """
    Used to get an int from the user, asks again if input is not if not divisible by 2
    convertible to int and/or
    :param prompt_string: the string explaining what to input
    :return: the int that was asked for
    """

    done = False

    int_error = "You need to enter a valid number, for example 4. Try again!"
    odd_error = "You need to enter an even number. Try again!"

    while not done:

        # Checks if input is an integer
        try:
            number = int(input(prompt_string))
        except ValueError:
            print(int_error)
            print("")
            continue

        # Checks if number is even (divisible by two)
        try:
            if number % 2 != 0:
                raise ValueError()
            else:
                done = True
        except ValueError:
            print(odd_error)
            print("")
            continue

        else:
            return number


def display_board(board_to_print):
    """
    Used to display the board:

    Welcome to the memory game!
    Choose the A x A size of your game:
    ==============================
        1   2   3   4   5   6
    A --- --- --- --- --- ---
    B --- --- --- --- --- ---
    C --- --- --- --- --- ---
    D --- --- --- --- --- ---
    E --- --- --- --- --- ---
    F --- --- --- --- --- ---
    ==============================
    Your move:
    ==============================
        1   2   3   4   5   6
    A --- --- --- hej --- ---
    B --- --- --- --- --- ---
    C --- kul --- --- --- ---
    D --- --- --- --- --- ---
    E --- --- --- --- --- ---
    F --- --- --- --- --- ---
    ==============================
    Your move:

    :param board_to_print: The A x A matrix
    :return: nothing
    """
    for row in range(0, len(board_to_print)):
        for column in range(len(board_to_print[row])):
            print(board_to_print[row][column], end=" ")
        print("")

    print("==============================")
    return board_to_print


def get_users_move():
    """
    Used to get input on which card the user wants to flip, asks again
    if input is not exactly one number and one letter.
    :return: A str corresponding with the users choice, in the format
    A1 or B3
    """

    number = ""
    letter = ""

    # We use a boolean variable to make sure we don't return the str
    # until we know it contains exactly one letter and one number

    valid_choice = False

    length_error = "Your entry should contain two characters. Try again!"
    int_error = "You need to choose a column number. Try again!"
    letter_error = "You need choose a row letter. Try again!"

    while not valid_choice:
        choice = input("Your move: ")

        # Checks if input contains two elements

        while len(choice) != 2:
            print(length_error)
            print("")
            choice = input("Your move: ")

        # Checks if one of the elements in the input is an integral.
        # If it can't find an int, 'number' continues to be an empty str
        # If it finds an int, 'number' becomes an int - that number

        for element in range(2):
            try:
                number = int(choice[element])
            except ValueError:
                number: ""

        # Checks if the length of the number-part of the input is 1
        # Prints error if it isn't, and goes back to the beginning of the loop again

        if len(str(number)) != 1:
            print(int_error)
            print("")

        # Now we know we have one (and only one) number
        # Now we check for letters a-Z in the same way

        else:
            # Removes anything that's not a character of type a-zA-Z (a letter)
            letter = re.sub('[^a-zA-Z]+', '', choice)
            # Checks that the length of the remaining part of the input is 1
            if len(letter) != 1:
                print(letter_error)
                print("")

            # Now we know that we have exactly one number and one letter
            # Now we can finally set valid_choice to True

            else:
                valid_choice = True

    # We return the choice as a str, for example: A1

    choice = letter + str(number)
    choice = choice.upper()
    print("Your move is: " + choice)
    print("==============================")

    return choice


def convert_users_move(choice):
    """
    Converts users move into a list
    :param choice:
    :return: A list [1, 1] which can be used as card coordinates
    """
    coordinates = []

    letter = choice[0]
    letter_position = ord(letter) - 64
    coordinates.append(letter_position)

    number = int(choice[1])
    coordinates.append(number)

    return coordinates


def initialize_game():
    """
    Used to initialize the game
    :return: nothing
    """
    print("")
    print("Welcome to the memory game!")
    print("==============================")
    user = input("Enter your name: ")
    size = get_int_input("The board is an A x A square. Enter a value for A: ")

    print("")
    print("You chose a", size, "x", size, "board. Let's play!")
    print("==============================")

    memory = MemoryGame(user, size)
    words = memory.words_for_game
    board = memory.board

    # Reads in all the words in the given memo file

    memory.get_words_from_file(word_file)

    # Creates a new list with the right amount of words from the wordlist

    memory.create_list_for_game()

    # Makes a dictionary for the game

    memory.dictionary_for_game(words)

    # Creates a memory board

    memory.create_board()

    # Prints the memory board

    display_board(board)

    # Plays game

    play_game(memory, board, user)

    return


def play_game(memory, board, user):
    """
    Used to play the game
    :return: nothing
    """

    done = "---" not in str(board)
    moves = 0
    matches = 0

    while not done:

        # Reveals the first card

        choice1 = get_users_move()
        memory.reveal_card(choice1, convert_users_move(choice1))

        # Reveals the second card

        choice2 = get_users_move()
        memory.reveal_card(choice2, convert_users_move(choice2))

        # Checks that the user doesn't choose the same card twice
        # This error-handling is not ready yet

        if choice2 == choice1:
            print("You can't choose the same card twice. Please choose another one.")

        else:

            # Hides the cards if they don't match

            if dictionary[choice1] != dictionary[choice2]:
                print("Nope, that's not a match. Try again!")
                memory.hide_card(convert_users_move(choice1))
                memory.hide_card(convert_users_move(choice2))
                moves += 1

            # Breaks the loop (stops the game) if all cards have a match

            elif "---" not in str(board):
                moves += 1
                break

            # Keeps revealing cards that match

            else:
                moves += 1
                matches += 1
                print("Waaae, That's", matches, "match(es)! Keep going.")
                pass

    print("Look at you,", user + "!", "You finished the game in only", moves, "moves!")
    print("Good Job!")
    print("")

    # Saves user's name and score to a file

    save_score_to_file(moves, user, hs_file)

    return


def save_score_to_file(moves, user, file_name):
    """
    Used to write user's name and score to a file
    :return: A list of all scores
    """

    # Adds score to list

    fw = open(file_name, "a")  # open to writing w/ stream at the end of the file
    fw.writelines("\n" + str(str(moves) + ";" + user))
    fw.close()

    # Puts scores into a list

    all_scores = []

    fr = open("highscore.txt", "r")
    for line in fr.readlines():
        stripped_line = line.strip("\n")
        all_scores.append(stripped_line)
    fr.close()

    # Sorts list

    all_scores.sort()

    # Prints all the scores

    print_scores(all_scores)


def print_scores(all_scores):
    """
    Used to print all the high scores.
    :param all_scores: A list containing all the scores (a list)
    :return: A string containing moves and score
    """
    print("Highscores: ")
    for score in all_scores:
        score = "Moves: " + str(score).replace(";", "  User: ")
        print(score)


initialize_game()
