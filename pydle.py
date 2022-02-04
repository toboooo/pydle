import datetime
import csv
import pickle
from tkinter import ttk
from tkinter import *


###############################################################

# Load in stats, create the stats dictionary if no file
try:
	stats_file = open('pydle_stats.pkl', 'rb')
	stats = pickle.load(stats_file)
	stats_file.close()
except FileNotFoundError:
	stats = {'n_plays': 0, 'last_date_played': datetime.datetime.now().date(),
			'played_today': False, '1_attempt': 0, '2_attempt': 0, 
			'3_attempt': 0, '4_attempt': 0,	'5_attempt': 0, '6_attempt': 0, 
			'n_attempts': 0, 'mean': 0, 'std_dev': 0, 'max': 0, 'min': 6, 
			'streak': 1, 'max_streak': 0}

# Set played_today to False if playing on new day
if stats['played_today'] == True:
	if datetime.datetime.now().date() != stats['last_date_played']:
		stats['played_today'] = False

# Increment the total number of plays if not played today
if stats['played_today'] == False:
	stats['n_plays'] += 1
	# Also increment the current streak, if played yesterday
	if (datetime.datetime.now().date() - stats['last_date_played']).days == 1:
		stats['streak'] += 1
	# change the max streak if exceeded
	if stats['streak'] > stats['max_streak']:
		stats['max_streak'] = stats['streak']
	# reset played today
	stats['played_today'] = True

###############################################################

# Get the word dictionaries.
with open('wordle_dicts.csv') as f:
	dicts = list(csv.reader(f))
	f.close()

# Choose a word based on the current date.
start_date = datetime.datetime(2021, 6, 19)
date_difference = datetime.datetime.now() - start_date
answer_word = dicts[0][date_difference.days]

# Initialise the number of attempts
attempt = 0

###############################################################

# Callback function bound to the return key.
def input_callback(*args):
	global attempt
	global letters
	# Check if number of allowed attempts has been reached
	if attempt <= 5:
		# Check if the input word is allowed
		if (word_var.get().lower() in dicts[0]) or (word_var.get().lower() in dicts[1]):
			# Loop through the letters in the word
			for index, letter in enumerate(word_var.get()):
				# Change the Label object for the current letter
				word_attempts[attempt][index].config(text=letter.upper())
				# Change the letter colors
				# Make the letter orange if it appears in the answer
				if letter in answer_word:
					word_attempts[attempt][index].config(foreground='#eba21a')
				# Make the letter green if it is in the correct place
				if letter == answer_word[index]:
					word_attempts[attempt][index].config(foreground='#5ceb1a')
				# Remove the letter from the string of untried letters
				try:
					letter_index = letters.index(letter.upper())
					letters = letters[:letter_index] + ' ' + letters[letter_index+1:]
				except ValueError:
					continue
			untried_letters.config(text=letters)
			attempt += 1

	# Clear the text box. Must be after finished with word_var
	word_entry.delete(0, END)

###############################################################

# Make the game gui.
root = tkinter.Tk()
root.title('Wordle in Python')

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
word_entry = ttk.Entry(input_frame, font=('Arial 30'), width=6, textvariable=word_var)
word_entry.grid(column=2, row=7)

# Make a widget for the list of letters.
letters = 'Q W E R T Y U I O P\n  A S D F G H J K L\n    Z X C V B N M'
untried_letters = ttk.Label(input_frame, font=('Arial 22'), text=letters)
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
		letter_attempt = ttk.Label(words_frame, font=('Arial 30'), text='')
		letter_attempt.grid(column=j, row=i+1)
		letter_attempts.append(letter_attempt)
	word_attempts.append(letter_attempts)

# Some formatting.
for child in main_frame.winfo_children():
	child.grid_configure(padx=5, pady=5)

root.bind('<Return>', input_callback)
root.mainloop()

