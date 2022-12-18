import textwrap, os
from journal import Journal
from termcolor import colored
from texttable import Texttable

class Menu:
  
  # The __init__ method sets up three variables: A Journal object, A dictionary of main menu methods, A dictionary
  # of stats menu methods.
  def __init__(self):

    self.journal = Journal()

    # The key is the choice number and the value is a method to be called if that choice is selected.
    self.methods = {
      '1': self.search_entries,
      '2': self.new_entry,
      '3': self.random_entry,
      '4': self.delete_entry,
      '5': self.stats
    }

    self.stats_methods = {
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
4. Delete Entry
5. Stats
6. Quit''')

  # This method prints the stats menu.
  def display_stats_menu(self):
    print('''
Stats Menu

1. Most Common Words
2. Longest Words
3. Most Common Letters
4. Most Common Word Combos
5. Back to Main Menu''')

  # This method runs the main menu in a loop until the user selects '5' (Quit).
  def run(self):

    os.system('color')
    
    print()
    print('~ Journal ~')

    run = True

    while run:

      self.display_main_menu()

      # Call the make_choice method and send the methods dictionary as a parameter.
      method = self.make_choice(self.methods)

      # If a method is returned call the method. Else end the loop.
      if method:
        method()
      else:
        run = False

    # Exit the program.
    print('Thank you for using your journal today.')
    self.journal.save()

  # Allows the user to search for entries that contain the search string.
  def search_entries(self):
    print()
    search_string = input('Enter a string to search: ')

    entries = self.find_matching_entries(search_string)

    date = ''
    words = ''

    # For each entry print it to the console with the matching string coloured.
    for entry in entries:
      date = self.color_text_match(str(entry.date), search_string)
      words = self.color_text_match(entry.words, search_string)
      self.display_entry(date, words)

  # Lets the user write a new entry to the journal.
  def new_entry(self):
    print()
    entry = input('Enter an entry: ')
    self.journal.new_entry(entry)

  # Returns a random entry from the journal and displays it on screen.
  def random_entry(self):
    entry = self.journal.random_entry()

    # Can call display_entry to display the single entry.
    self.display_entry(entry.date, entry.words)

  # Deletes an entry from the journal.
  def delete_entry(self):

    # prompt the user to search for an entry.
    print()
    search_string = input('Enter the date or words from the entry you want to delete: ')

    # returns entries that match with the search string.
    entries = self.find_matching_entries(search_string)

    if entries:
      menu = 'Choose an entry to delete\n\n'
      entry_choices = {}

      # This while loop will construct a menu string to be printed and a dictionary of choices.
      i = 0
      while i < len(entries):

        entry = entries[i]

        choice_num = str(i + 1)
        menu += choice_num + '. ' + str(entry.date) + ' - '

        if len(entry.words) <= 80:
          menu += entry.words + '\n'
        else:
          menu += entry.words[:80] + '...\n'

        entry_choices[choice_num] = entry
        i += 1

      menu += str(i + 1) + '. Back to main menu.'
      
      # print the menu
      print()
      print(menu)

      entry = self.make_choice(entry_choices)

      # If an entry is returned call the journals delete entry method.
      if entry:
        self.journal.delete_entry(entry)

    else:
      print()
      print('Nothing found')

  # run the stats menu
  def stats(self):
    run = True

    while run:
      self.display_stats_menu()
      method = self.make_choice(self.stats_methods)

      if method:
        method()
      else:
        run = False

  # Displays the top twenty most common words in the journal.
  def find_most_common_words(self):

    # word_counts is a list of tuples with the word as the first element and the number
    # of occurances as the second element.
    word_counts = self.journal.find_most_common_words()

    table = Texttable()
    table.header(['word', 'occurances'])

    for word_count in word_counts:
      table.add_row([word_count[0], word_count[1]])

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

    letter_counts, total = self.journal.find_most_common_letters()

    table = Texttable()
    table.header(['letter', 'occurances', 'percentage'])

    for letter_count in letter_counts:
      count = letter_count[1]
      table.add_row([letter_count[0], count, (count/total) * 100])
    
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

  # allows the user to make a choice from the choices dictionary and returns the value of the choice.
  def make_choice(self, choices):

    choice_value = None

    # The final choice will always be the choice to quit or return to the main menu, so it will not
    # have a key, value pair in the choices dictionary.
    final_choice = str(len(choices) + 1)

    print()
    choice = input('Enter an option: ')

    # Loop until the user makes a valid choice.
    while choice not in choices.keys() and choice != final_choice:
      print()
      print('"{0}" is not a valid choice.  Please enter a number between 1 and {1}.'.format(choice, final_choice))
      print()
      choice = input('Enter an option: ')

    # User choice will either be in the choices dictionary, or it will be the final choice.
    if choice in choices.keys():
      choice_value = choices.get(choice)

    return choice_value

  # Returns entries that contain the search_string in the date or words
  def find_matching_entries(self, search_string):
    entries = self.journal.search(search_string)

    if not entries:
      print()
      print('Nothing found.')

    elif len(entries) == 1:
      print()
      print('1 entry found')
    
    else:
      print()
      print(str(len(entries)) + ' entries found')

    return entries

  # returns a string with the characters in text_match colored
  def color_text_match(self, text, text_match):

    # The length of match will be needed multiple times so store it in a variable.
    span = len(text_match)
    colored_text = ''
    i = 0

    # Loop through the characters in text.
    while i < len(text):
        
      # Check to see if a section of the text matches and add that section as colored text to colored_text if it does.
      if text[i: i + span] == text_match:
        colored_text += colored(text_match, 'yellow', attrs=['bold'])
        i += span
      else:
        colored_text += text[i]
        i += 1

    return colored_text

  # Displays a single entry in a formatted way.
  def display_entry(self, date, words):
    print()
    print('{0} - {1}'.format(date, textwrap.fill(words, 100, subsequent_indent='\t     ')))

if __name__ == '__main__':
    Menu().run()


  
