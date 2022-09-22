import sys, textwrap
from journal import Journal
from texttable import Texttable

class Menu:
    '''Display a menu and respond to choices when run.'''
    def __init__(self):
        self.journal = Journal()
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

    def display_menu(self):
        print('''
Journal Menu

1. Search Entries
2. New Entry
3. Random Entry
4. Stats
5. Quit
''')

    def display_stats_menu(self):
        print('''
Stats Menu

1. Most Common Words
2. Longest Words
3. Most Common Letters
4. Most Common Word Combos
5. Back to Main Menu
''')

    def run(self):
        '''Display the menu and respond to choices.'''
        choice = ''
        while choice != '5':
            self.display_menu()
            choice = self.make_choice(self.main_choices)

        print()
        print('Thank you for using your journal today.')
        sys.exit(0)
            

    def show_entries(self, entries):
        for entry in entries:
            self.show_entry(entry)

    def show_entry(self, entry):
        print()
        print('{0} - {1}'.format(
            str(entry.date), textwrap.fill(entry.words,
                                           100,
                                           subsequent_indent='\t     ')))

    def search_entries(self):
        print()
        text = input(
            'Enter a string to search: ')
        entries = self.journal.search(text)
        if not entries:
            print()
            print('Nothing found.')
        else:
            self.show_entries(entries)

    def new_entry(self):
        entry = input('Enter an entry: ')
        self.journal.new_entry(entry)

    def random_entry(self):
        entry = self.journal.random_entry()
        self.show_entry(entry)

    def stats(self):
        choice = ''
        while choice != '5':
            self.display_stats_menu()
            choice = self.make_choice(self.stats_choices)

    def find_most_common_words(self):
        word_counts = self.journal.find_most_common_words()

        table = Texttable()
        table.header(['word', 'occurances'])

        for word in word_counts:
            table.add_row([word[0], word[1]])

        print()
        print(table.draw())

    def find_longest_words(self):
        ten_longest_words = self.journal.find_longest_words()

        table = Texttable()
        table.header(['word', 'length'])

        for word in ten_longest_words:
            table.add_row([word, len(word)])

        print()
        print(table.draw())

    def find_most_common_letters(self):
        letter_order, letter_counts, total = self.journal.find_most_common_letters()

        table = Texttable()
        table.header(['letter', 'occurances', 'percentage'])

        for letter in letter_order:
            count = letter_counts[letter]
            table.add_row([letter, count, (count/total) * 100])
        
        print()
        print(table.draw())

    def find_most_common_word_combos(self):
        word_combos = self.journal.find_most_common_word_combos()

        table = Texttable()
        table.header(['word combo', 'occurances'])

        for word_combo in word_combos:
            table.add_row([word_combo[0][0] + ' ' + word_combo[0][1], word_combo[1]])

        print()
        print(table.draw())

    def make_choice(self, choices):
        choice = input('Enter an option: ')
        action = choices.get(choice)
        if action:
            action()
        else:
            try:
                num = int(choice)
                if num != len(choices) + 1:
                   print('{0} is not a valid choice'.format(choice)) 
            except:
                print('Please enter a number')

        return choice
        

if __name__ == '__main__':
    Menu().run()
