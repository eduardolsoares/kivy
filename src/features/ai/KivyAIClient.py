from ..front.colors import colors
from groq import Groq
from subprocess import run
from .prompts import get_commandline_prompt, check_command_safety_prompt, kivy_personality, interpret_intention
from time import sleep
class KivyAIClient:
    """Manager for Kivy's AI operations."""
    def __init__(self, api_key):
        self.prompts = {
            'file_management': get_commandline_prompt,
            'check_safety': check_command_safety_prompt,
            'kivy_personality': kivy_personality,
            'interpret_intention': interpret_intention,
        }
        self.context = [{
            "role": "system",
            "content": self.prompts['kivy_personality']
        }]
        self.api_key = api_key
        self.load_model()



    def load_model(self): #probably using groq, but should look for a better alternative
        self.client = Groq(
            api_key=self.api_key) 
        
    def generate(self, messages=[]) -> str: 
        """uses self.context by default, unless messages is specified"""
        response = self.client.chat.completions.create(
            messages=self.context if not messages else messages,
            temperature = 1.3,
            max_tokens = 1024,
            model="llama3-8b-8192",
            top_p = 1,
            stream=True,
            stop=None)
        return ''.join(chunk.choices[0].delta.content for chunk in response if type(chunk.choices[0].delta.content) == str)

    def getResponse(self, intention: str, user_input="Hey! can you introduce yourself to me?") -> str:
        """Generates the final response to the user."""
        self.context.extend([{
            "role": "system",   
            "content": self.prompts[intention]
        }, {
            "role": "user",
            "content": user_input
        }]
        )
        response = self.generate()
        self.context.append({
            "role": "assistant",
            "content": response 
        })
        if intention == 'file_management':
            self.runCommands(response.strip('][').split(', '))   #<- transform list-like string into actual list
            return ''
        return response

    def runCommands(self, commands: list):
        """implements running the commands as subprocesses"""
        safety_level, reason = self.areCommandsSafe(commands)
        if safety_level == 'dangerous':
            print(f"{colors['WARNING']}[!] One or more commands that'll run might be dangerous. Run anyway? {colors['ENDC']}\n" 
                f"Commands: {''.join(command + '\n' for command in commands)}\n" 
                f"\nReason: {reason}")
            
            confirmation = input('(Y/N): ')
            while confirmation == '':
                confirmation = input('(Y/N): ')
            
            if confirmation not in ['Y', 'y', '']:
                self.start()     #   <- start over
        try:
            for command in commands:
                command = command.replace('"', '')
                run(f'powershell -command "{command}"' , shell=True)
                sleep(0.1)
        except Exception as e:
            print(f"{colors['FAIL']} an error occurred while running commands. {e} {colors['ENDC']}")

    def interpretIntention(self, message: str) -> str: 
        """Returns the intention behind the user's input.\n
        """
        response = self.generate(messages=[{ 
            "role": "system",
            "role": "system",
            "content": self.prompts['interpret_intention']
            },
            {
                "role": "user",
                "content": message
            }],
        )
        return response
    
    
    def areCommandsSafe(self, commands: list) -> tuple:
        check_safety: str = self.prompts['check_safety']
        response = self.generate(messages=[
            {
                "role": "system",
                "content": check_safety
            },
            {
                "role": "user",
                "content": ''.join(cmd for cmd in commands)
            }])
        safety_level, *reason = response #get reason in a single string
        reason = ''.join(word + ' ' for word in reason)

        return (safety_level, reason)