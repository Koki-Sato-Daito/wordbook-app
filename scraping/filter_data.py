import pandas as pd
import sys

def main():
    file_name = sys.argv[1]
    lang = sys.argv[2]

    df = pd.read_csv(file_name, index_col=0)
    df.columns = ['word', 'pos', 'freq']
    df.sort_values('freq', ascending=False)
    
    nouns = df.query('pos == "noun"')[:600]
    nouns.to_csv('./work/' + lang + '_nouns.csv')
    # print(nouns.head(100))

    verbs = df.query('pos == "verb"')[:600]
    verbs.to_csv('./work/' + lang + '_verbs.csv')
    # print(nouns.head(10))

    adjectives = df.query('pos == "adjective"')[:400]
    adjectives.to_csv('./work/' + lang + '_adjectives.csv')
    # print(nouns.head(10))

    adverbs = df.query('pos == "adverb"')[:400]
    adverbs.to_csv('./work/' + lang + '_adverbs.csv')
    # print(adverbs.head(10))

if __name__ == '__main__':
    main()