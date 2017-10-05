import sys
import os


kukulkan_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan_path, 'python')


sys.path.append(py_kukulkan)


import kukulkan.gui.config.writter as _writter
import kukulkan.gui.config.reader as _reader


def main():
    import time
    config = _reader.ConfigReader('ui')
    while True:
        try:
            time.sleep(.01)
        except KeyboardInterrupt:
            sys.exit('Stopped execution of config test.')


if __name__ == '__main__':
    main()
