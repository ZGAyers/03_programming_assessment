from tkinter import *
from functools import partial   # To prevent unwanted windows
import random
import re
import csv


# Class for Start GUI - so that user can setup initial parameters
class Start:
    # Displays Start GUI for user to setup game
    def __init__(self, parent):

        # GUI to get number of rounds
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Set initial balance to zero
        self.starting_rounds = IntVar()
        self.starting_rounds.set(0)

        # Quiz Heading (row 0)
        self.quiz_box_label = Label(self.start_frame, text="Country - Capital Game", font="Arial 19 bold")
        self.quiz_box_label.grid(row=0)

        # Quiz Box Description (row 1)
        self.quiz_instructions = Label(self.start_frame, text="Please enter the number of rounds "
                                                              "you would like to play (between 1-10) and "
                                                              "press the 'Start' button to play.", font="Arial 10 italic", wrap=275,
                                          justify=LEFT, padx=10, pady=10)
        self.quiz_instructions.grid(row=1)

        # Entry box and error frame (row 2)
        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=0, column=0)

        self.add_rounds_button = Button(self.entry_error_frame, font="Arial 14 bold", text="Check",
                                       command=self.check_rounds)
        self.add_rounds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon", text="", font="Arial 10 bold",
                                        wrap=275, justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # Play button and frame
        self.play_frame = Frame(padx=5, pady=5, width=200)
        self.play_frame.grid(row=3)

        self.play_button = Button(self.play_frame, text="Play", command=self.to_game,
                                        font="Arial 12 bold", bg="#87986a")
        self.play_button.grid(row=0, column=0, pady=10)

        # Disable play button at start
        self.play_button.config(state=DISABLED)

    # check rounds function - checks that the user entered a valid int for round setup
    def check_rounds(self):
        starting_rounds_set = self.start_amount_entry.get()

        # Set error background and colours (and assume no errors at the start)
        error_back = "#ffafaf"
        has_errors = "no"

        # Change background to white (fr testing purposes)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # If error disable button
        self.play_button.config(state=DISABLED)

        try:
            # set starting rounds
            starting_rounds_set = int(starting_rounds_set)

            # set boundaries for rounds entry
            if starting_rounds_set < 1:
                has_errors = "yes"
                error_feedback = "Sorry, the least amount of rounds you can play is 1"
            elif starting_rounds_set > 10:
                has_errors = "yes"
                error_feedback = "The most amount of rounds you can play is 10"

            # if user enters valid rounds
            else:
                self.play_button.config(state=NORMAL)
                self.add_rounds_button.config(state=DISABLED)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter an integer (not text or decimals)"

        # error display
        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)

        else:
            # set starting balance to amount entered by user
            self.starting_rounds.set(starting_rounds_set)
            self.start_amount_entry.config(bg="#b7e4c7")

    # to_game function - when game is setup sends user to start playing the game
    def to_game(self):
        starting_rounds_set = self.starting_rounds.get()

        Game(self, starting_rounds_set)

        # hide start up window
        root.withdraw()


# Class for Game GUI - so that user can play the game
class Game:
    # displays the Game GUI for game to then run
    def __init__(self, partner, starting_rounds):

        # make global variable for how manyy rounds
        global how_many_r
        # set as how many rounds user entered
        how_many_r = starting_rounds

        # initialise variables
        self.rounds = IntVar()

        # List for holding stats
        self.round_stats_list = []

        # List for holding stats
        # for game stats GUI:
        self.game_stats_list_l = [0]
        self.game_stats_list_w = [0]
        self.game_stats_b = [0]

        # For .txt file display:
        self.all_round_stats = []

        # GUI Setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # If user press cross at top, game quits
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)

        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # Heading Row
        self.heading_label = Label(self.game_frame, text="Country - Capital \nGame", font="Arial 24 bold",
                                   padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Instructions Label
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT,
                                        text="Guess the country's capital and "
                                             "see how many you can get "
                                             "correct!"
                                             " Punctuation does matter.")
        self.instructions_label.grid(row=1)

        # Country go here (row 2)

        # Set up country frame
        self.country_frame = Frame(self.game_frame)
        self.country_frame.grid(row=2, pady=10, padx=10)

        # Country question label
        self.country_q_label = Label(self.country_frame, text="Press Start to play", font="Arial 10 bold",
                                     wrap=275, justify=LEFT)
        self.country_q_label.grid(row=0, column=0, pady=5)

        # Country display label

        self.country_label = Label(self.country_frame, text="", font="Arial 18 bold",
                                   wrap=275, justify=LEFT)
        self.country_label.grid(row=2, pady=5)

        # Country flag display - might have to be moved to ccp function and have the display below
        self.country_p_label = Label(self.country_frame, image="",
                                     padx=10, pady=10)
        self.country_p_label.grid(row=1, column=0)

        # Capital goes here (row 3)
        self.capital_frame = Frame(self.game_frame)
        self.capital_frame.grid(row=3, pady=10, padx=10)

        self.capital_entry = Entry(self.capital_frame, font="Arial 15 bold")
        self.capital_entry.grid(row=0, column=0, ipady=10)

        # Check button goes here (row 3)
        self.check_button = Button(self.capital_frame, text="Check", bg="#8ecae6", font="Arial 15 bold",
                                   padx=5, pady=5, command=self.check)
        self.check_button.grid(row=0, column=1)
        # Disable check button before user starts game
        self.check_button.config(state=DISABLED)

        # Capital answer display (row 3)
        self.capital_answer = Label(self.game_frame, text="", font="Arial 10 bold",
                                    wrap=275, justify=LEFT)
        self.capital_answer.grid(row=4, pady=10)

        # Next button goes here (row 5)
        self.next_button = Button(self.game_frame, text="Start Game", bg="#adc178", font="Arial 15 bold",
                                  width=20, padx=10, pady=10, command=self.get_ccp)
        # grid setup of button
        self.next_button.grid(row=5)

        # Balance label (row 6)
        self.rounds_frame = Frame(self.game_frame)
        self.rounds_frame.grid(row=6, pady=10, padx=10)

        # Set up round display in Play GUI
        start_text = "Question: "

        self.rounds_label = Label(self.rounds_frame, font="Arial 12 bold", fg="#80b918",
                                  text=start_text)
        self.rounds_label.grid(row=0, column=0, pady=10)

        self.rounds1_label = Label(self.rounds_frame, font="Arial 12 bold", fg="#80b918", text="0")
        self.rounds1_label.grid(row=0, column=1, pady=10)

        # Help and Game Stats button (row 7)
        self.help_export_frame = Frame(self.game_frame, bg="#DDF0FF")
        self.help_export_frame.grid(row=7, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules", font="Arial 15 bold",
                                  bg="#f6bd60", fg="white", command=self.help)
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats", font="Arial 15 bold",
                                   bg="#468faf", fg="white", command=lambda: self.stats(self.game_stats_b[0], self.all_round_stats))
        self.stats_button.grid(row=0, column=1, padx=2)
        # Disable stats button
        self.stats_button.config(state=DISABLED)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#f07167", font="Arial 15 bold",
                                  width=20, command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=8, pady=10)

    # Game Stats section - sends user to Game Stats GUI
    def stats(self, game_stats, all_stats):
        get_stats = GameStats(self, game_stats, all_stats)

    # Help section - send user to Help GUI
    def help(self):
        get_help = Help(self)
        # get display help text to display in Help GUI
        get_help.help_text.configure(
            text="Press 'Start Game' to begin the first question of the game. A country and flag will be displayed and "
                 "a capital can then be entered into the entry field. \n\nPress 'Check' to check your answer and then "
                 "'Next' to begin the next question.\n\n To view your progress click the 'Game Stats' button to see how "
                 "many answers you've gotten correct. From there, if you wish, you can export your stats into a text "
                 "file where they will be displayed fully, round by round. \n\nGood Luck!")

    # retrieve information from csv file function for checking answer
    def get_ccp(self):

        # --- Configure display (below) ---

        # When user plays game, change label
        self.next_button.config(text="Next")
        # Disable next button
        self.next_button.config(state=DISABLED)
        # enable check button
        self.check_button.config(state=ACTIVE)

        # Change background to white
        self.capital_entry.config(bg="white")
        # clear capital answer
        self.capital_answer.config(text="")

        # clear entry box field
        self.capital_entry.delete(0, 'end')
        # change question label
        self.country_q_label.config(text="What is the capital of: ")

        # add rounds when next button is clicked
        global get_rounds
        #  make variable self.rounds list
        get_rounds = self.rounds.get()

        # add a round
        get_rounds += 1
        # set to self.rounds as next round
        self.rounds.set(get_rounds)

        # display round
        self.rounds1_label.config(text=get_rounds)

        # Open csv file and get provided information
        with open("00_country_capital.csv") as f:
            reader = csv.reader(f)
            reader = list(reader)

            # deletes first row in csv file
            del reader[0]

            # get randomised country, capital and image
            randomised_reader = random.choice(reader)

            # Split into variables
            global country
            # get country to display
            country = randomised_reader[0]
            # get the correct capital answer
            global capital_ans
            capital_ans = randomised_reader[1]
            # get the image file name
            image_file = randomised_reader[2]

            # -- Display for game --

            # Country label
            self.country_label.config(text=country)

            # Display image
            photo = PhotoImage(file=image_file)
            self.country_p_label.config(image=photo)
            self.country_p_label.photo = photo

    # Check user input function - views user input and returns whether ans = correct or incorrect
    def check(self):
        # Disable stats button
        self.stats_button.config(state=NORMAL)
        # Get capital from above function
        get_capital_answer_lo = capital_ans.lower()

        # get user input
        capital_guess = self.capital_entry.get().lower()  # ***for error testing this code works***

        # create global variable for loss and won
        global won
        global loss

        # make global variables have int
        won = 0
        loss = 0

        # error setup
        error_back = "#ffafaf"
        has_errors = "no"

        # -- Error types below --

        capital_guess = str(capital_guess)
        # if left blank
        if capital_guess == "":
            # Disable stats button
            self.stats_button.config(state=DISABLED)
            has_errors = "yes"
            error_feedback = "Please do not leave this field blank.\nHINT: The capital starts with the " \
                             "letter '{}'".format(capital_ans[0])

        # if guess is incorrect
        elif capital_guess != get_capital_answer_lo:
            # get loss
            loss = self.game_stats_list_l[0]
            loss += 1
            self.game_stats_list_l[0] = loss

            # disable check button
            self.check_button.config(state=DISABLED)
            # change entry background
            self.capital_entry.config(bg=error_back)

            # if there are rounds left
            if get_rounds != how_many_r:
                # enable next button
                self.next_button.config(state=NORMAL)

                # user answer feedback
                self.capital_answer.config(text="Incorrect! The capital is {}".format(capital_ans))

            # if there are no rounds left
            else:
                # user answer feedback
                self.capital_answer.config(text="Incorrect! The capital is {}.\n\n"
                                                "Game Over! Click Game Stats to view your game "
                                                "statistics".format(capital_ans))

        # if guess is correct
        else:
            # get won
            won = self.game_stats_list_w[0]
            won += 1
            self.game_stats_list_w[0] = won

            # change bg to green in entry box
            self.capital_entry.config(bg="#CAFFBF")
            # disable check button
            self.check_button.config(state=DISABLED)

            #  if there are rounds left
            if get_rounds != how_many_r:
                # enable next button
                self.next_button.config(state=NORMAL)

                # user answer feedback
                self.capital_answer.config(text="Correct!")

            # if there are no rounds left
            else:
                # user answer feedback
                self.capital_answer.config(text="Correct!\n\n"
                                                "Game Over! Click Game Stats to view your game "
                                                "statistics")

        # if user enters an invalid string
        if has_errors == "yes":
            self.capital_entry.config(bg=error_back)
            self.capital_answer.config(text=error_feedback)

        # Get Game Stats
        # set up for percentage correct label
        # if a round has been won run this code
        if self.game_stats_list_w[0] != 0:
            # get percentage (in decimal)
            percentage = self.game_stats_list_w[0] / get_rounds
            # get percentage (in percentage)
            percentage2 = percentage * 100
        # if no rounds won
        else:
            percentage2 = 0

        # Output setup for stats GUI
        display_game_stats = "Questions Answered: {} \n" \
                             "Questions Correct: {} \n" \
                             "Questions Incorrect: {} \n" \
                             "Percentage Correct: {:.2f}% \n".format(get_rounds, self.game_stats_list_w[0],
                                                         self.game_stats_list_l[0], percentage2)

        self.game_stats_b[0] = display_game_stats

        # Get all Game Stats - for Export .txt file display
        all_game_stats_write = "Round {}: {} - User Answer: '{}'  Correct Answer" \
                               ": {}".format(get_rounds, country, capital_guess, capital_ans)

        self.all_round_stats.append(all_game_stats_write)

    # quit game - quits and destroys the game box
    def to_quit(self):
        root.destroy()


# Help GUI - So that user can view help frame and understand what to do
class Help:
    #  Help GUI display setup
    def __init__(self, partner):
        background = "#fbc4ab"

        # disable help button
        partner.help_button.config(state=DISABLED)

        # Sets up child window (ie: help box)
        self.help_box = Toplevel()

        # If users press the cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Set up GUI Frame

        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.grid()

        # Set up Help Heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions", font="arial 14 bold",
                                 bg=background)
        self.how_heading.grid(row=0)

        # Help text (label, row 1)
        self.help_text = Label(self.help_frame, text="", justify=LEFT, width=40, bg=background,
                               wrap=250)
        self.help_text.grid(column=0, row=1)

        # Dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10, bg="#f4978e",
                                  font="arial 10 bold", command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    # closes the help box when user quits
    def close_help(self, partner):
        # Put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# Game Stats GUI - So that user can view their game progress
class GameStats:
    # Set up Game Stats GUI and display stats
    def __init__(self, partner, game_stats, all_stats):
        background = "#c6def1"

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # Sets up child window (ie: stats box)
        self.stats_box = Toplevel()

        # If users press the cross at top, closes help and 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # Set up GUI Frame

        self.stats_frame = Frame(self.stats_box, bg=background)
        self.stats_frame.grid()

        # Set up Stats Heading (row 0)
        self.stats_heading = Label(self.stats_frame, text="Game Statistics", font="arial 14 bold", bg=background)
        self.stats_heading.grid(row=0)

        # Stats text (label, row 1)
        self.stats_info_text = Label(self.stats_frame, text="Below are your game statistics for your played games. "
                                                            "If you want to view your full stats 'Export' your "
                                                            "statistics "
                                                            "into a file.", justify=LEFT, width=40, bg=background,
                                     wrap=250)
        self.stats_info_text.grid(column=0, row=1)

        # set up display stats frame (row 2)
        self.displays_frame = Frame(self.stats_frame, bg=background)
        self.displays_frame.grid(row=2)

        # Display stats (rounds, won and lost)
        self.stats_display = Label(self.displays_frame, text=game_stats, bg=background, wrap=250,
                                   font="arial 12 bold")
        self.stats_display.grid(row=0)

        # set up button frame (row 3)
        self.button_frame = Frame(self.stats_frame, bg=background)
        self.button_frame.grid(row=3)

        # Export Button (row 0, column 0)
        self.export_btn = Button(self.button_frame, text="Export", width=10, bg="#c9e4de", font="arial 10 bold",
                                 command=lambda: self.exp(game_stats, all_stats))
        self.export_btn.grid(row=0, column=0, padx=10)

        # Dismiss button (row 0, column 1)
        self.dismiss_btn = Button(self.button_frame, text="Dismiss", width=10, bg="#f9c6c9",
                                  font="arial 10 bold", command=partial(self.close_stats, partner))
        self.dismiss_btn.grid(row=0, column=1, pady=10)

    # sends user to Export class to be able to export stats
    def exp(self, game_stats, all_stats):
        get_export = Export(self, game_stats, all_stats)

    # closes the stats box when user quits
    def close_stats(self, partner):
        # Put help button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# Export section - So that user can export their stats if wanted
class Export:
    # Displays Export GUI so that user can export their stats
    def __init__(self, partner, game_stats, all_stats):

        # Disable export button
        partner.export_btn.config(state=DISABLED)

        # Sets up child window (ie: export box)
        self.export_box = Toplevel()

        # If users press cross at top, closes export and 'releases' export button
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

        # Set up GUI frame
        self.export_frame = Frame(self.export_box, width=300)
        self.export_frame.grid()

        # Set up export heading (row 0)
        self.how_heading = Label(self.export_frame, text="Export / Instructions", font="arial 14 bold")
        self.how_heading.grid(row=0)

        # Export Instructions (label, row 1)
        self.export_text = Label(self.export_frame, text="Enter a filename in the box below and press the "
                                                         "Save button to save your quiz history to "
                                                         "text file.", justify=LEFT, width=40, wrap=250)
        self.export_text.grid(row=1)

        # Warning text (label, row 2)
        self.export_text = Label(self.export_frame, text="If the filename you enter below already exists, "
                                                         "its contents will be replaced with your quiz "
                                                         "history", justify=LEFT, bg="#ffafaf", fg="maroon",
                                 font="Arial 10 italic", wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)

        # Filename Entry Box (row 3)
        self.filename_entry = Entry(self.export_frame, width=20, font="Arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        # Error Message Labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon")
        self.save_error_label.grid(row=4)

        # Save / Cancel Frame (row 5)
        self.save_frame = Frame(self.export_box)
        self.save_frame.grid(row=5, pady=10)

        # Save and Cancel Buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_frame, text="Save", width=10, font="Arial 10 bold", bg="#A7B690",
                                  fg="black", padx=10,
                                  command=partial(lambda: self.save_history(partner, game_stats, all_stats)))
        self.save_button.grid(row=0, column=1, padx=10)

        # Cancel button (row 0, column 1)
        self.cancel_btn = Button(self.save_frame, text="Cancel", width=10, bg="#f9c6c9",
                                 font="arial 10 bold", command=partial(self.close_exp, partner))
        self.cancel_btn.grid(row=0, column=2, pady=10)

    # closes export frame if user closes the box
    def close_exp(self, partner):
        # Put stats button back to normal...
        partner.export_btn.config(state=NORMAL)
        self.export_box.destroy()

    # checks user enters valid file name and if yes exports the file
    def save_history(self, partner, game_stats, all_stats):

        # assign problem variable
        problem = ""

        # Regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"

        filename = self.filename_entry.get()

        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "(No spaces allowed)"

            else:
                problem = ("(No {}'s allowed)".format(letter))
            has_error = "yes"
            break

        if filename == "":
            problem = "File name can't be blank"
            has_error = "yes"

        if has_error == "yes":
            self.filename_entry.config(bg="#ffafaf")
            self.save_error_label.config(text="Invalid Name: {}".format(problem))

        else:
            # If there are no errors, generate text filename and then close dialogue
            # add .txt suffix
            filename = filename + ".txt"

            # Create file to hold data
            f = open(filename, "w+")

            # Heading for stats
            f.write("**Game Statistics**\n\n")

            # Game stats
            f.write(game_stats)

            # Heading for Rounds
            f.write("\nRound Details:\n\n")

            # Add new line at end of each item
            for item in all_stats:
                f.write(item + "\n")

            # close file
            f.close()

            # close dialogue
            self.close_export(partner)

    # closes the export frame when user enters valid file name and exports stats
    def close_export(self, partner):
        # Put export button back to normal...
        partner.export_btn.config(state=NORMAL)
        self.export_box.destroy()


# main routine - runs game
if __name__ == "__main__":
    root = Tk()
    root.title("Country - Capital Game")
    something = Start(root)
    root.mainloop()
