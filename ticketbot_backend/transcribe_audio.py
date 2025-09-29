import os
import wave
from dotenv import load_dotenv
from pydub import AudioSegment
from google.cloud import speech_v1 as speech

# ---- Load .env and set credentials ----
base_dir = os.path.dirname(__file__)
env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Set credentials directly to the file in this folder
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(base_dir, "old_ticketbot.json")

# ---- Helper: Convert input file to mono 16k WAV ----
def convert_to_mono(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(output_file, format="wav")
    print(f"[INFO] Converted {input_file} -> {output_file}")

# ---- Helper: Print sample rate ----
def print_sample_rate(wav_file):
    with wave.open(wav_file, "rb") as wf:
        sample_rate = wf.getframerate()
        print(f"[INFO] Sample rate: {sample_rate}")

# ---- Transcription ----
def transcribe_audio(input_file, language_code="mr-IN"):
    client = speech.SpeechClient()
    with open(input_file, "rb") as f:
        content = f.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"[Transcript]: {result.alternatives[0].transcript}")
        print(f"[Confidence]: {result.alternatives[0].confidence}")


if __name__ == "__main__":
    input_path = os.path.join(base_dir, "static", "upload_input_mono.wav")
    output_path = os.path.join(base_dir, "static", "upload_input_mono.wav")

    convert_to_mono(input_path, output_path)
    print_sample_rate(output_path)
    transcribe_audio(output_path, language_code="mr-IN")
