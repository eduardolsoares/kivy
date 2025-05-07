import os
from dotenv import load_dotenv
import logging
from ..front.welcome import welcome
from ..front.colors import colors
from ..front.kivyDisplayer import KivyDisplayer
from .KivyAIClient import KivyAIClient


logging.basicConfig(
    filename="Kivy",
    level=logging.INFO
)

class Kivy:
    def __init__(self, args):
        self.args = args

        print(f"{colors["WARNING"]} [+] loading kivy model" if self.args.verbose else "")
        self.ai_client = self.loadClient()
        if self.args.display_image:
            self.displayer = KivyDisplayer(self.ai_client)
            return
        self.displayer = False


    def loadClient(self) -> KivyAIClient:
        """Returns a KivyAIClient instance."""
        load_dotenv()
        try:
           return KivyAIClient(api_key = os.environ.get("GROQ_API_KEY") or self.args.api_key)
        except Exception as e:
            print(f"{colors['FAIL']} [-] Couldn't load Groq model. Forgot to set the api key? {colors['ENDC']} \nError: {e}")
            exit()




    def start(self):
        """Boots up a Kivy instance."""
        os.system("cls" if os.name == "nt" else "clear")
        initial_response = self.ai_client.getResponse("kivy_personality")
        #output = welcome.replace("@eduardo!", self.styles.link("https://github.com/eduardolsoares", "@eduardo!"))
        print(f"{welcome}\n\n{initial_response}" if not self.args.display_image else "")

        if self.args.display_image:
            self.displayer.startMainMenu(response = initial_response)
        while True:
            inp = input("\n> ")
            intention = self.ai_client.interpretIntention(inp)
            print("intention: ", intention)
            response = self.ai_client.getResponse(intention = intention, user_input=inp)
            print(response)
