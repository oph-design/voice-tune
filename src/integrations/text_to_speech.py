from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

def text_to_speech(text, filename):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by language code and name
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=input_text, 
        voice=voice, 
        audio_config=audio_config)

    # Write the response to the output file.
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{filename}"')
    # Load audio file
    audio = AudioSegment.from_file(filename, format="mp3")

    # Play audio file
    play(audio)

    