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


def get_random_sentence(topic):
  with open(dir + '/topics/' + topic) as file:
    sentences = [line for line in file]
  return random.choice(sentences)


def delete_cache():
  for root, dirs, files in os.walk('/tmp'):
    for file in files:
      if file.endswith(".mp3"):
        os.remove("/tmp/" + file)


def get_text_to_speech_file(text):
  hashstr = get_text_hash(text)
  tmp_file_path = '/tmp/{path}.mp3'.format(path=hashstr)
  if not os.path.isfile(tmp_file_path):
    tts = gTTS(text=text, lang="es")
    tts.save(tmp_file_path)
  return tmp_file_path


def reproduce_file(file):
  subprocess.call(["cvlc", "--play-and-exit", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def play_message(text):
  reproduce_file(get_text_to_speech_file(text))


def play_random(topic):
  filename = topic
  if filename in topics:
    reproduce_file(get_text_to_speech_file(get_random_sentence(filename)))
  else:
    print("Topic doesn't exist")


if __name__ == "__main__":
  myself = os.path.abspath(sys.argv[0])
  dir = os.path.dirname(myself)
  topics = get_topics(dir + '/topics')
  default_topic = random.choice(topics)

  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--text", type=str, help="Text to reproduce")
  parser.add_argument("-r", "--random", type=str, nargs="?", const=default_topic, help="Reproduce random sentence from ./topics/RANDOM. Without argument, reproduce random sentence from random topic")
  parser.add_argument("-l", "--list", action="store_true", help="List available topics")
  parser.add_argument("-c", "--clean_cache", action="store_true", help="Clean mp3 files in /tmp")
  args = parser.parse_args()
  args = vars(args) 


  if args["text"]:
    text = args["text"]
    play_message(text)
    exit

  if args["random"]:
    topic = args["random"]
    play_random(topic)
    exit
    
  if args["list"]:
    print ("This is the list of available topics:")
    print(topics)
    exit

  if args["clean_cache"]:
    delete_cache()
    exit


      
