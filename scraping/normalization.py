import csv
import sys
from typing import Sequence

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

class NltkClient:
    @staticmethod
    def stemming_words(words):
        stem = PorterStemmer()
        stemmed = []
        for word in words:
            stemmed.append(stem.stem(word))
        return stemmed

    @staticmethod
    def lemmatize_sentence(word, tag):
        lemmatizer = WordNetLemmatizer()
        # 名詞
        if tag.startswith('NN'):
            pos = wordnet.NOUN
        # 動詞
        elif tag.startswith('VB'):
            pos = wordnet.VERB
        # 形容詞
        elif tag.startswith('JJ'):
            pos = wordnet.ADJ
        # 副詞
        elif tag.startswith('RB'):
            pos = wordnet.ADV
        else:
            return None
        return (lemmatizer.lemmatize(word, pos), pos)

    @staticmethod
    def tokenize_words(sentence):
        tokenized = word_tokenize(sentence)
        return tokenized

    @staticmethod
    def tag_to_pos_string(tag):
        if tag == wordnet.NOUN:
            pos = 'noun'
        # 動詞
        elif tag == wordnet.VERB:
            pos = 'verb'
        # 形容詞
        elif tag == wordnet.ADJ:
            pos = 'adjective'
        # 副詞
        elif tag == wordnet.ADV:
            pos = 'adverb'
        else:
            return None
        return pos

def main():
    file_r = sys.argv[1]
    file_w = sys.argv[2]
    with open(file_r, 'r') as f:
        document = f.readlines()
    
    words = []
    for line in document:
        if line == '\n':
            continue
        
        for word, tag in pos_tag(NltkClient.tokenize_words(line)):
            if lemmed := NltkClient.lemmatize_sentence(word.lower(), tag):
                lemmed_word = lemmed[0]
                pos = NltkClient.tag_to_pos_string(lemmed[1])
                words.append( (lemmed_word,pos) )
                print(lemmed)

    with open(file_w, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for row in words:
            writer.writerow(row)

if __name__ == '__main__':
    main()
