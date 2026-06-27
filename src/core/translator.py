import ollama
from typing import List

class Translator:
    def __init__(self, model: str = "translategemma:12b"):
        self.model = model

    def translate_subtitle_track(self, content: str, title: str) -> str:
        """
        Translates an entire subtitle track while maintaining the SRT format.
        The translator acts as an expert English-Spanish interpreter for anime.
        """
        system_prompt = (
            "You are an expert English-Spanish interpreter specializing in anime. "
            f"Translate the following subtitle track from English to Latin American Spanish. "
            f"The title of the anime is: {title}. "
            "Maintain the SRT format exactly, including timestamps and numbering. "
            "Ensure the translation sounds natural for a Latin American audience."
        )

        # Requesting translation via Ollama
        response = ollama.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': content},
            ]
        )
        return response['message']['content'].strip()

if __name__ == "__main__":
    # Example usage (for testing purposes)
    print("Translator class loaded.")

