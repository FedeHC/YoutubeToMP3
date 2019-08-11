#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

if __name__ != "__main__":
  try:
    import sys
    # Comprobar que se ejecutra el script desde Python >=3.5:
    assert sys.version_info >= (3, 5), "ERROR: el programa debe ejecutarse desde Python 3.5 o superior."

    # Youtube_dl:
    import youtube_dl

    # Tkinter:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox

    # Otros módulos necesarios:
    import os, threading, time, queue, platform, subprocess
    from pathlib import Path


  except AssertionError as e:
    print("\n{0}\n".format(e))
    sys.exit()  # Forzando finalización del programa.

  except ImportError as e:
    print("\n# ERROR: Hubo problemas al cargar módulos.\n- MENSAJE: {0}".format(e))
    print(e, "\n")
    sys.exit()  # Forzando finalización del programa.

  
  # Si no hubo problemas, se continua con la carga de las clases auxiliares:

  class MyLogger(object):
    """Clase para poder recibir mensajes de error desde youtube_dl."""

    def debug(self, msg):
      """Método debug (no usado)."""
      pass


    def warning(self, msg):
      """Método warning (no usado)."""
      pass


    def error(self, msg):
      """Método error, para mostrar mensaje de error en consola."""
      print(msg)

  # Diccionario con la configuración para la conversión del video a mp3 con youtube_dl
  # Este dicc. debe ir DESPUES de definir la clase MyLogger.
  # Más info:  https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
  ytdl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
      "key": "FFmpegExtractAudio",
      "preferredcodec": "mp3",
      "preferredquality": "320",
    }],
    "logger": MyLogger(),
  }


  class Hook(threading.Thread):
    """Clase para ejecutar Youtube_dl hook en un thread aparte."""

    def __init__(self, queue, ytdl_opts, url):

      # Invocando constructor padre:
      threading.Thread.__init__(self)
      
      # Variables principales:
      self.queue = queue
      self.url = url

      # Diccionario de opciones para youtube_dl:
      self.ytdl_opts = ytdl_opts
      self.ytdl_opts["progress_hooks"] = [self.hook_ytdl]
      # print(self.ytdl_opts)
      
      self.daemon = True # Estableciendo thread como "daemon" para que al cerrar la GUI finalice también su ejecución
      self.start()       # Iniciando thread.


    def run(self):
      """Método que ejecuta youtube_dl en un loop, recibiendo una URL como argumento."""

      with youtube_dl.YoutubeDL(self.ytdl_opts) as ytdl:
        ytdl.download([self.url])

      return


    def hook_ytdl(self, d):
      """Método callback que recibe el estado de ejecución de youtube_dl y lo guarda como string en una Queue.
      Se recibe un diccionario como parámetro."""
      
      # Si se recibe diccionario, ponerlo tal cual en queue:
      if d:
        self.queue.put(d)
