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
        if not isinstance(word, str):
            return -1
        if word not in self.storage:
            if not self.storage:
                self.storage[word] = 0
            else:
                self.storage[word] = max(list(self.storage.values())) + 1
        return self.storage[word]

    def get_id_of(self, word: str) -> int:
        if not isinstance(word, str) or word not in self.storage:
            return -1
        return self.storage[word]

    def get_original_by(self, identifier: int) -> str:
        for key, value in self.storage.items():
            if value == identifier:
                return key
        return 'UNK'

    def from_corpus(self, corpus: tuple):
        if not isinstance(corpus, tuple) or not corpus:
            return {}
        for word in corpus:
            if word not in self.storage:
                self.storage[word] = self.put(word)
        return self.storage


class NGramTrie:
    def __init__(self, number):
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}
        self.size = number

    def fill_from_sentence(self, sentence: tuple) -> str:
        if not isinstance(sentence, tuple) or not sentence:
            return 'ERROR'
        patterns = []
        for i in range(len(sentence)):
            if len(sentence) - i > self.size:
                patterns.append(sentence[i: i + self.size])
            elif len(sentence) - i == self.size:
                patterns.append(sentence[i:])
        for element in patterns:
            if element not in self.gram_frequencies:
                self.gram_frequencies[element] = 1
            else:
                self.gram_frequencies[element] += 1
        return 'OK'

    def calculate_log_probabilities(self):
        for pattern in self.gram_frequencies:
            frequent = [v for k, v in self.gram_frequencies.items() if pattern[0:len(pattern) - 1] == k[0:len(k) - 1]]
            probability = self.gram_frequencies[pattern] / sum(frequent)
            self.gram_log_probabilities[pattern] = math.log(probability)

    def predict_next_sentence(self, prefix: tuple) -> list:
        if not isinstance(prefix, tuple) or not prefix or len(prefix) != self.size - 1:
            return []
        prefix = list(prefix)
        basis = [elem[0:len(elem) - 1] for elem in self.gram_log_probabilities]
        basis = list(map(list, basis))
        sentence = []
        sentence.extend(prefix)
        while prefix in basis:
            where_to_find = {k: v for k, v in self.gram_log_probabilities.items() if tuple(prefix) == k[0:len(k) - 1]}
            most_frequent = list(where_to_find.items())
            most_frequent.sort(key=lambda x: x[1], reverse=True)
            sentence.append(most_frequent[0][0][-1])
            prefix = list(most_frequent[0][0][1:])
        return sentence


def encode(storage_instance, corpus) -> list:
    encoded_corpus = []
    for sentence in corpus:
        encoded_sentence = []
        for word in sentence:
            encoded_sentence.append(storage_instance[word])
        encoded_corpus.append(encoded_sentence)
    return encoded_corpus


def split_by_sentence(text: str) -> list:
    if not isinstance(text, str) or not text or '.' not in text:
        return []
    text = text.replace('!', '.')
    text = text.replace('?', '.')
    text = text.lower()
    sentences = text.split('. ')
    clear_sentences = []
    for sentence in sentences:
        for symbol in sentence:
            if not symbol.isalpha() and symbol != ' ':
                sentence = sentence.replace(symbol, '')
        clear_sentences.append(sentence)
    if not clear_sentences:
        return []
    corpus = []
    for sentence in clear_sentences:
        sentence = sentence.split()
        to_add = ['<s>']
        to_add.extend(sentence)
        to_add.append('</s>')
        corpus.append(to_add)
    return corpus


def initialisation(text: str, first_part: tuple) -> list:
    size = len(first_part) + 1
    NANI_GRAM = NGramTrie(size)
    split_text = split_by_sentence(text)
    for sentence in split_text:
        REAL_STORAGE.from_corpus(tuple(sentence))
    corpus_in_code = encode(REAL_STORAGE.storage, split_text)
    for sentence_in_code in corpus_in_code:
        NANI_GRAM.fill_from_sentence(tuple(sentence_in_code))
    NANI_GRAM.calculate_log_probabilities()
    prefix = []
    for word in first_part:
        prefix.append(real_storage.get_id_of(word))
    result = NANI_GRAM.predict_next_sentence(tuple(prefix))
    return result


def decoding(sentence_in_code: tuple) -> str:
    real_sentence = []
    for number in sentence_in_code:
        real_sentence.append(REAL_STORAGE.get_original_by(number))
    if real_sentence:
        real_sentence = list(real_sentence)
        if '<s>' in real_sentence:
            ind = real_sentence.index('<s>')
            real_sentence.pop(ind)
            real_sentence[ind] = real_sentence[ind].capitalize()
        if '</s>' in real_sentence:
            ind = real_sentence.index('</s>')
            real_sentence.pop(ind)
        if real_sentence:
            sentence = ' '.join(real_sentence)
            return sentence
    return ''


REAL_STORAGE = WordStorage()
encoded_list = initialisation(REFERENCE_TEXT, ('<s>', 'sherlock', 'holmes'))
to_print = decoding(tuple(encoded_list))
print(to_print)
