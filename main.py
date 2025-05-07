from src.features.ai.kivy import Kivy
from argparse import ArgumentParser
from signal import SIGINT, signal
import os

def handler(_, _1):
    os.system("cls" if os.name == "nt" else "clear")
    exit()

def main():
    signal(SIGINT, handler)
    parser = ArgumentParser(
        prog="Kivy",
        description="AI-driven desktop assistance"
    )
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    parser.add_argument('-display', '--display_image',
                        action='store_true')
    parser.add_argument('-key', '--api_key')
    args = parser.parse_args()
    kivy = Kivy(args)
    kivy.start()



if __name__ == '__main__':
    main()
