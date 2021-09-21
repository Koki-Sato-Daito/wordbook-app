import sys
import csv

from nltk.corpus import stopwords


def main():
    stop_words = stopwords.words('english')
    file_re = sys.argv[1]
    file_wr = sys.argv[2]
    fr = open(file_re, 'r')
    fw =  open(file_wr, 'w')
    reader = csv.reader(fr)
    writer = csv.writer(fw)

    for row in reader:
        if row[0] not in stop_words:
            writer.writerow(row)
            print(row)

    fr.close()
    fw.close()


if __name__ == '__main__':
    main()