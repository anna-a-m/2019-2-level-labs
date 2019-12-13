"""
Labour work #3
 Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):

        self.storage = {}

    def put(self, word: str) -> int:
        if word not in self.storage and isinstance(word, str):
            id_word = hash(word)
            self.storage[word] = id_word
            return id_word
        return -1

    def get_id_of(self, word: str) -> int:

        if word in self.storage and isinstance(word, str):
            id_word = self.storage.get(word)
            return id_word
        return -1

    def get_original_by(self, id_number: int) -> str:

        if id_number in self.storage.values():
            id_word = list(self.storage.values()).index(id_number)
            return list(self.storage.keys())[id_word]
        return "UNK"

    def from_corpus(self, corpus: tuple):

        if corpus and isinstance(corpus, tuple):
            corpus = set(corpus)
            for element in corpus:
                id_element = hash(element)
                self.storage[element] = id_element
        return self.storage


class NGramTrie:
    def __init__(self, n):

        self.size = n
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:

        if sentence is not None and isinstance(sentence, tuple):
            for i in range(len(sentence) - self.size + 1):
                n_list = [sentence[i + j] for j in range(self.size)]
                n_tuple = tuple(n_list)
                if n_tuple in self.gram_frequencies.keys():
                    self.gram_frequencies[n_tuple] += 1
                else:
                    self.gram_frequencies[n_tuple] = 1
            return self.gram_frequencies
        return []

    def calculate_log_probabilities(self):
        prob_dict = {}
        for key, value in self.gram_frequencies.items():
            if key[:self.size - 1] not in prob_dict:
                prob_dict[key[:self.size - 1]] = value
            else:
                prob_dict[key[:self.size - 1]] += value
        for key, value in self.gram_frequencies.items():
            if key not in self.gram_log_probabilities:
                probability = value / prob_dict[key[:self.size - 1]]
                self.gram_log_probabilities[key] = math.log(probability)
        return self.gram_log_probabilities

    def predict_next_sentence(self, prefix: tuple) -> list:

        next_sentence = []
        list_prob_keys = []
        list_prob_values = []
        if prefix is not None and isinstance(prefix, tuple) and len(prefix) == self.size - 1:
            next_sentence.extend(list(prefix[:self.size - 1]))
            for _ in self.gram_log_probabilities:
                if prefix[-1] not in next_sentence:
                    next_sentence.append(prefix[-1])
                for key in list(self.gram_log_probabilities.keys()):
                    if prefix == key[:-1]:
                        list_prob_keys.append(key)
                        list_prob_values.append(self.gram_log_probabilities[key])
                if list_prob_keys != [] and list_prob_values != []:
                    key_prob = max(list_prob_values)
                    prefix = list_prob_keys[list_prob_values.index(key_prob)][1:]
                    list_prob_keys = []
                    list_prob_values = []
        return next_sentence


def encode(storage_instance, corpus) -> list:
    for sentence in corpus:
        for word in sentence:
            for key, value in storage_instance.items():
                if word == key:
                    sentence[sentence.index(word)] = value
    return corpus


def split_by_sentence(text: str) -> list:
    corpus = []
    new_text = ''
    if isinstance(text, str) and ' ' in text:
        text = text.replace('\n', ' ')
        while '  ' in text:
            text = text.replace('  ', ' ')
        text = text.replace('!', '.')
        text = text.replace('?', '.')
        if '.' in text:
            for symbol in text:
                if symbol.isalpha() or symbol == ' ' or symbol == '.':
                    new_text += symbol.lower()
    sentences = new_text.split('.')
    while '' in sentences:
        sentences.remove('')
    for element in sentences:
        element = element.split()
        element.insert(0, '<s>')
        element.append('</s>')
        corpus.append(element)
    return corpus
