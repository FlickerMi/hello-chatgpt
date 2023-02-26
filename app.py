import pvporcupine
import struct
import pyaudio
import pvcobra
import time
import os
import speech_recognition as sr
from agent import chatGPTAgent as gpt
from agent import speechAgent as speech
from utils.logger import logger

porcupine = None
pa = None
audio_stream = None
r = sr.Recognizer()


def picovoice():
    picovoice_access_key = ''
    porcupine = pvporcupine.create(
        access_key=picovoice_access_key,
        keyword_paths=['hi-chat_en_mac_v2_1_0.ppn']
    )
    pa = pyaudio.PyAudio()
    cobra = pvcobra.create(picovoice_access_key)
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        #
        _pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(_pcm)
        if keyword_index >= 0:
            os.system(f'say -v "Mei-Jia" "a"')
            run()


def chatGPT(text):
    if len(text) == 0:
        return
    text = text.replace('\n', ' ').replace('\r', '').strip()
    logger.info(f'Q: {text}')
    res = gpt.ask(text)
    logger.info(f'A: {res}')
    return res


def run():
    # logger.info('start recognize_from_microphone')
    logger.info('speak into your microphone')
    q = speech.recognize_from_microphone()
    # logger.info(f'recognize_from_microphone, text={q}')
    res = chatGPT(q)
    # os.system(f'say -v "Mei-Jia" "{res}"')
    speech.tts(res)
    # run()


picovoice()
