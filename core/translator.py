from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

def translate_text(text, target_language):
    """
    Takes text and target language
    Returns translated text
    
    Supported languages:
    - 'ml' for Malayalam
    - 'hi' for Hindi
    - 'ta' for Tamil
    - 'en' for English
    """
    try:
        translator = GoogleTranslator(
            source='auto',
            target=target_language
        )
        
        # Split text into chunks if too long
        # GoogleTranslator has a 5000 char limit
        if len(text) > 4000:
            text = text[:4000]
        
        translated = translator.translate(text)
        return translated
    
    except Exception as e:
        return f"Translation error: {str(e)}"


def translate_to_malayalam(text):
    return translate_text(text, 'ml')


def translate_to_hindi(text):
    return translate_text(text, 'hi')


def translate_to_tamil(text):
    return translate_text(text, 'ta')


if __name__ == "__main__":
    test_text = "The tenant must pay rent of 15000 rupees before 5th of every month. Late payment penalty is 500 rupees per day."
    
    print("Original:", test_text)
    print("\nMalayalam:", translate_to_malayalam(test_text))
    print("\nHindi:", translate_to_hindi(test_text))