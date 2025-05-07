from groq import Groq
import os
from prompts import get_message_prompt, get_commandline_prompt, check_command_safety_prompt, detect_command_type_prompt
from logging import log

class Kivy:
    def __init__(self):
        self.prompts = {
            'message': get_message_prompt,
            'commandline_creation': get_commandline_prompt,
            'check_safety': check_command_safety_prompt,
            'detect_command': detect_command_type_prompt,
            'kivy_personality': 1 #to implement yet
        }
        

    def load_env(self):
        self.key = os.environ.get("GROQ_API_KEY")


    def load_model(self): #probably using groq, but should look for a better alternative
        key = self.load_env()
        try:
            self.client = Groq(
                api_key=key
            )   
        except Exception as e:
            log(f"Couldn't load Groq model. {e}")


    def isShellCommand(self, command: str) -> str:
        """
        Generates the shell command to be executed based on context.
        """
        prompt: str = self.prompts['commandline_creation'].replace('{user_command}', command)
        response = self.client.chat.completions.create(messages=[{
            "role": "system",
            "content": prompt
            }], model="llama3-8b-8192")
        return response.choices[0].message.content
    
    def getResponse(self, context: str) -> str:
        """Generates the final response to the user"""
        personality: str = self.prompts['kivy_personality']
        response = self.client.chat.completions.create(messages=[{ 
            "role": "system",
            "content": personality
            }], model="llama3-8b-8192")
        return response.choices[0].message.content

    def isCommandSafe(self, cmd):
        check_safety: str = self.prompts['check_safety']
        response = self.client.chat.completions.create(messages=[{ 
            "role": "system",
            "content": check_safety 
            }], model="llama3-8b-8192")
        return response.choices[0].message.content

    def talk(self, message):
        """implements talking with google-TTS api."""
        pass
    

            
