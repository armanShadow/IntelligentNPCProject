from dotenv import load_dotenv
from openai import OpenAI
import pyaudio
import wave

class SpeechTextTranslator(object):
    def translate_speech_to_text(self, speech_file_path):
        client = OpenAI()
        speech_file = open(speech_file_path, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=speech_file,
            response_format="text"
        )
        return transcription
    
    def translate_text_to_speech(self, text):
        client = OpenAI()
        speech_file_path = "output.wav"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
            response_format ="wav"
        )
        response.write_to_file(speech_file_path)
        return speech_file_path

    def record_speech(self, seconds=3):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 2
        rate = 44100
        speech_file_path = "input.wav"

        audio = pyaudio.PyAudio()

        print("Start Recording")

        stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []

        for i in range(0, int(rate / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        print("Stop Recording")

        wav_file = wave.open(speech_file_path, 'wb')
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(audio.get_sample_size(format))
        wav_file.setframerate(rate)
        wav_file.writeframes(b''.join(frames))
        wav_file.close()
        return speech_file_path
    
    def play_speech(self, speech_file_path):
        chunk = 1024

        wav_file = wave.open(speech_file_path, 'rb')

        audio = pyaudio.PyAudio()

        stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                        channels=wav_file.getnchannels(),
                        rate=wav_file.getframerate(),
                        output=True)

        data = wav_file.readframes(chunk)

        while data != b'':
            stream.write(data)
            data = wav_file.readframes(chunk)

        stream.close()
        audio.terminate()
    
    def record_speech_as_text(self, seconds=3):
        speech_file_path = self.record_speech(seconds)
        return self.translate_speech_to_text(speech_file_path)
    
    def play_speech_from_text(self, text):
        speech_file_path = self.translate_text_to_speech(text)
        self.play_speech(speech_file_path)