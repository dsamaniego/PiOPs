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


def handle(msg):
  global esperaMensaje
  separator = "auth="
  print(msg)
  chat_id = str(msg['chat']['id'])
  comando = msg['text']
  nombre_usuario = msg['from']['first_name']
  
  keyboard = InlineKeyboardMarkup(inline_keyboard=[])

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
      esperaRandom = True
      temas = reproduce.get_topics()
      #escribeLog("El usuario %s (%s) ha reproducido un mensaje aleatorio" %(nombre_usuario, chat_id))
      #reproduce.play_random(random.choice(reproduce.get_topics()))
      mensaje = "Por favor, elige uno de los siguientes temas:"
      botones = []
      for item in temas:
        botones.append([InlineKeyboardButton(text=item, callback_data=item)])
      #cachopos = [botones[i:i+2] for i in range(0,len(botones),2)]
      keyboard = InlineKeyboardMarkup(inline_keyboard=botones)
    

# keyboard = InlineKeyboardMarkup(inline_keyboard=[
# 		[InlineKeyboardButton(text=str(result[0][1]), callback_data=result[0][0]),InlineKeyboardButton(text=str(result[1][1]), callback_data=result[1][0])],
# 		[InlineKeyboardButton(text=str(result[2][1]), callback_data=result[2][0]),InlineKeyboardButton(text=str(result[3][1]), callback_data=result[3][0])],
# 		[InlineKeyboardButton(text=str(result[4][1]), callback_data=result[4][0]),InlineKeyboardButton(text=str(result[5][1]), callback_data=result[5][0])],
# 		[InlineKeyboardButton(text=str(result[6][1]), callback_data=result[6][0]),InlineKeyboardButton(text=str(result[7][1]), callback_data=result[7][0])],
# 		[InlineKeyboardButton(text=str(result[8][1]), callback_data=result[8][0]),InlineKeyboardButton(text=str(result[9][1]), callback_data=result[9][0])],
# 		[InlineKeyboardButton(text='10 previous', callback_data=next)],
# 		])

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
      if texto.endswith(".mp3"):
        reproduce.play_mp3(texto)
      else:
        reproduce.play_message(texto)
      escribeLog("El usuario %s (%s) ha enviado el mensaje '%s'" %(nombre_usuario, chat_id, texto))
      mensaje = "Mensaje reproducido"

    elif esperaRandom:
      esperaRandom = False

    else:
      mensaje = "Ay %s, eres un lechón. Aprende a usar este bot ejecutando el comando /help anda" %nombre_usuario
    telegram.sendMessage(chat_id, mensaje, reply_markup=keyboard)

    #telegram.answerCallbackQuery
    pass



async def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

    reproduce.play_random(data)
    # if data == 'notification':
    #     await telegram.answerCallbackQuery(query_id, text='Notification at top of screen')
    # elif data == 'alert':
    #     await telegram.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
    # elif data == 'edit':
    #     global message_with_inline_keyboard

    #     if message_with_inline_keyboard:
    #         msg_idf = telepot.message_identifier(message_with_inline_keyboard)
    #         await telegram.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
    #     else:
    #         await telegram.answerCallbackQuery(query_id, text='No previous message to edit')




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
  #MessageLoop(telegram,handle).run_as_thread()
  MessageLoop(telegram, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

  while 1:
    secretos = lee_secretos(args["configfile"])
    time.sleep(60)
