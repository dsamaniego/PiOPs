#!/usr/bin/env python3

import time
import telepot
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from telepot.loop import MessageLoop
import json
import syslog
import os, os.path
import sys
import argparse
import speech
import random


secretos = {}
esperaMensaje = False
esperaRandom = False

def lee_secretos(configfile):
  global secretos
  with open(configfile, 'r') as f:
    return json.load(f)


def guarda_secretos(configfile):
  global secretos
  with open(configfile, 'w') as f:
    json.dump(secretos, f) 


def escribeLog(texto):
  syslog.syslog(texto)


def on_chat_message(msg):
  global esperaMensaje
  chat_id = str(msg['chat']['id'])
  comando = msg['text']
  nombre_usuario = msg['from']['first_name']
  
  keyboard = InlineKeyboardMarkup(inline_keyboard=[])

  if chat_id not in secretos["authorized_ids"]:
    escribeLog("El usuario %s (%s) no esta autorizado" %(nombre_usuario, chat_id))
    mensaje = "El usuario %s (%s) quiere usar @datiops_bot, para autorizarle pulsa el boton" %(nombre_usuario, chat_id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Autorizar', callback_data='authorize ' + chat_id)],])
    telegram.sendMessage("7404034",mensaje, reply_markup=keyboard)
    return
  else:
    if comando == "/help":
      mensaje = """
      Estos son los comandos disponibles:
      - /text: el texto que quieras reproducir en la raspberry (después de ejecutar el comando pregunta el texto a reproducir)
      - /random: para reproducir una frase aleatoria de los temas propuestos
      """

    elif comando == "/start":
      escribeLog("El usuario %s (%s) ha iniciado chat con datiops_bot" %(nombre_usuario, chat_id))
      mensaje = 'Buenas %s!\nSoy el bot de Operaciones de DATIO. Ejecuta /help para saber los comandos que tienes disponibles. A disfrutarlos' %nombre_usuario

    elif comando.startswith("/text "):
      reproduce.play_message(comando.split("/text ")[1])
      mensaje = "Mensaje reproducido"

    elif comando == "/text":
      esperaMensaje = True
      mensaje = "Por favor, dime qué quieres reproducir en la raspberry:"

    elif comando == "/random":
      esperaRandom = True
      temas = reproduce.get_topics()
      temas.sort()
      botones = []
      for item in temas:
        botones.append(InlineKeyboardButton(text=item, callback_data=item))
      columnas = [botones[i:i+2] for i in range(0,len(botones),2)]
      keyboard = InlineKeyboardMarkup(inline_keyboard=columnas)
      mensaje = "Por favor, elige uno de los siguientes temas:"

    elif esperaMensaje:
      esperaMensaje = False
      texto = comando
      # if texto.endswith(".mp3"):
      #   print(texto)
      #   reproduce.play_mp3(texto)
      # else:
      #   reproduce.play_message(texto)
      reproduce.play_message(texto)
      escribeLog("El usuario %s (%s) ha enviado el mensaje '%s'" %(nombre_usuario, chat_id, texto))
      mensaje = "Mensaje reproducido"

    else:
      mensaje = "Ay %s, eres un lechón. Aprende a usar este bot ejecutando el comando /help anda" %nombre_usuario
    telegram.sendMessage(chat_id, mensaje, reply_markup=keyboard)
    pass



def on_callback_query(msg):
  nombre_usuario = msg['from']['first_name']
  chat_id = str(msg['from']['id'])

  query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
  telegram.answerCallbackQuery(query_id, text='Mensaje reproducido')
  
  if query_data in reproduce.get_topics():
    reproduce.play_random(query_data)
    escribeLog("El usuario %s (%s) ha reproducido un mensaje aleatorio de %s" %(nombre_usuario, chat_id, query_data))
  elif "authorize" in query_data:
    nuevo_usuario = query_data.split(" ")[1]
    secretos["authorized_ids"].append(nuevo_usuario)
    guarda_secretos(args["config"])
    telegram.sendMessage("7404034", "Usuario autorizado")




if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--configfile", required=True, help="Define el fichero json de configuracion del script")
  args = parser.parse_args()
  args = vars(args)

  if os.path.islink(os.path.abspath(sys.argv[0])):
    mydir = os.path.dirname(os.readlink(sys.argv[0]))
  else:
    mydir = os.path.dirname(os.path.abspath(sys.argv[0]))
  reproduce = speech.TeHablo(mydir + "/topics")
  
  secretos = lee_secretos(args["configfile"])
  telegram = telepot.Bot(secretos["token"])
  MessageLoop(telegram, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

  while 1:
    secretos = lee_secretos(args["configfile"])
    time.sleep(60)
