#!/usr/bin/env python3

import time
import telepot
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


def handle(msg):
  global esperaMensaje
  separator = "auth="

  chat_id = str(msg['chat']['id'])
  comando = msg['text']
  nombre_usuario = msg['from']['first_name']

  if chat_id not in secretos["authorized_ids"]:
    escribeLog("El usuario %s (%s) no esta autorizado" %(nombre_usuario, chat_id))
    speech.play_message("%s no está autorizado para enviarme mensajes" %nombre_usuario)
    mensaje = "El usuario %s (%s) quiere usar @datiops_bot, para autorizarle envia auth=%s" %(nombre_usuario, chat_id, chat_id)
    telegram.sendMessage("7404034",mensaje)
    return
  else:
    if comando == "/help":
      mensaje = """
      Estos son los comandos disponibles:
      - /list:  para listar los temas disponibles para reproducir frases aleatoriamente
      - /text: el texto que quieras reproducir en la raspberry (después de ejecutar el comando pregunta el texto a reproducir)
      - /random: para ejecutar una frase aleatoria de un tema aleatorio
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
      escribeLog("El usuario %s (%s) ha reproducido un mensaje aleatorio" %(nombre_usuario, chat_id))
      reproduce.play_random(random.choice(reproduce.get_topics()))
      mensaje = "Mensaje reproducido"

    elif comando == "/list":
      mensaje = "Te puedo reproducir frases de cualquiera de estos temas: \n" + ", ".join(reproduce.get_topics())

    elif separator in comando:
      if chat_id == "7404034":
        nuevo_usuario = comando.split(separator)[1]
        secretos["authorized_ids"].append(nuevo_usuario)
        guarda_secretos(args["config"])
        escribeLog("Se ha autorizado al usuario %s (%s)" %(nombre_usuario,chat_id))
        mensaje = "Usuario autorizado"
      else:
        mensaje = "Estás intentando autorizar a un usuario pero tú tampoco estás autorizado"

    elif esperaMensaje:
      esperaMensaje = False
      texto = comando
      reproduce.play_message(texto)
      escribeLog("El usuario %s (%s) ha enviado el mensaje '%s'" %(nombre_usuario, chat_id, texto))
      mensaje = "Mensaje reproducido"

    else:
      mensaje = "Ay %s, eres un lechón. Aprende a usar este bot ejecutando el comando /help anda" %nombre_usuario
    telegram.sendMessage(chat_id, mensaje)
    pass
  


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
  MessageLoop(telegram,handle).run_as_thread()

  while 1:
    secretos = lee_secretos(args["configfile"])
    time.sleep(60)
