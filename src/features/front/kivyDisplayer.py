from blessed import Terminal
from .colors import colors
import pathlib
from ..ai.KivyAIClient import KivyAIClient
from ascii_magic import AsciiArt

class KivyDisplayer:
    def __init__(self, ai_client):
        self.path = str(pathlib.Path(__file__).parent.resolve())
        self.sprites = {
            'confused': self.path + '\\sprites/confused.png',
            'happy': self.path + '\\sprites/happy.png',
            'worried': self.path + '\\sprites/worried.png',
            'dreamy': self.path + '\\sprites/dreamy.png',
            'test': self.path + '\\sprites/test.png'
        }
        self.screen = Terminal()
        self.ai_client: KivyAIClient = ai_client

        self.loadMainScreen()


    def loadMainScreen(self):
        if not (self.screen.width >= 169 and self.screen.height >= 36):
            print(f"{colors['FAIL']}[-] The terminal must be at least 169x36 in order to run display mode. Current res: {self.screen.width}x{self.screen.height}{colors['ENDC']}")
            exit()
        print(self.screen.move_xy(100, 20) + '-' * (self.screen.width - 101), end='') #create main central line

        for i in range(self.screen.height):
            print(self.screen.move_xy(100, i) + '|', end='') #create left vertical line

    def get_input_inline(self):
        with self.screen.raw():
            input_str = ""
            while True:
                with self.screen.cbreak():
                    char = self.screen.inkey()
                if char.is_sequence:
                    if char.code == self.screen.KEY_ENTER:
                        break
                    elif char.code in (self.screen.KEY_BACKSPACE, self.screen.KEY_DELETE):
                        if len(input_str) > 0:
                            input_str = input_str[:-1]
                            print(self.screen.move_left(1) + " " + self.screen.move_left(1), end='', flush=True)
                else:
                    input_str += str(char)
                    print(char, end='', flush=True)
            return input_str


            
    def interpretEmotion(self, message: str):
        """TODO: interpret emotion and convert the specific sprite that conveys that emotion."""
        response = self.ai_client.generate([
            {"role": "system",
             "content": """
                        Considering the given message, interpret its emotion and classify it. There are two, and ONLY TWO, possible answers.
                        I want you to only reply with the emotion the message is conveying and nothing else. do not write explanations. do not write comments.
                        These are the ONLY POSSIBLE answer types, do not write something that's not on the list.
                        confused
                        dreamy
                        happy
                        worried

                        Reply with only the emotion and nothing else.
                        """
             },
             {"role": "user",
              "content": message}
        ])
        return response


    def display_text(self, response):
        with self.screen.location(101, 0):
            for line in self.screen.wrap(response, width=66, initial_indent = ' ', subsequent_indent = self.screen.move_right(102)):
                print(line)


    def display_emotion(self, emotion):
        with self.screen.location(0, 20):
            print(emotion)
            

        with self.screen.location(0, 0):
            AsciiArt.from_image(self.sprites[emotion]).to_terminal(columns=79)



    def startMainMenu(self, response):
        """Handles display mode inputting and screen design."""
        while True:
            with self.screen.location(101, 20):
                inp = self.get_input_inline()
                intention = self.ai_client.interpretIntention(inp)
                emotion = self.interpretEmotion(response)
                response = self.ai_client.getResponse(intention=intention, user_input=inp)
                self.display_emotion(emotion)
                self.display_text(response)
            