import language_tool_python

# Load English grammar checker
tool = language_tool_python.LanguageTool('en-US')


def correct_text(text):
    """
    Correct grammar and spelling mistakes.

    Parameters:
        text (str): User input text

    Returns:
        str: Corrected text
    """

    try:
        corrected = tool.correct(text)
        return corrected

    except Exception as e:
        print("Grammar Error:", e)
        return text