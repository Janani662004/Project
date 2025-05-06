import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import torch
import torchaudio
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2Processor
import os

# ========== RECORD AUDIO ==========
def record_audio(filename="live_audio.wav", duration=5, fs=16000):
    print(f"🎙️ Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(filename, fs, audio)
    print("✅ Recording complete.")

# ========== LOAD MODEL ==========
model_path = r"D:\ja\Models\wav2vec2"  # update if needed
processor = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path)
model.eval()

# ========== PREDICT EMOTION ==========
def predict_emotion(audio_path):
    speech, rate = torchaudio.load(audio_path)
    if rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=rate, new_freq=16000)
        speech = resampler(speech)
    
    inputs = processor(speech.squeeze(), sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = torch.argmax(logits).item()
    scores = torch.nn.functional.softmax(logits, dim=1)[0]
    
    labels = model.config.id2label
    sorted_scores = sorted(zip(labels.values(), scores), key=lambda x: x[1], reverse=True)

    print("\n🎯 Top Predicted Emotions:")
    for label, score in sorted_scores[:3]:
        print(f"  {label:<15} : {score:.4f}")

# ========== RUN ==========
if __name__ == "__main__":
    audio_file = "live_audio.wav"
    record_audio(audio_file, duration=8)  # change duration if needed
    predict_emotion(audio_file)