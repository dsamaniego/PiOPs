#!/usr/bin/env python3


import argparse
import os, os.path
import random
import sys
import subprocess
import hashlib
from gtts import gTTS

topics = []

def get_text_hash(text):
  return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_topics(path):
  for root, dirs, files in os.walk(path):
    return files

def get_text_to_speech_file(text):
  hashstr = get_text_hash(text)
  tmp_file_path = '/tmp/{path}.mp3'.format(path=hashstr)
  if not os.path.isfile(tmp_file_path):
    tts = gTTS(text=text, lang="es")
    tts.save(tmp_file_path)
  return tmp_file_path

def reproduce_file(_file):
  subprocess.call(["cvlc", "--play-and-exit", _file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--text", type=str, help="Text to reproduce")
  parser.add_argument("-r", "--random", action="store_true", help="Reproduce random sentence from files in ./topics")
  parser.add_argument("-g","--generate", action="store_true", help="Generate mp3 files for precharged sentences")
  args = parser.parse_args()
  args = vars(args) 

  myself = os.path.abspath(sys.argv[0])
  dir = os.path.dirname(myself)

  if args["text"]:
    text = args["text"]
    reproduce_file(get_text_to_speech_file(text))
    exit

  if args["random"]:
    topics = get_topics(dir + '/topics')
    with open(dir + '/topics/' + random.choice(topics)) as file:
      sentences = [line for line in file]
    audio_files = []
    for sentence in sentences:
      audio_files.append(get_text_to_speech_file(sentence))

    reproduce_file(random.choice(audio_files))
    exit

  if args["generate"]:
    topics = get_topics(dir + '/topics')
    for topic in topics:
      with open(dir + '/topics/' + random.choice(topics)) as file:
        sentences = [line for line in file]
      for sentence in sentences:
        generated_file = get_text_to_speech_file(sentence)
        print ("Creating file %s..." %generated_file)
    exit

