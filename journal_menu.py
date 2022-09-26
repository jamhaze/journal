import sys, textwrap
from journal import Journal
from texttable import Texttable

class Menu:
    
    # The __init__ method sets up three variables: A Journal object, A dictionary of main menu choices, A dictionary
    # of stats menu choices.
    def __init__(self):

        self.journal = Journal()

        # The key is the choice number and the value is a function to be called if that choice is selected.
        self.main_choices = {
                '1': self.search_entries,
                '2': self.new_entry,
                '3': self.random_entry,
                '4': self.stats
                }

        self.stats_choices = {
                '1': self.find_most_common_words,
                '2': self.find_longest_words,
                '3': self.find_most_common_letters,
                '4': self.find_most_common_word_combos
                }

    # This method prints the main menu
    def display_main_menu(self):
        print('''
Main Menu

1. Search Entries
2. New Entry
3. Random Entry
4. Stats
5. Quit
''')

    # This method prints the stats menu.
    def display_stats_menu(self):
        print('''
Stats Menu

1. Most Common Words
2. Longest Words
3. Most Common Letters
4. Most Common Word Combos
5. Back to Main Menu
''')

    # This method runs the main menu in a loop until the user selects '5' (Quit).
    def run(self):
        
        choice = ''
        while choice != '5':

            self.display_main_menu()

            # Call the make_choice method and send the main_choices dictionary as a parameter.
            choice = self.make_choice(self.main_choices)

        print()
        print('Thank you for using your journal today.')
        sys.exit(0)
            
    # This method dispalys all the elements in the list entries
    def show_entries(self, entries):
        for entry in entries:
            self.show_entry(entry)

    # Prints an entry in a neatly formatted way.
    def show_entry(self, entry):
        print()
        print('{0} - {1}'.format(
            str(entry.date), textwrap.fill(entry.words,
                                           100,
                                           subsequent_indent='\t     ')))

    # Allows the user to search for entries that contain the search string.
    def search_entries(self):
        print()
        text = input('Enter a string to search: ')
        entries = self.journal.search(text)
        if not entries:
            print()
            print('Nothing found.')
        else:
            self.show_entries(entries)

    # Lets the user write a new entry to the journal.
    def new_entry(self):
        entry = input('Enter an entry: ')
        self.journal.new_entry(entry)

    # Returns a random entry from the journal and displays it on screen.
    def random_entry(self):
        entry = self.journal.random_entry()

        # Can call show_entry to display the single entry.
        self.show_entry(entry)

    # This method is called when the user selects the stats option from the main menu.  It runs the
    # stats menu in a loop until the user selects '5'.
    def stats(self):
        choice = ''
        while choice != '5':
            self.display_stats_menu()

            # Call the make choice method and pass the stats_choices dictionary as a parameter.
            choice = self.make_choice(self.stats_choices)

    # Displays the top twenty most common words in the journal.
    def find_most_common_words(self):

        # word_counts is a list of tuples with the word as the first element and the number
        # of occurances as the second element.
        word_counts = self.journal.find_most_common_words()

        table = Texttable()
        table.header(['word', 'occurances'])

        for word in word_counts:
            table.add_row([word[0], word[1]])

        print()
        print(table.draw())

    # Displays the top twenty longest words in the journal.
    def find_longest_words(self):

        # Longest words is a list of the top twenty longest words.
        longest_words = self.journal.find_longest_words()

        table = Texttable()
        table.header(['word', 'length'])

        for word in longest_words:
            table.add_row([word, len(word)])

        print()
        print(table.draw())

    # Displays a table with the letters of the alphabet, their occurances, and their total percentage of all letters used.
    def find_most_common_letters(self):

        # letter_order is a list containing the order of the letters from most to least frequent.
        # letter_counts is a dictionary of the letters and their counts.
        # total is the total number of letters used in the journal.
        letter_order, letter_counts, total = self.journal.find_most_common_letters()

        table = Texttable()
        table.header(['letter', 'occurances', 'percentage'])

        for letter in letter_order:
            count = letter_counts[letter]
            table.add_row([letter, count, (count/total) * 100])
        
        print()
        print(table.draw())

    # Displays the top ten most common word combinations in the journal.
    def find_most_common_word_combos(self):

        # Word combos is a list of tuples containing the word combo as the first element and the
        # number of occurances as the second element.
        word_combos = self.journal.find_most_common_word_combos()

        table = Texttable()
        table.header(['word combo', 'occurances'])

        for word_combo in word_combos:
            table.add_row([word_combo[0], word_combo[1]])

        print()
        print(table.draw())

    # This method takes either the main_choices or stats_choices dictionaries as a parameter and
    # processes a choice gathered from the user.
    def make_choice(self, choices):

        choice = input('Enter an option: ')

        # If the choice is a key in the dictionary, the action variable will contain a method.  If it is
        # not a key, action will contain None.
        action = choices.get(choice)
        final_choice = str(len(choices) + 1)

        if action:

            # If action is not None it will contain a method and it can be called.
            action()

        elif choice != final_choice:

            print()
            print('"{0}" is not a valid choice.  Please enter a number between 1 and {1}.'.format(choice, final_choice)) 

        return choice
        

if __name__ == '__main__':
    Menu().run()
