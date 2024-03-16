from playsound import playsound 
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from googletrans import Translator 
from gtts import gTTS 
import os 
from tempfile import NamedTemporaryFile

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio.write_audiofile(audio_path)

def recognize_speech(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio_data, language='en-in')
        return query
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results: {e}")
        return None

def translate_text(query, to_lang_code):
    translator = Translator()
    translation = translator.translate(query, dest=to_lang_code)
    return translation.text

def main():
    video_path = "D:/Bluetooth/sample.mp4"
    audio_path = "D:/Bluetooth/audio_extracted.wav"
    translated_audio_path = "D:/Bluetooth/translated_audio.mp3"

    # Extract audio from the video
    extract_audio(video_path, audio_path)

    # Recognize speech from the extracted audio
    query = recognize_speech(audio_path)

    if query is None:
        return

    # Input destination language
    print("Enter the language to translate to (e.g., Hindi, English):")
    to_lang = input("Enter language: ").lower()

    # Mapping language name to its code
    language_codes = {
        'english': 'en',
        'hindi': 'hi'
        # Add more languages as needed
    }

    to_lang_code = language_codes.get(to_lang)
    if to_lang_code is None:
        print("Language not supported")
        return

    # Translate the recognized speech
    translated_text = translate_text(query, to_lang_code)
    
    # Convert translated text to speech
    translated_audio = gTTS(text=translated_text, lang=to_lang_code, slow=False)
    translated_audio.save(translated_audio_path)

    # Convert gTTS object to AudioSegment object
    #audio_segment = AudioSegment.from_mp3(translated_audio_path)

    # Play the translated audio
    playsound(translated_audio_path)

    # Clean up temporary files
    os.remove(audio_path)
    os.remove(translated_audio_path)

main()
