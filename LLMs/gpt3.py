from LLMs.LLMs import LLM
from openai import OpenAI
import logging

class ChatgptHandler(LLM):
    def __init__(self, config, text) -> None:
        super().__init__(config, text)
        self.client = OpenAI(api_key=self.token)
        self.summary = None
        self.sendMessage()
        
    def _sendMessage(self):
        message = self.prompt + self.text
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": message}
            ]
        )
        self.summary = completion.choices[0].message.content

    def getSummary(self):
        return self.summary

    def sendMessage(self):
        max_retries = 3
        for i in range(max_retries):
            try:
                self._sendMessage()
                break
            except Exception as e:
                logging.error(f"An error occurred during sendMessage: {str(e)}")
                logging.info(f"Retrying {i+1}/{max_retries} times ...")
                continue
        else:
            raise Exception("An error occurred during sendMessage")