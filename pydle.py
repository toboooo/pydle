import os
import csv
import pickle
import random
import tkinter
from tkinter import ttk
from tkinter import *

# Callback function bound to the return key.
def input_callback(*args):
	global attempt
	global letters
	global word_entry
	# Check if number of allowed attempts has not been reached and the input is
	# allowed.
	guess = word_var.get().lower().strip(" ")
	# Count frequencies of letters in answer word.
	answer_counts = {letter: answer_word.count(letter) for letter in set(answer_word)}
	if attempt <= 5 and guess in allowed_words:
		# Create a temporary list of letters to keep track of which have been
		# marked.
		marked_letters = list(guess)
		seen_letters = []
		# Green pass to mark all letters in the right place
		for i, letter in enumerate(guess):
			# Also initialise the text box whilst we are here
			word_attempts[attempt][i].config(text=letter.upper())
			# Mark the letter green if it is in the right place
			if letter == answer_word[i]:
				word_attempts[attempt][i].config(foreground="#5ceb1a")
				marked_letters[i] = "-"
				seen_letters.append(letter)
			# Remove the letter from the string of untried letters
			try:
				letter_index = letters.index(letter.upper())
				letters = letters[:letter_index] + " " + letters[letter_index+1:]
			except ValueError:
				continue
		# Orange pass to mark letters that are in the word, but are not in the
		# right place.
		for i, letter in enumerate(marked_letters):
			# Skip if already marked.
			if letter == "-":
				continue
			elif letter in answer_word:
				if seen_letters.count(letter) < answer_counts[letter]:
					word_attempts[attempt][i].config(foreground="#eba21a")
					seen_letters.append(letter)
			# Remove the letter from the string of untried letters
			try:
				letter_index = letters.index(letter.upper())
				letters = letters[:letter_index] + " " + letters[letter_index+1:]
			except ValueError:
				continue
		untried_letters.config(text=letters)
		attempt += 1

	# Collect stats if correct.
	if guess == answer_word:
		stats["n_wins"] += 1
		stats["attempt_distribution"][attempt-1] += 1
		stats["score_sum"] += attempt
		# Pickle the stats
		stats_file = open("stats_pydle.pkl", "wb")
		pickle.dump(stats, stats_file)
		stats_file.close()
		word_entry.config(state="disabled")
		root.unbind("<Return>")
	elif attempt > 5:
		print("Answer:", answer_word)
		word_entry.config(state="disabled")
		root.unbind("<Return>")

	# Clear the text box after finished with word_var.
	word_entry.delete(0, END)

# Function to create the popup window for stats
def popup_window():
	stats_window = tkinter.Toplevel()
	stats_text = "Number of plays: " + str(stats["n_plays"]) + "\n" + \
				"Number of wins: " + str(stats["n_wins"]) + "\n" + \
				"Mean score: " + str(round(stats["score_sum"] / stats["n_wins"], 2) if stats["n_wins"] != 0 else 0) + "\n"
	for i in range(6):
		if sum(stats["attempt_distribution"]) == 0:
			stats_text += str(i+1) + " attempts: 0%\n"
		else:
			stats_text += str(i+1) + " attempts: " + str(int(round(stats["attempt_distribution"][i] / sum(stats["attempt_distribution"]) * 100))) + "%\n"
	stats_label = ttk.Label(stats_window, font=("Arial 12"), text=stats_text)
	stats_label.grid(column=0, row=2)
	# Pad everything in the stats window
	for child in stats_window.winfo_children():
		child.grid_configure(padx=5, pady=5)

# Function to reset the game after it is complete
def reset_game():
	stats["n_plays"] += 1
	global root
	global main_frame 
	global input_frame
	global words_frame
	global word_var
	global word_entry
	global untried_letters
	global word_attempts
	global stats_button
	global attempt
	global answer_word
	global letters
	# Choose a new answer
	answer_word = random.choice(answers)
	# Reset number of attempts
	attempt = 0

	# Destroy all current widgets
	for child in root.winfo_children():
		child.destroy()
	
	# Create frame widget to hold GUI contents.
	main_frame = ttk.Frame(root, padding="3 3 12 12")
	main_frame.grid(column=0, row=0, sticky=(N,W,E,S))
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)

	# Create a separate frame for the input box and letter tracking.
	input_frame = ttk.Frame(main_frame)
	input_frame.grid(column=0, row=1)
	# Make the entry text box.
	word_var = StringVar()
	word_entry = ttk.Entry(input_frame, font=("Arial 30"), width=6, textvariable=word_var)
	word_entry.grid(column=2, row=7)

	# Make a widget for the list of letters.
	letters = "Q W E R T Y U I O P\n  A S D F G H J K L\n    Z X C V B N M"
	untried_letters = ttk.Label(input_frame, font=("Arial 22"), text=letters)
	untried_letters.grid(column=2, row=8)

	# Create a new frame for the letters.
	words_frame = ttk.Frame(main_frame)
	words_frame.grid(column=0, row=0)
	# Make the label objects that will contain the letters of the words.
	# Five labels per word in a row, by six words
	word_attempts = []
	for i in range(6):
		letter_attempts = []
		for j in range(0, 5):
			letter_attempt = ttk.Label(words_frame, font=("Arial 30"), text="")
			letter_attempt.grid(column=j, row=i+1)
			letter_attempts.append(letter_attempt)
		word_attempts.append(letter_attempts)

	# Some formatting.
	for child in main_frame.winfo_children():
		child.grid_configure(padx=5, pady=5)

	# Reset button.
	reset_button = ttk.Button(input_frame, text="Reset", command=reset_game)
	reset_button.grid(column=2, row=9)

	# The button to show stats
	stats_button = ttk.Button(input_frame, text="Stats", command=popup_window)
	stats_button.grid(column=2, row=10)

	# Rebind return key
	root.bind("<Return>", input_callback)


if __name__ == "__main__":
	# Load in stats, create the stats dictionary if no file
	if os.path.exists("./stats_pydle.pkl"):
		stats_file = open("stats_pydle.pkl", "rb")
		stats = pickle.load(stats_file)
		stats["n_plays"] += 1
		stats_file.close()
	else:
		stats = {"n_plays": 1, "n_wins": 0, "score_sum": 0,
				"attempt_distribution": [0,0,0,0,0,0]}

	# Get the word dictionaries.
	with open("wordle_dicts.csv") as file:
		dicts = list(csv.reader(file))
		file.close()
	answers, allowed_words = dicts[0], set(dicts[1])
	for answer in answers:
		allowed_words.add(answer)

	# Select a random word as the answer
	answer_word = random.choice(answers)

	# Initialise the number of attempts
	attempt = 0

	# Make the game gui.
	root = tkinter.Tk()
	root.title("Wordle in Python")

	# Create frame widget to hold GUI contents.
	main_frame = ttk.Frame(root, padding="3 3 12 12")
	main_frame.grid(column=0, row=0, sticky=(N,W,E,S))
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)

	# Create a separate frame for the input box and letter tracking.
	input_frame = ttk.Frame(main_frame)
	input_frame.grid(column=0, row=1)
	# Make the entry text box.
	word_var = StringVar()
	word_entry = ttk.Entry(input_frame, font=("Arial 30"), width=6, textvariable=word_var)
	word_entry.grid(column=2, row=7)

	# Make a widget for the list of letters.
	letters = "Q W E R T Y U I O P\n  A S D F G H J K L\n    Z X C V B N M"
	untried_letters = ttk.Label(input_frame, font=("Arial 22"), text=letters)
	untried_letters.grid(column=2, row=8)

	# Create a new frame for the letters.
	words_frame = ttk.Frame(main_frame)
	words_frame.grid(column=0, row=0)
	# Make the label objects that will contain the letters of the words.
	# Five labels per word in a row, by six words
	word_attempts = []
	for i in range(6):
		letter_attempts = []
		for j in range(0, 5):
			letter_attempt = ttk.Label(words_frame, font=("Arial 30"), text="")
			letter_attempt.grid(column=j, row=i+1)
			letter_attempts.append(letter_attempt)
		word_attempts.append(letter_attempts)

	# Some formatting.
	for child in main_frame.winfo_children():
		child.grid_configure(padx=5, pady=5)

	# Reset button.
	reset_button = ttk.Button(input_frame, text="Reset", command=reset_game)
	reset_button.grid(column=2, row=9)

	# The button to show stats.
	stats_button = ttk.Button(input_frame, text="Stats", command=popup_window)
	stats_button.grid(column=2, row=10)

	root.bind("<Return>", input_callback)
	root.mainloop()
