from LLMs.LLMs import LLM
import google.generativeai as genai  
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import logging

class GeminiHandler(LLM):
    def __init__(self, config, text) -> None:
        super().__init__(config, text)
        self.client = genai.configure(api_key=self.token)

    def _send_message(self):
        generation_config = genai.GenerationConfig(   
            temperature=0.3,
            top_p=0.9,
            top_k=50,
            max_output_tokens=self.max_output_tokens
        )
  
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        model = genai.GenerativeModel('models/gemini-1.5-pro')
        
        response = model.generate_content(f'{self.prompt} {self.text}', generation_config=generation_config, safety_settings=safety_settings)

        self.summary = response.text
        
    def send_message(self):
        try:
            self._send_message()
        except Exception as e:
            logging.error(f"An error occurred during send_message: {str(e)}")