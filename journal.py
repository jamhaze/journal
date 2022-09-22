import datetime, pickle, random,  re, string
from collections import Counter

class Entry:
    '''Represents an entry in the journal.'''

    def __init__(self, words):
        '''Initialize an entry.'''
        self.words = words
        self.date = datetime.date.today()

    def match(self, text):
        '''Determine if an entry matches the search text.'''

        return text in str(self.date) or text in self.words

class Journal:

    def __init__(self):
        try:
            with open(
                r'C:\Users\James\Documents\Python\myScripts\journal\list.pkl',
                'rb') as file:
                    self.entries = pickle.load(file)
        except EOFError:
            self.entries = []

    def new_entry(self, words):
        self.entries.append(Entry(words))
        with open(
                r'C:\Users\James\Documents\Python\myScripts\journal\list.pkl',
                'wb') as file:
                    pickle.dump(self.entries, file)

    def search(self, text):
        '''Find all entries that match the text string.'''
        return [entry for entry in self.entries if
                entry.match(text)]

    def random_entry(self):
        index = random.randint(0, len(self.entries) - 1)
        return self.entries[index]

    def return_all_words(self):
        regex = re.compile('[^a-zA-Z \'\-]')

        all_words = []
        
        for entry in self.entries:
            no_punc = regex.sub('', entry.words).split(' ')
            for word in no_punc:
                if word:
                    all_words.append(word.lower())

        return all_words

    def find_most_common_words(self):
        all_words = self.return_all_words()
        c = Counter(all_words)

        return c.most_common(20)
            
    def find_longest_words(self):
        all_words = list(dict.fromkeys(self.return_all_words()))
        sorted_by_len = sorted(all_words, key=len, reverse=True)

        if len(sorted_by_len) > 20:
            top_twenty_sorted_by_len = sorted_by_len[0:20]
            return top_twenty_sorted_by_len
        else:
            return sorted_by_len

    def find_most_common_letters(self):

        letter_counts = dict.fromkeys(string.ascii_lowercase, 0)
        total = 0

        for entry in self.entries:
            for char in entry.words:
                lowercase_char = char.lower()
                if lowercase_char in letter_counts.keys():
                    letter_counts[lowercase_char] += 1
                    total += 1

        return sorted(letter_counts, key=letter_counts.get, reverse=True), letter_counts, total

    def find_most_common_word_combos(self):
        all_words = self.return_all_words()

        all_combos = []

        for i in range(len(all_words) - 1):
            word_combo = (all_words[i], all_words[i + 1])
            all_combos.append(word_combo)

        c = Counter(all_combos)

        return c.most_common(10)


            
            
        
        

           




        
    

        
     


                
