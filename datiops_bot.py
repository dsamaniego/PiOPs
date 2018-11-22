#!/usr/bin/env python3

import time
import telepot
from telepot.loop import MessageLoop
import json
import syslog
import argparse
import speech
import datetime

esperaMensaje = False

def lee_secretos(configfile):
  with open(configfile, 'r') as f:
    return json.load(f)


def escribeLog(texto):
  """
  Esta funcion escribe en log los mensajes de depuracion de este script recibidos como parametro
  """

  date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  syslog.syslog(texto)


def handle(msg):

  global esperaMensaje

  chat_id = str(msg['chat']['id'])
  comando = msg['text']
  nombre_usuario = msg['from']['first_name']
  #content_type, chat_type, chat_id = telepot.glance(msg)

  if chat_id not in secretos["authorized_ids"]:
    escribeLog("El usuario %s (%s) no esta autorizado" %(nombre_usuario, chat_id))
    speech.play_message("%s no está autorizado para enviarme mensajes" %nombre_usuario)
    return
  else:
    if comando == "/help":
      mensaje = """
      Estos son los comandos disponibles:

      - /text: para reproducir un mensaje en la raspberry de ops (después de ejecutar el comando se pedirá el mensaje a reproducir)
      - /random: para reproducir un mensaje aleatorio en la raspberry"
      """
    elif comando == "/start":
      escribeLog("El usuario %s (%s) ha iniciado chat con datiops_bot" %(nombre_usuario, chat_id))
      mensaje = 'Buenas %s!\nSoy el bot de Operaciones de DATIO. Ejecuta /help para saber los comandos que tienes disponibles. A disfrutarlos' %nombre_usuario
    elif comando == "/text":
      esperaMensaje = True
      mensaje = "Por favor, dime qué quieres reproducir en la raspberry:"
    elif esperaMensaje:
      esperaMensaje = False
      texto = comando
      speech.play_message(texto)
      escribeLog("El usuario %s (%s) ha enviado el mensaje '%s'" %(nombre_usuario, chat_id, texto))
      mensaje = "Mensaje reproducido"
    else:
      mensaje = "Ay %s, eres un lechón. Aprende a usar este bot ejecutando el comando /help anda" %nombre_usuario
    telegram.sendMessage(chat_id, mensaje)
    pass
  


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--config", required=True, help="Define el fichero json de configuracion del script")
  args = parser.parse_args()
  args = vars(args)
  
  secretos = lee_secretos(args["config"])
  telegram = telepot.Bot(secretos["token"])
  MessageLoop(telegram,handle).run_as_thread()

  while 1:
    secretos = lee_secretos(args["config"])
    time.sleep(300)

    
