import os
from bardapi import Bard
from dotenv import load_dotenv

class bardHandler():
    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        self.token = os.getenv("BARD_API_KEY")

        # Verifica se a chave da API foi encontrada
        if not (self.token):
            raise Exception("Bard API Key não encontrada. Certifique-se de definir BARD_API_KEY em seu arquivo .env.")
        
        # Inicializa o objeto Bard com a chave da API
        self.bard = Bard(token = self.token)
       
    def defineAnalysisType(self, analysisType, outputLanguage):
        if analysisType == "summarization":
            self.input_text = 'Summarize the following text into 150 words, making it easy to read and comprehend. The summary should be concise, clear, and capture the main points of the text. Avoid using complex sentence structures or technical jargon. Response language: %s and in "%s".' % ('%', outputLanguage) + " Text: "
        elif analysisType == "classification":
            self.input_text = "Situation: You function as a text classifier, receiving a text and providing only its tags. Without explaining or summary the text, just the tags. Response language: %s" % outputLanguage + " Text: "

    def get_bard_response(self, prompt):
        # Obtém a resposta da API Bard usando a instância já criada
        result = self.bard.get_answer(f"{self.input_text} {prompt}")['content']

        return result