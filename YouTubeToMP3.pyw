#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from extras import *


class YoutubeToMP3():
  """Clase que contiene toda la interfaz gráfica y toda la funcionalidad del programa principal."""
  def __init__(self, title, path, ytdl_opts, template):

    # Status, url y archivo mp3:
    self.download_status = ""
    self.url = None
    self.mp3_file = ""

    # Directorio de trabajo:
    self.final_path = self.check_path(path)

    # El nombre y la extensión final del mp3 convertido (según youtube_dl templates):
    self.template = template

    # Dicc. de config para Youtube_dl:
    self.ytdl_opts = ytdl_opts
    self.ytdl_opts["progress_hooks"] = [self.hookYoutubeDl]
    self.ytdl_opts["outtmpl"] = self.final_path + self.template

    # Iniciando interfaz gráfica:
    self.gui(title)


  def gui(self, title):
    """Método que inicia la gui del programa, con sus respectivos widgets."""
    
    # [Propiedades de la Ventana]
    self.window = Tk()
    self.window.title(title)
    self.window.geometry("700x110")
    self.window.resizable(FALSE, FALSE)
    self.window.option_add("*tearOff", FALSE)

    # [Icono del programa]
    icon_window = Image("photo", file="images/logo.png")
    self.window.tk.call("wm", "iconphoto", self.window._w, icon_window)

    # [MENU]
    # [Barra de menu]
    menubar = Menu(self.window)
    self.window["menu"] = menubar

    # [Menu Archivo]
    menu_file = Menu(menubar)
    menubar.add_cascade(menu=menu_file, label="Archivo")
    menu_file.add_command(label="Iniciar")
    menu_file.add_separator()
    menu_file.add_command(label="Salir")

    # [Menu Acerca]
    menu_help = Menu(menubar)
    menubar.add_cascade(menu=menu_help, label="Ayuda")
    menu_help.add_command(label="Acerca")

    # [VENTANA]
    # [URL / Botón INICIAR]
    label_url = Label(self.window, text="Youtube URL:", font=("Arial", 14))
    label_url.grid(column=0, row=0, padx=10, pady=10, sticky=W,)

    self.entry_url = Entry(self.window, width=41, font=("Arial", 14), fg="red", bd=0,
                       highlightcolor="#EF5958", highlightthickness=1, selectbackground="#EF5958")
    self.entry_url.grid(column=1, row=0, sticky=W)
    self.entry_url.focus()    # Poner en foco en este campo al arrancar el programa.

    self.btn_download = Button(self.window, text="INICIAR", font=("Arial", 10), command=self.download_and_convert)
    self.btn_download.grid(column=2, row=0, padx=10, sticky=W)

    # [Carpeta de Descarga]
    label_dir = Label(self.window, text="Carpeta de descarga:", font=("Arial", 10))
    label_dir.grid(column=0, row=1, padx=10, sticky=W)

    self.entry_dir = Entry(self.window, width=64, font=("Arial", 10), bd=0, selectbackground="#EF5958")
    self.entry_dir.insert(0, self.final_path)
    self.entry_dir.grid(column=1, row=1, sticky=W)

    self.btn_final_dir = Button(self.window, text="CAMBIAR", font=("Arial", 6), command=self.select_dir)
    self.btn_final_dir.grid(column=2, row=1, padx=10, sticky=W)

    # [Mensaje de status]
    label_status_title = Label(self.window, text="Status:", font=("Arial", 10))
    label_status_title.grid(column=0, row=2, padx=10, pady=20, sticky=W)

    self.label_status = Label(self.window, text="Esperando una URL válida...",
                     font=("Arial", 10, "italic"))
    self.label_status.grid(column=1, row=2, pady=10, sticky=W)

    # Iniciando loop:
    self.window.mainloop()

    return


  def check_path(self, temp_path):
    """Método que chequea una path recibida como argumento, remueve espacios y comprueba si es válida para el 
    S.O. actual. Según el caso se cambia la."""
    
    from pathlib import Path
    import os

    # Removiendo espacios iniciales y finales (si hay):
    temp_path = temp_path.strip()

    # Chequeando si es una path existente y válida:
    path = Path(temp_path)
    if path.exists() and path.is_dir():
      temp_path = str(path)

    else:
      print("# AVISO: la path pasada por constructor no es válida (fijando path actual como carpeta de destino)")
      temp_path = os.getcwd()

    # En cualquier caso se retorna siempre el path rectificado con "/" al final:
    return temp_path + "/"


  def select_dir(self):
    """Método que abre ventana de diálogo solicitando una carpeta de destino y actualiza el campo
    correspondiente en ventana."""

    selected_dir = filedialog.askdirectory(initialdir=self.final_path,
                                          title="Doble click para seleccionar la carpeta destino:")
    self.entry_dir.delete(0, "end")
    self.entry_dir.insert(0, selected_dir)

    return


  def check_url(self, current_url):
    """Método que chequea si la url de youtube pasada por argumento es válida."""
    
    status_url = {"url": None, "valid": None, "reason": None}

    # Si el url está vacío:
    if current_url == "":
      status_url = {"url": "", "valid": False, "reason": "empty"}

    # Si el url empieza correctamente:
    elif "www.youtube.com/watch?v=" in current_url:
      status_url = {"valid": True, "reason": "valid"}

      if "&" in current_url:
        # Quitando todo lo que sigue después del primer "&" en la url:
        pos = current_url.find("&")
        current_url = current_url[0:pos]

        if not current_url.startswith("https://"):
          current_url = "https://" + current_url

      # Agregando url al dicc.:
      status_url["url"] = current_url

    else:
      status_url = {"url": current_url, "valid": False, "reason": "invalid"}

    return status_url


  def check_status_url(self, status_url):
    """Método que chequea datos de un dicc. recibido como argumento, actualiza label en ventana y devuelve
    True o False según el caso."""

    # Si no es una url válida se aborta y se muestra mensaje:
    if status_url["valid"] == False:
      if status_url["reason"] == "empty":
        self.label_status.configure(text="URL vacia, ingrese una.", fg="red")

      elif status_url["reason"] == "invalid":
        self.label_status.configure(text="URL no válida, ingrese una nueva.", fg="red")

      else:
        print("# ERROR: se recibió una reason nula desde función check_url dentro de check_status_url.")

      self.entry_url.select_range(0, END) # Dejar seleccionado el campo URL para borrar/corregir más rápido.
      return False

    elif status_url["valid"] == None:
      print("# ERROR: se recibió una URL nula desde función check_url dentro de check_status_url.")
      self.entry_url.select_range(0, END) # Dejar seleccionado el campo URL para borrar/corregir más rápido.
      return False

    else:
      return True  


  def download_and_convert(self):
    """Método que procede a descargar el video, convertirlo a MP3 y moverlo a la carpeta de destino."""

    # Obteniendo y chequeando la carpeta de destino en el campo corresp.:
    self.final_path = self.check_path(self.entry_dir.get())

    # Actualizando directorio final de descarga en dicc. de youtube_ld:
    self.ytdl_opts["outtmpl"] = self.final_path + self.template

    # URL:
    status_url = self.check_url(self.entry_url.get())
    ok_url = self.check_status_url(status_url)

    # Solo si está bien la URL se continua con la descarga y conversión:
    if ok_url:

      # Se cambia por la URL ya rectificada:
      url = status_url['url']

      # Llamando a youtube_dl para descargar video y convertirlo a mp3 en paralelo (para no congelar gui):
      self.execute_youtube_dl(url)

      if self.download_status == "finished":
        try:
          # Corrigiendo problema del guión en título original:
          import os
          old_name = self.mp3_file
          new_name = self.mp3_file.replace(" - ", "- ")
          os.rename(old_name, new_name)
          self.mp3_file = new_name

          # Abriendo carpeta de destino:
          self.open_folder_from_os()

        except OSError as e:
          print("\n# ERROR al renombrar archivo en carpeta destino.\n- Detalles:")
          print(e)
          self.label_status.configure(text="MP3 descargado, pero no se pudo renombrar correctamente (chequear permisos en carpeta destino).", fg="black")

    # Reseteando flags y variables de la clase, al margen del resultado:
    self.reset_flags_and_variables()

    return


  def execute_youtube_dl(self, url):
    """Método que simplemente llama a youtube_dl en paralelo, recibiendo una URL como argumento."""

    with youtube_dl.YoutubeDL(self.ytdl_opts) as ytdl:
        ytdl.download([url])

    return 


  def check_and_change_to_mp3(self, d):
    """Método que chequea la extensión del video previamente bajado (recibido como string en diccionario) y
    lo renombra a MP3."""
    
    # Chequeando desde diccionario generado por Youtube_dl:
    self.mp3_file = d["filename"]
    
    # Si es un formato de video típico, quitarlo y renombrarlo a MP3:
    if self.mp3_file.endswith(".webm") or self.mp3_file.endswith(".mpeg") \
    or self.mp3_file.endswith(".mpg") or self.mp3_file.endswith(".avi"):
      self.mp3_file = self.mp3_file[0:-5] + ".mp3"
    
    # Si no es un formato conocido, buscar a partir de donde inicia la extensión y renombrarlo a MP3.
    # (Este método puede generar problemas si el título termina de casualidad con algún punto):
    else:
      pos = self.mp3_file.find(".", -5)
      self.mp3_file = self.mp3_file[0:pos]

    return


  def change_buttons_state(self, action):
    """Método que cambia el estado de todos los botones del programa según string pasado."""

    self.btn_download.config(state=action)
    self.btn_final_dir.config(state=action)

    return


  def reset_flags_and_variables(self):
    """Método que resetea flags y demás variables de la clase luego de finalizar una descarga/conversión."""

    self.mp3_file = ""
    self.download_status = ""
    self.url = None
    self.entry_url.select_range(0, END) # Dejar seleccionado el campo URL para borrar/corregir más rápido.

    return


  def open_folder_from_os(self):
    """Método que abre una carpeta desde el SO a partir de una path."""
    import os, platform, subprocess

    if platform.system() == "Windows":
        os.startfile(self.final_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", self.final_path])
    else:
        subprocess.Popen(["xdg-open", self.final_path])

    return


  def hookYoutubeDl(self, d):
    """Método callback para recibir mensaje de status desde youtube_dl."""

    if d["status"] == "error":
      self.download_status = d["status"]
      self.change_buttons_state("normal")
      self.label_status.configure(text="Error al intentar descargar video desde Youtube.", fg="red")

    if d["status"] == "downloading":
      self.download_status = d["status"]
      self.change_buttons_state("disabled")       # Para evitar problemas durante la descarga.
      self.label_status.configure(text="Iniciando descarga, por favor espere...", fg="green")

    if d["status"] == "finished":
      self.download_status = d["status"]         # Cambiando status.
      self.check_and_change_to_mp3(d)               # Renombrando a MP3.
      self.change_buttons_state("normal")
      self.label_status.configure(text="Descarga y conversión completa!", fg="green")

    return


# Iniciando:
if __name__ == "__main__":
  youtubeToMp3 = YoutubeToMP3(title="YouTubeToMP3 v1.0b",
                              path="/media/Archivos/",
                              ytdl_opts=ytdl_opts,
                              template="%(title)s.%(ext)s")

