from LLMs.LLMs import LLM
import google.generativeai as genai  
import logging

class GeminiHandler(LLM):
    def __init__(self, config, text) -> None:
        super().__init__(config, text)
        self.client = genai.configure(api_key=self.token)
        self.sendMessage()

    def getSummary(self):
        return self.summary

    def _sendMessage(self):
        generation_config = {
            "temperature":0,
            "top_p":1,
            "top_k":1,
            "max_output_tokens": 1000
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(f'{self.prompt} {self.text}', stream=True)

        for chunk in response:
            self.summary += chunk.text 


    def sendMessage(self):
        self._sendMessage()
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