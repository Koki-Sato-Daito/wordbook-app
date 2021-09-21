from bs4 import BeautifulSoup
import sys
import re

def main():
    html_doc = sys.argv[1]
    write_file = sys.argv[2]

    with open(html_doc, 'r') as rf:
        with open(write_file, 'w') as wf:
            line = rf.readline()
            while line:
                soup = BeautifulSoup(line, 'html.parser')
                for script in soup('script'):
                    script.extract()
                for style in soup('style'):
                    style.extract()
                text = soup.get_text()
                text = re.sub(r'[^\w|\ ]', '\n', text)
                print(text)
                wf.write(text)
                line = rf.readline()

if __name__ == '__main__':
    main()