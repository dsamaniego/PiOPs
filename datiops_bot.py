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
import hashlib


secretos = {}
esperaMensaje = False
to_superadmin = False
superadmin = "7404034"
aprobado = ""
moderacion = {}

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
  print(texto)
  # telegram.sendMessage(superadmin, texto, disable_notification=True)


def teclado_usuarios(callback_str):
  botones = []
  for item in secretos["authorized_ids"]:
    botones.append(InlineKeyboardButton(text=telegram.getChat(item)["first_name"], callback_data=callback_str + item))
  columnas = [botones[i:i+2] for i in range(0,len(botones),2)]
  return InlineKeyboardMarkup(inline_keyboard=columnas)


def mensaje_para_admins(mensaje, keyboard=[]):
  for admin in secretos["admin"]:
    telegram.sendMessage(admin, mensaje, reply_markup=keyboard)


def estado_moderacion():
  if secretos["moderation_mode"]:
    return "La moderacion de mensajes esta ACTIVADA"
  else:
    return "La moderacion de mensajes esta DESACTIVADA"


def get_hash_texto(texto):
  return hashlib.md5(texto.encode("utf-8")).hexdigest()


def get_text_from_hash(hash_texto):
  for item in moderacion.keys():
    for i in moderacion[item]:
      if i[0] == hash_texto:
        return i[1]


def hash_already_exists(chat_id, hash_texto):
  # print(moderacion)
  try:
    if (hash_texto, get_text_from_hash(hash_texto)) in moderacion[chat_id]:
      return True
    else:
      return False
  except KeyError:
    return False

def delete_text(chat_id, hash_texto):
  moderacion[chat_id].remove((hash_texto, get_text_from_hash(hash_texto)))


def on_chat_message(msg):
  global esperaMensaje
  global to_superadmin
  
  chat_id = str(msg['chat']['id'])
  comando = msg['text']
  nombre_usuario = msg['from']['first_name']
  
  keyboard = InlineKeyboardMarkup(inline_keyboard=[])

  # print("CHAT_ID: " + chat_id)
  # print("NOMBRE_USUARIO: "+ nombre_usuario)
  # print("COMANDO: " + comando)

  if chat_id not in secretos["authorized_ids"]:
    escribeLog("El usuario %s (%s) no esta autorizado" %(nombre_usuario, chat_id))
    mensaje = "El usuario %s (%s) quiere usar @datiops_bot, para autorizarle pulsa el boton" %(nombre_usuario, chat_id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Autorizar', callback_data='authorize.' + chat_id)],])
    mensaje_para_admins(mensaje, keyboard)
    return
  else:
    if comando == "/help":
      mensaje = """
      Estos son los comandos disponibles:
      - /text: el texto que quieras reproducir en la raspberry (después de ejecutar el comando pregunta el texto a reproducir)
      - /random: para reproducir una frase aleatoria de los temas propuestos
      - /mp3: para reproducir uno de los mp3 propuestos
      - /admin: solo para administradores
      """

    elif comando == "/start":
      escribeLog("El usuario %s (%s) ha iniciado chat con datiops_bot" %(nombre_usuario, chat_id))
      mensaje = 'Buenas %s!\nSoy el bot de Operaciones de DATIO. Ejecuta /help para saber los comandos que tienes disponibles. A disfrutarlos' %nombre_usuario

    # elif comando.startswith("/text "):
    #   reproduce.play_message(comando.split("/text ")[1])
    #   mensaje = "Mensaje reproducido"

    elif comando == "/text":
      esperaMensaje = True
      mensaje = "Por favor, dime qué quieres reproducir en la raspberry:"

    elif comando == "/random":
      temas = reproduce.get_topics()
      temas.sort()
      botones = []
      for item in temas:
        botones.append(InlineKeyboardButton(text=item, callback_data=item))
      columnas = [botones[i:i+2] for i in range(0,len(botones),2)]
      keyboard = InlineKeyboardMarkup(inline_keyboard=columnas)
      mensaje = "Por favor, elige uno de los siguientes temas:"

    elif comando == "/mp3":
      mp3 = reproduce.get_mp3()
      mp3.sort()
      botones = []
      for item in mp3:
        botones.append([InlineKeyboardButton(text=item, callback_data=item)])
      keyboard = InlineKeyboardMarkup(inline_keyboard=botones)
      mensaje = "Por favor, elige uno de los siguientes mp3:"

    elif comando == "/admin":
      if chat_id not in secretos["admin"]:
        mensaje = "Lo siento pero no eres un usuario administrador. Pase por caja para aumentar tus privilegios https://www.paypal.me/ohermosa"
        escribeLog ("El usuario %s (%s) ha intentado ejecutar el comando '/admin'" %(nombre_usuario, chat_id))
      else:
        mensaje = "Elige qué quieres hacer:"
        botones = [[InlineKeyboardButton(text="Ver autorizados", callback_data="authorized"), InlineKeyboardButton(text="Bannear", callback_data="ban")],
          [InlineKeyboardButton(text="Ver administradores", callback_data="ver_admin"), InlineKeyboardButton(text="Nuevo admin", callback_data="new_admin")],
          [InlineKeyboardButton(text="Moderation STATUS", callback_data="moderation_status"), InlineKeyboardButton(text="Moderation MODE", callback_data="moderation_mode")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=botones)

    elif esperaMensaje:
      esperaMensaje = False
      texto = comando
      hash_texto = get_hash_texto(texto)
      if secretos["moderation_mode"]:
        if chat_id not in moderacion.keys():
          moderacion[chat_id] = [(hash_texto, texto)]
        elif chat_id in moderacion.keys() and not hash_already_exists(chat_id, hash_texto):
          moderacion[chat_id].append((hash_texto, texto))
        elif chat_id in moderacion.keys() and hash_already_exists(chat_id, hash_texto):
          print ("El usuario %s (%s) insiste en reproducir la misma frase" %(nombre_usuario, chat_id))
      
        mensaje = "%s quiere enviar el siguiente mensaje: '%s'. Permitir?" %(nombre_usuario, texto)
        botones = [[InlineKeyboardButton(text="SÍ", callback_data="authmsgyes_" + chat_id + "_" + hash_texto), InlineKeyboardButton(text="NO", callback_data="authmsgno_" + chat_id + "_" + hash_texto)]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=botones)
        to_superadmin = True
        
      else:
        reproduce.play_message(texto)
        escribeLog("El usuario %s (%s) ha enviado el mensaje '%s'" %(nombre_usuario, chat_id, texto))
        mensaje = "Mensaje reproducido"

    else:
      mensaje = "Ay %s, eres un lechón. Aprende a usar este bot ejecutando el comando /help anda" %nombre_usuario
    
    if to_superadmin:
      telegram.sendMessage(superadmin, mensaje, reply_markup=keyboard)
      to_superadmin = False
    else:
      telegram.sendMessage(chat_id, mensaje, reply_markup=keyboard)
    



def on_callback_query(msg):
  nombre_usuario = msg['from']['first_name']
  chat_id = str(msg['from']['id'])
  query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

  if query_data in reproduce.get_topics():
    reproduce.play_random(query_data)
    telegram.answerCallbackQuery(query_id, text='Mensaje reproducido')
    escribeLog("El usuario %s (%s) ha reproducido un mensaje aleatorio de %s" %(nombre_usuario, chat_id, query_data))

  elif query_data in reproduce.get_mp3():
    reproduce.play_mp3(query_data)
    telegram.answerCallbackQuery(query_id, text='MP3 reproducido')
    escribeLog("El usuario %s (%s) ha reproducido el mp3 %s" %(nombre_usuario, chat_id, query_data))

  elif "authorize." in query_data:
    nuevo_usuario = query_data.split("authorize.")[1]
    if nuevo_usuario in secretos["authorized_ids"]:
      mensaje = "El usuario %s (%s) ya estaba autorizado" %(telegram.getChat(nuevo_usuario)["first_name"], nuevo_usuario)
    else:
      secretos["authorized_ids"].append(nuevo_usuario)
      guarda_secretos(args["configfile"])
      escribeLog("Se ha autorizado al usuario %s a usar el bot" %nuevo_usuario)
      mensaje = "El usuario %s (%s) ha sido autorizado" %(telegram.getChat(nuevo_usuario)["first_name"], nuevo_usuario)
    telegram.answerCallbackQuery(query_id, text=mensaje)
    mensaje_para_admins(mensaje)

  elif query_data == "authorized":
    mensaje = "Ahora mismo hay estos usuarios autorizados:\n"
    for usuario in secretos["authorized_ids"]:
      mensaje = mensaje + telegram.getChat(usuario)["first_name"] + "\n"
    telegram.answerCallbackQuery(query_id, text='Se ha mostrado la lista de usuarios autorizados')
    telegram.sendMessage(chat_id, mensaje)

  elif query_data == "ban":
    keyboard = teclado_usuarios("ban.")
    mensaje = "Elige que usuario quieres bannear:"
    telegram.sendMessage(chat_id, mensaje, reply_markup=keyboard)

  elif "ban." in query_data:
    to_ban = query_data.split("ban.")[1]
    if to_ban not in secretos["authorized_ids"]:
      mensaje = "El usuario %s (%s) ya no estaba en la lista de usuarios autorizados" %(telegram.getChat(to_ban), to_ban)
    else:
      secretos["authorized_ids"].remove(to_ban)
      if to_ban in secretos["admin"]:
        secretos["admin"].remove(to_ban)
      guarda_secretos(args["configfile"])
      escribeLog ("El usuario %s (%s) ha baneado al usuario %s (%s)" %(nombre_usuario, chat_id, telegram.getChat(to_ban)["first_name"], to_ban))
    telegram.answerCallbackQuery(query_id, mensaje)
    mensaje_para_admins(mensaje)
  
  elif query_data == "new_admin":
    mensaje = "Elije cual de estos usuarios quieres convertirlo en administrador:"
    keyboard = teclado_usuarios("newadmin.")
    telegram.sendMessage (chat_id, mensaje, reply_markup=keyboard)
  
  elif query_data == "ver_admin":
    mensaje = "Ahora mismo hay estos usuarios administradores:\n"
    for usuario in secretos["admin"]:
      mensaje = mensaje + telegram.getChat(usuario)["first_name"] + "\n"
    telegram.answerCallbackQuery(query_id, text='Se ha mostrado la lista de usuarios administradores')
    telegram.sendMessage(chat_id, mensaje)    

  elif "newadmin." in query_data:
    to_admin = query_data.split("newadmin.")[1]
    if to_admin in secretos["admin"]:
      mensaje = "El usuario %s (%s) ya es administrador" %(telegram.getChat(to_admin)["first_name"], to_admin)
    else:
      secretos["admin"].append(to_admin)
      guarda_secretos(args["configfile"])
      mensaje = "Se ha convertido en administrador al usuario %s (%s)" %(telegram.getChat(to_admin)["first_name"], to_admin)
      escribeLog ("El usuario %s (%s) ha convertido en admin al usuario %s (%s)" %(nombre_usuario, chat_id, telegram.getChat(to_admin)["first_name"], to_admin))
      telegram.sendMessage(to_admin,"Ya eres administrador del bot, recuerda: __'un gran poder conlleva una gran responsabilidad__'")
    telegram.answerCallbackQuery(query_id, text=mensaje)
    mensaje_para_admins(mensaje)

  elif query_data == "moderation_status":
    mensaje = estado_moderacion()
    telegram.answerCallbackQuery(query_id, text=mensaje)
  
  elif query_data == "moderation_mode":
    secretos["moderation_mode"] = not secretos["moderation_mode"]
    guarda_secretos(args["configfile"])
    mensaje = estado_moderacion()
    telegram.answerCallbackQuery(query_id, text=mensaje)
    if chat_id != superadmin:
      telegram.sendMessage(superadmin, mensaje)
    escribeLog ("El usuario %s (%s) ha cambiado el modo moderación" %(nombre_usuario, chat_id))

  elif "authmsgyes_" in query_data:
    telegram.answerCallbackQuery(query_id, "Mensaje aceptado")
    usuario = query_data.split("_")[1]
    hash_texto = query_data.split("_")[2]
    texto = get_text_from_hash(hash_texto)
    if hash_already_exists(usuario, hash_texto):
      reproduce.play_message(texto)
      telegram.sendMessage(usuario, "Mensaje reproducido")
      delete_text(usuario, hash_texto)
      escribeLog("El usuario %s (%s) ha enviado el mensaje '%s' y ha sido aprobado por el superadmin" %(telegram.getChat(usuario)["first_name"], usuario, texto))
    else:
      telegram.sendMessage(superadmin, "Este mensaje ya ha sido procesado")
    
  elif "authmsgno_" in query_data:
    telegram.answerCallbackQuery(query_id, "Mensaje denegado")
    usuario = query_data.split("_")[1]
    hash_texto = query_data.split("_")[2]
    if hash_already_exists(usuario, hash_texto):
      telegram.sendMessage(usuario, "Dios no ha aprobado tu mensaje, anda y que te den por culo")
      delete_text(usuario, hash_texto)
      escribeLog("El usuario %s (%s) ha enviado el mensaje '%s' pero no ha sido aprobado por el superadmin" %(telegram.getChat(usuario)["first_name"], usuario, get_text_from_hash(hash_texto)))
    else:
      telegram.sendMessage(superadmin, "Este mensaje ya ha sido procesado")
      


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--configfile", required=True, help="Define el fichero json de configuracion del script")
  args = parser.parse_args()
  args = vars(args)

  if os.path.islink(os.path.abspath(sys.argv[0])):
    mydir = os.path.dirname(os.readlink(sys.argv[0]))
  else:
    mydir = os.path.dirname(os.path.abspath(sys.argv[0]))
  reproduce = speech.TeHablo(mydir)
  
  secretos = lee_secretos(args["configfile"])
  # print (secretos)
  telegram = telepot.Bot(secretos["token"])
  MessageLoop(telegram, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

  while 1:
    secretos = lee_secretos(args["configfile"])
    time.sleep(10)
