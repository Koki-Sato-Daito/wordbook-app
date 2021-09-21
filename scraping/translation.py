import sys
import time

from bs4 import BeautifulSoup
import pandas as pd
import requests


class Translator:
    @staticmethod
    def translate(word):
        res = requests.get('https://ejje.weblio.jp/content/' + word)
        soup = BeautifulSoup(res.text, 'html.parser')
        meaning_html = soup.find(class_="content-explanation")
        if meaning_html:
            meaning_text = meaning_html.get_text()
            return meaning_text
        else:
            return ''

def main():
    r_file = sys.argv[1]
    df = pd.read_csv(r_file)
    
    res = []
    translator = Translator()
    for _, row in df.iterrows():
        time.sleep(1)
        try:
            translated = translator.translate(row.word)
            print(translated)
            res.append((row.word, row.pos, row.freq, translated))
        except:
            continue
    
    w_file = sys.argv[2]
    new_df = pd.DataFrame(res, columns=['word', 'pos', 'freq', 'japanese'])
    new_df.to_csv(w_file)


if __name__ == '__main__':
    main()