#!/usr/bin/env python

import speech_recognition as sr
import speech
import os, os.path
import sys

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#   print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

r = sr.Recognizer()
mic = sr.Microphone(device_index=7)

if os.path.islink(os.path.abspath(sys.argv[0])):
  mydir = os.path.dirname(os.readlink(sys.argv[0]))
else:
  mydir = os.path.dirname(os.path.abspath(sys.argv[0]))
reproduce = speech.TeHablo(mydir)

def callback(recognizer, audio):
  # received audio data, now we'll recognize it using Google Speech Recognition
  try:
    texto = recognizer.recognize_google(audio)
    print("Has dicho, " + texto)
    reproduce.play_message(texto)
  except sr.UnknownValueError:
    print('No entiendo.')
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))



with mic as source:
  r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
  audio = r.listen(source)
#stop_listening = r.listen_in_background(mic, callback)

texto = r.recognize_google(audio, language="es-ES")
print("Has dicho, " + texto)
reproduce.play_message(texto)
# if "*" in texto:
#   reproduce.play_message("No digas tacos, coño")
