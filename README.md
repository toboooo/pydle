# pydle
An implementation of the game Wordle (https://www.powerlanguage.co.uk/wordle/) in Python, using Tkinter.

To play, run the script and enter five letter words into the text box until the correct word is guessed or all six attempts are used up. Letters are highlighted green if they are in the word and in the correct place, and highlighted orange if they are in the word but not in the correct place. Once the word is guessed correctly or the player runs out of attempts, the "Reset" button may be used to play again.

The game records play stats in a binary file ('pydle_stats.pkl') in the same directory as the pydle.py script.

Use Python >= 3.6. There are no other dependencies since the only libraries pydle uses are the Python standard libraries: tkinter, os, random, csv and pickle.
