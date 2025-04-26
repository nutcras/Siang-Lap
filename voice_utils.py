import os
import random
import wave
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyaudio

def record_audio(filename, duration=5):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                      rate=RATE, input=True,
                      frames_per_buffer=CHUNK)
    
    print("กำลังบันทึกเสียง...")
    frames = []
    
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("บันทึกเสียงเสร็จสิ้น")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def speech_to_text():
    recognizer = sr.Recognizer()
    base_dir = "voiceRecord"
    temp_dir = os.path.join(base_dir, "recordings")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file = os.path.join(temp_dir, f"temp_{random.randint(1000, 9999)}.wav")
    
    # บันทึกเสียง
    record_audio(temp_file)
    
    # แปลงเสียงเป็นข้อความ
    with sr.AudioFile(temp_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='th-TH')
            return text
        except sr.UnknownValueError:
            print("ไม่สามารถเข้าใจเสียง")
            return None

def record_and_convert_to_text(duration=5, sample_rate=16000):
    try:
        print("กำลังบันทึกเสียง...")
        recording = sd.rec(int(duration * sample_rate),
                          samplerate=sample_rate,
                          channels=1,
                          dtype='int16')
        
        sd.wait()
        
        temp_file = "temp_recording.wav"
        wav.write(temp_file, sample_rate, recording)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='th-TH')
            return text
    except Exception as e:
        print(f"ข้อผิดพลาดในการแปลงเสียง: {str(e)}")
        return None