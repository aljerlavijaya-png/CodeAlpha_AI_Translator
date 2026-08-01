from deep_translator import GoogleTranslator
from langdetect import detect


def translate_text(text, target_language):
    """
    Detects the source language and translates the text.

    Parameters:
        text (str): Text entered by the user
        target_language (str): Language code (e.g. te, hi, fr)

    Returns:
        tuple: (detected_language, translated_text)
    """

    try:
        # Detect source language
        source_language = detect(text)

        # Translate text
        translated = GoogleTranslator(
            source=source_language,
            target=target_language
        ).translate(text)

        return source_language, translated

    except Exception as e:
        return "Unknown", f"Translation Error: {str(e)}"