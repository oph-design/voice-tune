from google.cloud import speech
import speech_recognition as sr

def transcribe_audio(speech_file):
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        input_audio = audio_file.read()

    audio = speech.RecognitionAudio(content=input_audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    print(response)
    for result in response.results:
        print(result.alternatives[0].transcript)

def speech_to_text():
    r = sr.Recognizer()
    r.energy_threshold = 3000

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        # return transcribe_audio(audio)
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        raise sr.UnknownValueError
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        raise sr.RequestError



# Replace 'path/to/audio/file' with the path to your audio file
# transcribe_audio('path/to/audio/file')