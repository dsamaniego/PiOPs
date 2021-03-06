#!/usr/bin/env python3


import argparse
import os, os.path
import random
import sys
import subprocess


class TeHablo:
  # PRIVATE FUNCTIONS
  
  def __init__(self, path_to=''):
    """
    Argument -> directory path of topics
    """
    if path_to == '':
      self.nodir = True
    else:
      self.nodir = False
      self.path_topics = os.path.abspath(path_to + "/topics")
      self.path_mp3 = os.path.abspath(path_to + "/mp3")
      self.__update_topics()
      self.__update_mp3()


  def __get_random_sentence(self, topic):
    if topic in self.topics:
      with open(self.path_topics + "/" + topic) as file:
        sentences = [line for line in file]
      return random.choice(sentences)
    else:
      print("Topic doesn't exist")
      return ""

  def __update_topics(self):
    for root, dirs, files in os.walk(self.path_topics):
      self.topics =  files


  def __update_mp3(self):
    for root, dirs, files in os.walk(self.path_mp3):
      self.mp3 =  files


  def __reproduce_file(self, file):
    subprocess.call(["cvlc", "--play-and-exit", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


  def __reproduce_text(self, text):
    url = "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=" + text.replace(" ","+").replace("\n","") + "&tl=es"
    subprocess.call(["cvlc", "--play-and-exit", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


  def get_topics(self):
    if self.nodir:
      raise ArgumentTypeError("Topics directory is not defined")
      return []
    self.__update_topics()
    return self.topics


  def get_mp3(self):
    if self.nodir:
      raise ArgumentTypeError("MP3 directory is not defined")
      return []
    self.__update_mp3()
    return self.mp3


  def play_message(self, text):
    self.__reproduce_text(text)


  def play_random(self, topic=''):
    if self.nodir:
      raise ArgumentTypeError("Topics directory is not defined")
    else:
      if topic in self.topics:
        self.__reproduce_text(self.__get_random_sentence(topic))
      else:
        print("Topic doesn't exist")


  def play_mp3(self, file):
    if self.nodir:
      raise ArgumentTypeError("Topics directory is not defined")
    else:
      if file in self.mp3:
        self.__reproduce_file(os.path.join(self.path_mp3,file))
      else:
        print("MP3 doesn't exist")




if __name__ == "__main__":
  mydir = os.path.dirname(os.path.abspath(sys.argv[0]))
  reproduce = TeHablo(mydir)
  default_topic = random.choice(reproduce.get_topics())

  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--text", type=str, help="Text to reproduce")
  parser.add_argument("-r", "--random", type=str, nargs="?", const=default_topic, help="Reproduce random sentence from ./topics/RANDOM. Without argument, reproduce random sentence from random topic")
  parser.add_argument("-l", "--list", action="store_true", help="List available topics")
  parser.add_argument("-m", "--mp3", type=str, help="MP3 file of list. User -l to see available mp3")
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
    print ("")
    print ("This is the list of available mp3:")
    print(reproduce.get_mp3())
    exit

  if args["mp3"]:
    reproduce.play_mp3(args["mp3"])
    exit
