# pydle
An implementation of the game Wordle (https://www.powerlanguage.co.uk/wordle/) in Python, using Tkinter.

To play, run the script and enter five letter words into the text box until the correct word is guessed or all six attempts are used up. Letters are highlighted green if they are in the word and in the correct place, and highlighted orange if they are in the word but not in the correct place. The word changes each day.

The game records play stats (such as mean number of attempts and the current streak) in a binary file ('pydle_stats.pkl') in the same directory as the pydle.py script. The play stats are recorded once the word has been correctly guessed, or until all six attempts are used up. The stats are recorded for the first completed game of each day.

Use Python >= 3.6. No other dependencies since the only libraries pydle uses are the Python standard libraries: tkinter, datetime, csv and pickle.
