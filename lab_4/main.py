import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(scripts: list) -> list:
    if not isinstance(scripts, list):
        return []
    corpora = []
    for script in scripts:
        if not isinstance(script, str):
            continue
        script = script.lower()
        script = script.replace('<br />', ' ')
        for sign in script:
            if not sign.isalpha() and sign != ' ':
                script = script.replace(sign, '')
        corpora.append(script.split())
    return corpora


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []

    def calculate_tf(self):
        if not isinstance(self.corpus, list):
            return []
        for doc in self.corpus:
            if not isinstance(doc, list):
                continue
            doc_dict = {}
            clean_doc = []
            for elem in doc:
                if isinstance(elem, str):
                    clean_doc.append(elem)
            for word in clean_doc:
                if word not in doc_dict:
                    doc_dict[word] = doc.count(word) / len(clean_doc)
            self.tf_values.append(doc_dict)
        return self.tf_values

    def calculate_idf(self):
        if not isinstance(self.corpus, list):
            return {}
        all_words = [el for doc in self.corpus if isinstance(doc, list) for el in doc if isinstance(el, str)]
        words = list(set(all_words))
        clean_corpus = []
        for doc in self.corpus:
            if isinstance(doc, list):
                clean_corpus.append(doc)
        for word in words:
            frequency = [1 for doc in clean_corpus if isinstance(doc, list) and word in doc]
            self.idf_values[word] = math.log(len(clean_corpus) / sum(frequency))
        return self.idf_values

    def calculate(self):
        if not isinstance(self.tf_values, list):
            return []
        for doc in self.tf_values:
            new_doc_dict = {}
            for key in doc:
                if key in doc and key in self.idf_values:
                    new_doc_dict[key] = doc[key] * self.idf_values[key]
                else:
                    return []
            self.tf_idf_values.append(new_doc_dict)
        return self.tf_idf_values

    def report_on(self, word, document_index):
        if self.tf_idf_values is None or document_index > len(self.tf_idf_values) - 1 or \
                word not in self.tf_idf_values[document_index]:
            return ()
        word_info = [self.tf_idf_values[document_index][word]]
        the_most_important = list(self.tf_idf_values[document_index].items())
        the_most_important.sort(key=lambda x: x[1], reverse=True)
        ind = -1
        for elem in the_most_important:
            if elem[0] == word:
                ind = the_most_important.index(elem)
                break
        if ind != -1:
            word_info.append(ind)
        return tuple(word_info)

    def dump_report_csv(self):
        with open('new.csv', "a") as file:
            all_words = [el for doc in self.corpus if isinstance(doc, list) for el in doc if isinstance(el, str)]
            words = list(set(all_words))
            for word in words:
                metrics = []
                for doc in self.tf_values:
                    if word in doc:
                        metrics.append(doc[word])
                    else:
                        metrics.append(0)
                metrics.append(self.idf_values[word])
                for doc in self.tf_idf_values:
                    if word in doc:
                        metrics.append(doc[word])
                    else:
                        metrics.append(0)
                metrics = [str(elem) for elem in metrics]
                file.write(word + ',' + ','.join(metrics))
                file.write('\n')

    def cosine_distance(self, index_text_1: int, index_text_2: int) -> int:
        if index_text_1 > len(self.tf_idf_values) - 1 or index_text_2 > len(self.tf_idf_values) - 1:
            return 1000
        first_text_dict = self.tf_idf_values[index_text_1]
        second_text_dict = self.tf_idf_values[index_text_2]
        words = list(first_text_dict.keys())
        words.extend(list(second_text_dict.keys()))
        words = list(set(words))
        first_vector = []
        second_vector = []
        for word in words:
            if word in first_text_dict and word in second_text_dict:
                first_vector.append(first_text_dict[word])
                second_vector.append(second_text_dict[word])
            elif word in first_text_dict:
                first_vector.append(first_text_dict[word])
                second_vector.append(0)
            else:
                first_vector.append(0)
                second_vector.append(second_text_dict[word])
        scalar_product = [first_vector[i] * second_vector[i] for i in range(len(first_vector))]
        first_norm = [i ** 2 for i in first_vector]
        second_norm = [j ** 2 for j in second_vector]
        cos_distance = sum(scalar_product) / math.sqrt(sum(first_norm) * sum(second_norm))
        return cos_distance


if __name__ == '__main__':
    TEXTS = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in TEXTS:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    TEST_TEXTS = clean_tokenize_corpus(REFERENCE_TEXTS)
    TF_IDF = TfIdfCalculator(TEST_TEXTS)
    TF_IDF.calculate_tf()
    TF_IDF.calculate_idf()
    TF_IDF.calculate()
    print(TF_IDF.report_on('good', 0))
    print(TF_IDF.report_on('and', 1))
