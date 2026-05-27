from gtts import gTTS
import os

def text_to_speech(text, language='en', filename='output.mp3'):
    """
    Converts text to speech and saves as mp3
    
    Languages:
    - 'en' for English
    - 'ml' for Malayalam  
    - 'hi' for Hindi
    - 'ta' for Tamil
    """
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    test_text = "This rental agreement requires you to pay 15000 rupees before the 5th of every month."
    
    print("Generating English audio...")
    text_to_speech(test_text, 'en', 'test_english.mp3')
    print("Done. Check test_english.mp3")
    
    print("Generating Malayalam audio...")
    text_to_speech("വാടകക്കാരൻ എല്ലാ മാസവും 5-ന് മുമ്പ് 15000 രൂപ വാടക നൽകണം.", 'ml', 'test_malayalam.mp3')
    print("Done. Check test_malayalam.mp3")