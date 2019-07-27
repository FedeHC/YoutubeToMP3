#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

if __name__ != "__main__":
  try:
    # Youtube_dl:
    import youtube_dl

    # Tkinter:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog

  except ImportError as e:
    print("\n# # ERROR: Hubo problemas al cargar los módúlos necesarios.\n- Detalles:")
    print(e)


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


  # Diccionario con la configuración para la conversión del video a mp3 con youtube_dl.
  # (https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl)
  ytdl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
      "key": "FFmpegExtractAudio",
      "preferredcodec": "mp3",
      "preferredquality": "320",
    }],
    "logger": MyLogger(),
  }
