import sys
import re

import pandas as pd
from googletrans import Translator


def main():
    file_r = sys.argv[1]
    df = pd.read_csv(file_r)

    res = []
    for tuple, count in df.value_counts().iteritems():
        word =  tuple[0]
        pos = tuple[1]

        pattern = re.compile(r'[^0-9a-zA-Z]')
        match = re.search(pattern, word)
        if match is None:
            res.append((word, pos, count))

    df = pd.DataFrame(res, columns=['word', 'pos', 'freq'])
    file_w = sys.argv[2]
    df.to_csv(file_w)
    
        
if __name__ == '__main__':
    main()