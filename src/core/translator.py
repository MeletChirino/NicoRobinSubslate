import ollama
from typing import List
from deep_translator import GoogleTranslator

class Translator:
    def __init__(self, model: str = "translategemma:12b"):
        self.model = model

    def translate_subtitle_track(self, content: str, title: str) -> str:
        """
        Translates an entire subtitle track while maintaining the SRT format using a
        Two-Stage Hybrid Architecture: Machine Translation followed by LLM Refinement.
        """
        # Stage 1 - Rapid Bulk Translation
        # Split based on double newlines which separates subtitle blocks in SRT
        blocks = content.strip().split('\n\n')
        processed_data = [] # List of (line_id, original_eng, rough_es)

        for block in blocks:
            lines = block.split('\n')
            # A standard SRT block has at least 3 lines: ID, Timestamp, Text
            if len(lines) >= 3 and lines[0].strip().isdigit():
                line_id = int(lines[0])
                source_text = "\n".join(lines[2:])

                try:
                    # Fast pass using GoogleTranslator
                    rough_translation = GoogleTranslator(source='en', target='es').translate(source_text)
                    processed_data.append((line_id, source_text, rough_translation))
                except Exception as e:
                    print(f"Error during initial translation for ID {line_id}: {e}")
                    # Fallback to original text if translator fails
                    processed_data.append((line_id, source_text, source_text))

        if not processed_data:
            return content

        # Stage 2 - Contextual Batch Refining (Ollama)
        final_translated_blocks = []
        batch_size = 40

        for i in range(0, len(processed_data), batch_size):
            batch = processed_data[i : i + batch_size]
            refined_result = self.refine_translation_batch(batch)
            final_translated_blocks.append(refined_result)

        return "\n\n".join(final_translated_blocks)

    def refine_translation_batch(self, batch_data: List[tuple]) -> str:
        """
        Refines a batch of rough translations using an LLM as a High-Context Editor.
        """
        # batch_data structure: [(line_id, "Eng text", "Rough Spanish text"), ...]
        payload_lines = []
        for line_id, eng, rough_es in batch_data:
            payload_lines.append(f"[{line_id}]\nEN: {eng}\nROUGH_ES: {rough_es}")

        payload = "\n\n".join(payload_lines)

        system_instructions = (
            "You are an elite Anime Localization Editor. You will receive a list of subtitle lines containing "
            "the original English text and a rough Spanish translation. Your job is to refine the Spanish text "
            "so it sounds natural, fluid, and hits the correct emotional tone for anime dialogue. "
            "Retain Japanese honorifics if present in the English source. "
            "Output ONLY the corrected Spanish text matching the structure `[ID] Clean Spanish Text`. "
            "Do NOT merge lines, skip lines, or include notes. Your output line count must exactly match the input."
        )

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_instructions},
                    {'role': 'user', 'content': payload}
                ],
                options={
                    'temperature': 0.2,       # Low temperature keeps it accurate but allows natural phrasing
                    'num_predict': 4096
                }
            )
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Ollama stage failed: {e}. Falling back to rough translation.")
            # Fallback logic: Return the raw translations for this batch if Ollama fails
            fallback_lines = []
            for line_id, _, rough_es in batch_data:
                fallback_lines.append(f"[{line_id}]\n{rough_es}")
            return "\n\n".join(fallback_lines)

if __name__ == "__main__":
    print("Translator class loaded with Hybrid Architecture.")
