import os
from bardapi import Bard
from dotenv import load_dotenv
from LLMs import LLMs

class bardHandler(LLMs):
    def __init__(self, config, text):
        super().__init__(config, text)

        self.client = Bard(token=self.token)

        if not (self.token):
            raise Exception("Bard API Key não encontrada. Certifique-se de definir BARD_API_KEY em seu arquivo .env.")
        
    def _sendMessage(self):
        message = self.prompt + self.text
        client = self.client
        result = client.get_answer(f"{self.input_text} {self.prompt}")['content']

        return result
       
    def defineAnalysisType(self, analysisType, outputLanguage):
        if analysisType == "summarization":
            self.input_text = 'Summarize the following text into 150 words, making it easy to read and comprehend. The summary should be concise, clear, and capture the main points of the text. Avoid using complex sentence structures or technical jargon. Response language: %s and in "%s".' % ('%', outputLanguage) + " Text: "
        elif analysisType == "classification":
            self.input_text = "Situation: You function as a text classifier, receiving a text and providing only its tags. Without explaining or summary the text, just the tags. Response language: %s" % outputLanguage + " Text: "
