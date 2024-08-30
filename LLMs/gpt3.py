from LLMs.LLMs import LLM
from openai import OpenAI
import logging

class ChatGptHandler(LLM):
    def __init__(self, config, text) -> None:
        super().__init__(config, text)
        self.client = OpenAI(api_key=self.token)
        
    def _send_message(self):
        message = self.prompt + self.text
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.3,
            top_p=0.9,
            top_k=50,
            max_tokens=self.max_output_tokens
        )
        
        self.summary = completion.choices[0].message.content

    def send_message(self):
        max_retries = 3
        for i in range(max_retries):
            try:
                self._send_message()
                break
            except Exception as e:
                logging.error(f"An error occurred during send_message: {str(e)}")
                logging.info(f"Retrying {i+1}/{max_retries} times ...")
                continue
        else:
            raise Exception("An error occurred during sendMessage")
    