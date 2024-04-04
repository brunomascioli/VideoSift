from openai import OpenAI
from LLMs import LLMs
import logging

class chatgptHandler(LLMs):
    def __init__(self, config, text):
        super().__init__(config, text)
        self.client = OpenAI(api_key=self.token)

    def _sendMessage(self):
        message = self.prompt + self.text
        client = self.client
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        self.summary = completion.choices[0].message.content

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
