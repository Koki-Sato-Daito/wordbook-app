import glob
import sys

def main():
    args = sys.argv
    dir = args[1]
    file_name = args[2]
    files = []
    files += glob.glob(dir + "/**/*.html", recursive=True)

    with open(file_name, 'w') as writeFile:
        for file in files:
            f = open(file, 'r')
            writeFile.write(f.read())
            f.close()

if __name__ == '__main__':
    main()