#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from extras import *


class YoutubeToMP3():
  """Clase que contiene toda la interfaz gráfica y el grueso de la funcionalidad del programa principal."""

  def __init__(self, title, path, ytdl_opts, template):

    # Variables principales:
    self.reset_variables()

    # Directorio de trabajo:
    self.final_path = self.check_path(path)

    # El nombre y la extensión final del mp3 convertido (según youtube_dl templates):
    self.template = template

    # Dicc. de config para Youtube_dl:
    self.ytdl_opts = ytdl_opts
    self.ytdl_opts["outtmpl"] = self.final_path + self.template

    # Iniciando interfaz gráfica:
    self.gui(title)


  def gui(self, title):
    """Método que inicia la GUI del programa, con sus respectivos widgets."""
    
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

    self.status_message = StringVar()
    self.status_message.set("Esperando una URL válida...")

    self.label_status = Label(self.window, textvariable=self.status_message, font=("Arial", 10, "italic"))
    self.label_status.grid(column=1, row=2, pady=10, sticky=W)

    # Iniciando loop:
    self.window.mainloop()

    return


  def check_path(self, temp_path):
    """Método que chequea una path recibida como argumento, remueve espacios y comprueba si es válida para el 
    S.O. actual. Según el caso se cambia la."""
    
    try:
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


    except ImportError as e:
      print("\n# ERROR: Hubo problemas al cargar módulo.\n- MENSAJE: {0}".format(e))


    finally:
      # Se retorna siempre el path rectificado con "/" al final:
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
        self.status_message.set("URL vacia, ingrese una.")
        self.label_status.configure(textvariable=self.status_message, fg="red")
        self.window.update_idletasks()                # Actualizar GUI.

      elif status_url["reason"] == "invalid":
        self.status_message.set("URL no válida, ingrese una nueva.")
        self.label_status.configure(textvariable=self.status_message, fg="red")
        self.window.update_idletasks()                # Actualizar GUI.

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

    if ok_url:
      # Se cambia por la URL ya rectificada y se avisa por mensaje de status:
      url = status_url['url']
      self.status_message.set("URL válida!")
      self.label_status.configure(textvariable=self.status_message, fg="black")
      self.window.update_idletasks()                # Actualizar GUI.

      # Llamando a youtube_dl para descargar video y convertirlo a mp3 en thread paralelo
      # (para no congelar GUI):
      self.youtube_dl_thread(url)

      # Esperando conversión para cambiar extension y el nombre al MP3:
      self.change_to_MP3()

      # Se abre la carpeta de destino:
      self.open_target_folder()

      # Habilitando botones y campos nuevamente:
      self.change_buttons_state("normal")

      # Mensaje final de éxito:
      self.status_message.set("¡Conversión a MP3 finalizada con éxito! :)")
      self.label_status.configure(textvariable=self.status_message, fg="green")
      self.window.update_idletasks()                # Actualizar GUI.

    # En cualquier caso...
    # Se resetea las variables principales:
    self.reset_variables()

    # Dejar seleccionado el campo URL para borrar/corregir más rápido:
    self.entry_url.select_range(0, END)

    return


  def youtube_dl_thread(self, url):
    """Método que simplemente llama a youtube_dl a modo de proceso paralelo (para no congelar la GUI),
    recibiendo y pasando una URL como argumento."""

    try:
      import queue, time

      # Creando objeto cola, para comunicar mensajes desde ese thread:
      self.queue = queue.Queue()

      # Iniciando youtube_dl desde la clase (que se ejecuta desde un thread aparte):
      ytdl_hook = Hook(self.queue, self.ytdl_opts, url)

      # Ejecutando finalmente el método que busca mensajes constantemente desde la queue:
      self.check_queue()

    except ImportError as e:
      print("\n# ERROR: Hubo problemas al cargar módulos.\n- MENSAJE: {0}".format(e))

    return


  def check_queue(self):
    """Método que chequea en queue en búsqueda de dicc. de youtube_dl. Si no se recibe dicc., se vuelve
    a reiniciar el ciclo hasta obtener una. El ciclo finaliza al encontrar un mensaje de status determinado."""

    finish = False
    status_updated = False

    while not finish:
      try:
        # Obteniendo dicc. desde queue:
        d = self.queue.get(0)

        # Obteniendo path y filename:
        self.video_file = d["filename"]

        # Si el último status es diferente de la última vez, actualizar:
        if self.download_status != d["status"]:
          status_updated = True
          self.download_status = d["status"]

        # Si hubo un cambio de status, chequear el status de la descarga:
        if status_updated:

          if self.download_status == "downloading":
            self.status_message.set("Iniciando descarga del video...")
            self.label_status.configure(textvariable=self.status_message, fg="black")
            self.change_buttons_state("disabled")         # Para evitar problemas durante la descarga.
            self.window.update_idletasks()                # Actualizar GUI.

          if self.download_status == "finished":
            self.status_message.set("Video descargado, convirtiendo ahora a MP3 (espere unos segundos...)")
            self.label_status.configure(textvariable=self.status_message, fg="black")
            self.window.update_idletasks()                # Actualizar GUI.
            finish = True                                 # Para terminar con el ciclo y finalizar.

          if self.download_status == "error":
            self.change_buttons_state("normal")           # Activando botones nuevamente.
            self.status_message.set("Error al descargar video.")
            self.label_status.configure(textvariable=self.status_message, fg="red")
            self.window.update_idletasks()                # Actualizar GUI.
            finish = True                                 # Para terminar con el ciclo y finalizar.

          status_updated = False

      # Si la cola de mensajes está vacía, seguir de largo sin elevar una excepción:
      except Exception:
        pass

    return


  def change_to_MP3(self):
    """Método que espera a que termine la conversión en curso, detecta la finalización y renombra finalmente
    un archivo MP3 previamente descargado."""

    # Desde path del archivo de video se obtiene la path del MP3 (aún en conversión):
    self.mp3_file = self.video_file[0:-5] + ".mp3"

    # Si finalizó la conversión del video a MP3, se continua:
    if self.check_if_MP3_is_converted():

      # Cambiando la posición del guión que suele venir típicamente en los videos de música:
      self.change_hyphen_in_MP3_filename()

    return

 
  def check_if_MP3_is_converted(self):
    """Método que chequea si youtube_dl ha terminado de convertir el video a MP3.
    En caso de que detecte el video pero el MP3 siga aún incrementando su tamaño, se espera.
    Si deja de incrementar su tamaño, se da por finalizado y se retorna."""

    last_size = 0
    current_size = 0
    finish = False
      
    while not finish:
      try:
        import os, time

        current_size = os.path.getsize(self.mp3_file)
        # print(current_size)

        if current_size == last_size:
          finish = True

        else:
          last_size = current_size

      except OSError as e:
        # print("\n# ERROR: No se pudo obtener el tamaño del archivo MP3.\n- MENSAJE: {0}".format(e))
        pass # Se pasa de largo (suele saltar excepción solo en la 1ra lectura)...

      except ImportError as e:
        print("\n# ERROR: Hubo problemas al cargar módulo.\n- MENSAJE: {0}".format(e))

      finally:
        time.sleep(1)   # Dejar pasar 1 segundo antes de reiniciar el ciclo.

    # Si se finalizó correctamente...
    return finish


  def change_hyphen_in_MP3_filename(self):
    """Método que cambia la posición del guión que suele venir típicamente de los videos de música en Youtube."""

    try:
      import os

      # Corrigiendo problema del guión en título original:
      old_name = self.mp3_file
      new_name = self.mp3_file.replace(" - ", "- ")

      # print("- Viejo nombre: {0}".format(old_name)
      # print("- Nuevo nombre: {0}".format(new_name))

      os.rename(old_name, new_name)
      self.mp3_file = new_name

    except OSError as e:
      print("\n# ERROR al renombrar archivo en carpeta destino.\n- Detalles: {0}".format(e))
      self.status_message.set("MP3 descargado, pero no se pudo renombrar correctamente (ver consola).")
      self.label_status.configure(textvariable=self.status_message, fg="black")
      self.window.update_idletasks()                # Actualizar GUI.

    except ImportError as e:
      print("\n# ERROR: Hubo problemas al cargar módulo.\n- MENSAJE: {0}".format(e))

    return


  def change_buttons_state(self, action):
    """Método que cambia el estado de todos los botones del programa según un string de estado pasado como argumento."""

    # URL:
    self.entry_url.config(state=action)
    self.btn_download.config(state=action)

    # Carpeta destino:
    self.entry_dir.config(state=action)
    self.btn_final_dir.config(state=action)

    return


  def open_target_folder(self):
    """Método que abre una carpeta desde el SO (sea cual sea) a partir de la path de destino."""
    import os, platform, subprocess

    try:
      if platform.system() == "Windows":
          os.startfile(self.final_path)
      elif platform.system() == "Darwin":
          subprocess.Popen(["open", self.final_path])
      else:
          subprocess.Popen(["xdg-open", self.final_path])

    except ImportError as e:
      print("\n# ERROR: Hubo problemas al cargar módulos.\n- MENSAJE: {0}".format(e))

    return


  def reset_variables(self):
    """Método que simplemente resetea las variables principales de la clase."""

    # Reseteando variables principales:
    self.download_status = None
    self.convertion_status = None
    self.url = None
    self.video_file = None
    self.mp3_file = None
    self.queue = None
    
    return


# Iniciando:
if __name__ == "__main__":
  youtubeToMp3 = YoutubeToMP3(title="YouTubeToMP3 v1.0b",
                              path="/media/Archivos/",
                              ytdl_opts=ytdl_opts,
                              template="%(title)s.%(ext)s")
