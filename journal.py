import datetime, pickle, random,  re
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

        return c.most_common(10)
            
    def find_longest_words(self):
        all_words = list(dict.fromkeys(self.return_all_words()))
        sorted_by_len = sorted(all_words, key=len, reverse=True)
                               
        return sorted_by_len[0:10]
            
            
        
        

           




        
    

        
     


                
