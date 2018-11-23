#!/usr/bin/env python3


import argparse
import os, os.path
import random
import sys
import subprocess
import hashlib
from gtts import gTTS


class TeHablo:
  # PRIVATE FUNCTIONS
  
  def __init__(self, path_to_topics):
    """
    Argument -> directory path of topics
    """
    self.path_topics = os.path.abspath(path_to_topics)
    for root, dirs, files in os.walk(path_to_topics):
      self.topics =  files


  def __get_text_hash(self, text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


  def __get_random_sentence(self, topic):
    if topic in self.topics:
      with open(self.path_topics + "/" + topic) as file:
        sentences = [line for line in file]
      return random.choice(sentences)
    else:
      print("Topic doesn't exist")
      return ""
    

  def __get_text_to_speech_file(self, text):
    hashstr = self.__get_text_hash(text)
    tmp_file_path = '/tmp/{path}.mp3'.format(path=hashstr)
    if not os.path.isfile(tmp_file_path):
      tts = gTTS(text=text, lang="es")
      tts.save(tmp_file_path)
    return tmp_file_path


  def __reproduce_file(self, file):
    subprocess.call(["cvlc", "--play-and-exit", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)



  # PRIVATE FUNCTIONS
  
  def delete_cache(self):
    for root, dirs, files in os.walk('/tmp'):
      for file in files:
        if file.endswith(".mp3"):
          os.remove("/tmp/" + file)


  def get_topics(self):
    return self.topics


  def play_message(self, text):
    self.__reproduce_file(self.__get_text_to_speech_file(text))


  def play_random(self, topic):
    if topic in self.topics:
      self.__reproduce_file(self.__get_text_to_speech_file(self.__get_random_sentence(topic)))
    else:
      print("Topic doesn't exist")



if __name__ == "__main__":
  reproduce = TeHablo("./topics")
  default_topic = random.choice(reproduce.get_topics())

  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--text", type=str, help="Text to reproduce")
  parser.add_argument("-r", "--random", type=str, nargs="?", const=default_topic, help="Reproduce random sentence from ./topics/RANDOM. Without argument, reproduce random sentence from random topic")
  parser.add_argument("-l", "--list", action="store_true", help="List available topics")
  parser.add_argument("-c", "--clean_cache", action="store_true", help="Clean mp3 files in /tmp")
  args = parser.parse_args()
  args = vars(args) 


  if args["text"]:
    text = args["text"]
    reproduce.play_message(text)
    exit

  if args["random"]:
    topic = args["random"]
    reproduce.play_random(topic)
    exit
    
  if args["list"]:
    print ("This is the list of available topics:")
    print(reproduce.get_topics())
    exit

  if args["clean_cache"]:
    reproduce.delete_cache()
    exit


      
