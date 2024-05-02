class LLM:
    def __init__(self, config, text):
        self.token = config.api_token
        self.prompt = 'Summarize the following text, making it easy to read and comprehend. The summary should be concise, clear, and capture the main points of the text. Avoid using complex sentence structures or technical jargon. Please begin by editing the following text: '
        self.summary = ''
        self.text = text

    def _sendMessage(self):
        # Subclasses should override this method
        raise NotImplementedError("Subclasses must implement _sendMessage() method.")

    def sendMessage(self):
        # before sending the message
        self._sendMessage()