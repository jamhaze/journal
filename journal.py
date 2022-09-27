import datetime, pickle, random,  re, string, os, sys
from collections import Counter

class Entry:
    
    # The Entry object is initialised with two attributes:  The words making up the entry and the date of its
    # submission.
    def __init__(self, words):
        
        self.words = words
        self.date = datetime.date.today()

    # This method returns true if the text parameter is contained within either the date or words.
    def contains(self, text):

        return text in str(self.date) or text in self.words

class Journal:

    def __init__(self):

        # Open list.pkl and load all the Entry objects into a list called entries. (The pickle file stores objects in a 
        # binary format).  If list.pkl doesn't exist, it will be created in the current directory.
        try:
            with open(os.path.join(sys.path[0], 'list.pkl'), 'rb') as file:
                self.entries = pickle.load(file)

        # This exception will only occur if the pickle file is empty, so create an empty list.
        except EOFError:
            self.entries = []

    def new_entry(self, words):

        # Create a new Entry object with the words supplied by the user and append it to the entries list.
        self.entries.append(Entry(words))

        # Dump the entries array into the pickle file.
        with open(os.path.join(sys.path[0], 'list.pkl'), 'wb') as file:
            pickle.dump(self.entries, file)

    # This method returns a list with entries that contain the text parameter in the date or words.
    def search(self, text):
        
        return [entry for entry in self.entries if entry.contains(text)]

    # This method returns a random entry from entries.
    def random_entry(self):

        index = random.randint(0, len(self.entries) - 1)
        return self.entries[index]

    # Returns a list containing all the words in all entries.
    def return_all_words(self):

        all_words = []
        
        for entry in self.entries:

            # Split the entries at whitespace.
            words = entry.words.split()

            for word in words:

                # Subs out all non-letter characters at the beginning or end of a string before appending the string
                # to all_words.
                subbed_word = re.sub('^[^a-zA-Z]*|[^a-zA-Z]*$', '', word)

                # Check subbed_word is not an empty string.
                if subbed_word:
                    all_words.append(subbed_word.lower())

        return all_words

    # Returns the twenty most common words and their counts.
    def find_most_common_words(self):

        all_words = self.return_all_words()
        c = Counter(all_words)

        return c.most_common(20)

    # Return a list of the longest words.
    def find_longest_words(self):

        # A list of all words from longest to shortest.
        sorted_by_len = sorted(self.return_all_words(), key=len, reverse=True)

        # Return a list that either contains the top twenty longest words or all the words if there are less than twenty
        # words. (The zip function returns an iterator that is the length of the parameter with the least items)
        return [x for _, x in zip(range(20), sorted_by_len)]

    # Returns a sorted list of letter counts and the total amount of letters used.
    def find_most_common_letters(self):

        # Make a regex to match any non-letter characters.
        regex = re.compile('[^a-zA-Z]')

        # Make a counter with lowercase letters as keys.
        letter_counts = Counter(dict.fromkeys(string.ascii_lowercase, 0))
        total = 0

        for entry in self.entries:

            # remove all non-letter characters from entry.words
            subbed_entry = regex.sub('', entry.words)

            # Update the Counter and the total.
            letter_counts.update(subbed_entry.lower())
            total += len(subbed_entry)

        return letter_counts.most_common(26), total

    # Returns a sorted list of the most common word combos used in the dictionary.
    def find_most_common_word_combos(self):

        all_words = self.return_all_words()

        all_combos = []

        for i in range(len(all_words) - 1):
            word_combo = all_words[i] + ' ' + all_words[i + 1]
            all_combos.append(word_combo)

        c = Counter(all_combos)

        return c.most_common(10)


            
            
        
        

           




        
    

        
     


                
