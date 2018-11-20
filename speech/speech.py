#!/usr/bin/env python3


import argparse
import binascii
import docopt
import os
import pygame
import random
import sys
import subprocess
import hashlib
# reload(sys)
# sys.setdefaultencoding('utf8')

from gtts import gTTS
# reload(sys)
# sys.setdefaultencoding('utf8')


def get_text_to_speech_file(text):
  hashstr = hashlib.md5(text.encode("utf-8")).hexdigest()
  tmp_file_path = '/tmp/{path}.mp3'.format(path = hashstr)
  if not os.path.isfile(tmp_file_path):
    tts = gTTS(text=text, lang="es")
    tts.save(tmp_file_path)
  return tmp_file_path


def reproduce_file(_file):
  subprocess.call(["cvlc", "--play-and-exit", _file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--text", type=str, help="Text to reproduce")
  parser.add_argument("-f", "--file", action="store_true", help="File to take random line and reproduce it")
  args = parser.parse_args()
  args = vars(args) 


  if args["text"]:
    text = args["text"]
    reproduce_file(get_text_to_speech_file(text))
    exit

  if args["file"]:
    topics = ["angel","luis","javi","jose","oscar","pani","chema","dani","carlos"]
    
    with open('./topics/' + random.choice(topics) + '.txt') as file:
      sentences = [line for line in file]
    audio_files = []
    for sentence in sentences:
      audio_files.append(get_text_to_speech_file(sentence))

    reproduce_file(random.choice(audio_files))
    exit
