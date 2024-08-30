from config.ProgramConfig import TextProcessingOption

class LLM:
    def __init__(self, config, text):
        self.config = config
        self.token = config.api_token
        self.prompt = self._choose_prompt()
        self.max_output_tokens = self._set_max_tokens()
        self.summary = None
        self.text = text

    def _set_max_tokens(self):
        max_output_tokens = 1000
        if self.config.text_processing_option == TextProcessingOption.classify:
            max_output_tokens = 10
        return max_output_tokens

    def _choose_prompt(self):
        if (self.config.text_processing_option == TextProcessingOption.summarize):
            return """
                Summarize the following text, making it easy to read and comprehend. 
                The summary should be concise, clear, and capture the main points of the text.
                Add clear headings and subheadings to guide the reader through each section.
                Avoid using complex sentence structures or technical jargon. 
                Ensure that the summary is written in the same language as the original text.
                Please begin by editing the following text: 
                """
        else:
            return """
                Read the text below and identify exactly three primary categories using
                a single word for each.
                Provide only the three tags that best categorize the text, and nothing else.
                Please begin by editing the following text:
                """

    def _send_message(self) -> str:
        # Subclasses should override this method
        raise NotImplementedError("Subclasses must implement _send_message() method.")

    def send_message(self) -> None:
        # before sending the message
        raise NotImplementedError("Subclasses must implement send_message method")

    def get_summary(self) -> str:
        return self.summary