#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from extras import *


class YoutubeToMP3():
  """Clase que contiene toda la interfaz gráfica y el grueso de su funcionalidad."""

  def __init__(self, title, path, ytdl_opts, template):

    self.reset_variables()                  # Reseteando las variables principales.
    self.final_path = self.check_path(path) # Seteando el directorio de trabajo.
    self.ytdl_opts = ytdl_opts # Dicc. de config básica para youtube_dl.
    
    # Seteando path, nombre y extensión final del mp3 convertido en dicc. de youtube_dl:
    self.template = template
    self.ytdl_opts["outtmpl"] = self.final_path + self.template

    self.gui(title) # Iniciando método que inicia la GUI del programa.
    

  def gui(self, title):
    """Método que inicia la GUI del programa, con sus respectivos widgets."""
    
    # [Propiedades generales de la ventana]
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
    self.menubar = Menu(self.window)
    self.window["menu"] = self.menubar

    # [Menu Archivo]
    self.menu_file = Menu(self.menubar)
    self.menubar.add_cascade(menu=self.menu_file, label="Archivo")
    self.menu_file.add_command(label="Iniciar")
    self.menu_file.add_separator()
    self.menu_file.add_command(label="Salir")

    # [Menu Acerca]
    self.menu_help = Menu(self.menubar)
    self.menubar.add_cascade(menu=self.menu_help, label="Ayuda")
    self.menu_help.add_command(label="Acerca")

    # [VENTANA]
    # [URL / Botón INICIAR]
    self.label_url = Label(self.window, text="Youtube URL:", font=("Arial", 14))
    self.label_url.grid(column=0, row=0, padx=10, pady=10, sticky=W,)

    self.entry_url = Entry(self.window, width=41, font=("Arial", 14), bd=0)
    self.entry_url.grid(column=1, row=0, sticky=W)
    self.entry_url.focus()    # Poner en foco en este campo al arrancar el programa.

    self.btn_download = Button(self.window, text="INICIAR", font=("Arial", 10), command=self.download_and_convert)
    self.btn_download.grid(column=2, row=0, padx=10, sticky=W)

    # [Carpeta de Descarga]
    self.label_dir = Label(self.window, text="Carpeta de descarga:", font=("Arial", 10))
    self.label_dir.grid(column=0, row=1, padx=10, sticky=W)

    self.entry_dir = Entry(self.window, width=64, font=("Arial", 10), bd=0)
    self.entry_dir.insert(0, self.final_path)
    self.entry_dir.grid(column=1, row=1, sticky=W)

    self.btn_final_dir = Button(self.window, text="Seleccionar", font=("Arial", 6), command=self.select_dir)
    self.btn_final_dir.grid(column=2, row=1, padx=10, sticky=W)

    # [Mensaje de status]
    self.label_status_title = Label(self.window, text="Status:", font=("Arial", 10))
    self.label_status_title.grid(column=0, row=2, padx=10, pady=20, sticky=W)

    self.status_message = StringVar()
    self.status_message.set("Esperando una URL válida...")

    self.label_status = Label(self.window, textvariable=self.status_message, font=("Arial", 10, "italic"))
    self.label_status.grid(column=1, row=2, pady=10, sticky=W)

    # Cambiando todos los colores de ventana y widgets:
    self.change_GUI_colors()

    # Iniciando loop:
    self.window.mainloop()

    return


  def change_GUI_colors(self):
    """Metodo que simplemente cambia los colores de la GUI a los valores pasados."""

    # Determinando variables con los colores a usar:
    self.black = "#282923"
    self.white = "#F3F8F2"
    self.grey = "#51524B"
    self.red = "#EF5958"
    self.green = "#71FF4F"

    # Ajustando colores de letra y fondo a la ventana:
    self.window.configure(bg=self.black)

    # Ajustando colores de letra y fondo a menues:
    self.menubar.configure(fg=self.white, bg=self.black)
    self.menu_file.configure(fg=self.white, bg=self.black)
    self.menu_help.configure(fg=self.white, bg=self.black)

    # Ajustando colores de letra, fondo y selección al resto de los widgets:
    self.label_url.configure(fg=self.white, bg=self.black)
    self.entry_url.configure(fg=self.white, bg=self.black,
                             disabledbackground=self.grey,
                             highlightthickness=1, highlightcolor=self.red, selectbackground=self.red)
    self.btn_download.configure(fg=self.white, bg=self.black,
                                disabledforeground=self.grey)
    self.label_dir.configure(fg=self.white, bg=self.black)
    self.entry_dir.configure(fg=self.white, bg=self.black,
                             disabledbackground=self.grey, selectbackground=self.red)
    self.btn_final_dir.configure(fg=self.white, bg=self.black,
                                 disabledforeground=self.grey)
    self.label_status_title.configure(fg=self.white, bg=self.black)
    self.label_status.configure(fg=self.white, bg=self.black)

    return


  def check_path(self, temp_path):
    """Método que chequea una path recibida como argumento, remueve espacios y comprueba si es válida para el 
    S.O. actual. Según el caso se rectifica la path recibida según el caso."""
    
    try:
      from pathlib import Path
      import os

      temp_path = temp_path.strip()       # Removiendo espacios iniciales y finales (si los hay).

      # Chequeando si es una path existente y válida:
      path = Path(temp_path)
      if path.exists() and path.is_dir():
        temp_path = str(path)

      # Si no existe path se avisa por consola:
      else:
        print("# AVISO: la path pasada por constructor no es válida (fijando path actual como carpeta de destino)")
        temp_path = os.getcwd()

    except ImportError as e:
      print("\n# ERROR: Hubo problemas al cargar módulo.\n- MENSAJE: {0}".format(e))

    # En cualquier caso, se retorna la path rectificada con "/" al final:
    finally:
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
    
    status_url = {"url": None, "valid": None, "reason": None} # Dicc. de status de la URL recibida.

    # Si la URL está vacía:
    if current_url == "":
      status_url = {"url": "", "valid": False, "reason": "empty"}

    # Si la URL empieza correctamente:
    elif "www.youtube.com/watch?v=" in current_url:
      status_url = {"valid": True, "reason": "valid"}

      # Si es recibe una lista de reproducción, se quita la parte restante de la URL:
      if "&" in current_url:
        pos = current_url.find("&") 
        current_url = current_url[0:pos]

        # Si no empieza con "https", se le agrega:
        if not current_url.startswith("https://"):
          current_url = "https://" + current_url

      status_url["url"] = current_url   # Agregando URL al dicc.

    # Si no empieza la url correctamente, se devuelve el dicc. con status inválido:
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
        self.label_status.configure(textvariable=self.status_message, fg=self.red)
        self.window.update_idletasks()    # Actualizar GUI.

      elif status_url["reason"] == "invalid":
        self.status_message.set("URL no válida, ingrese una nueva.")
        self.label_status.configure(textvariable=self.status_message, fg=self.red)
        self.window.update_idletasks()    # Actualizar GUI.

      else:
        print("# ERROR: se recibió una reason nula desde función check_url dentro de check_status_url.")

      self.entry_url.select_range(0, END) # Dejar seleccionado el campo URL para borrar/corregir más rápido.
      return False

    elif status_url["valid"] == None:
      print("# ERROR: se recibió una URL nula desde función check_url dentro de check_status_url.")
      self.entry_url.select_range(0, END) # Dejar seleccionado el campo URL para borrar/corregir más rápido.
      return False

    # Si es una URL válida se continua devolviendo True:
    else:
      return True  


  def download_and_convert(self):
    """Método que procede a descargar el video, convertirlo a MP3 y moverlo a la carpeta de destino."""

    self.final_path = self.check_path(self.entry_dir.get())     # Chequear carpeta destino en el campo corresp.
    self.ytdl_opts["outtmpl"] = self.final_path + self.template # Actualizando carpeta destino (en dicc. youtube_ld).

    # URL:
    status_url = self.check_url(self.entry_url.get())
    ok_url = self.check_status_url(status_url)

    # Si la URL es correcta, se prosigue a descargar, convertir a MP3, renombrar, abrir carpeta y avisar:
    if ok_url:
      url = status_url['url'] # Se cambia por la URL ya rectificada.
      self.status_message.set("URL válida! Comenzando...")
      self.label_status.configure(textvariable=self.status_message, fg=self.white)
      self.window.update_idletasks()      # Actualizar GUI.

      self.youtube_dl_thread(url) # Youtube_dl en thread paralelo para desc. y convertir a MP3 sin congelar GUI.
      self.change_to_MP3()        # Esperando conversión para cambiar extension y arreglar guión.
      self.open_target_folder()           # Se abre la carpeta de destino.
      self.change_buttons_state("normal") # Habilitando botones y campos nuevamente.

      # Mensaje final de éxito:
      self.status_message.set("¡Conversión a MP3 finalizada con éxito! :)")
      self.label_status.configure(textvariable=self.status_message, fg=self.green)
      self.window.update_idletasks()      # Actualizar GUI.

    # En cualquier caso...
    self.reset_variables()                # Se resetea las variables principales.
    self.entry_url.select_range(0, END)   # Dejar seleccionado el campo URL para borrar/corregir más rápido.

    return


  def youtube_dl_thread(self, url):
    """Método que simplemente llama a youtube_dl a modo de proceso paralelo (para no congelar la GUI),
    recibiendo y pasando una URL como argumento."""

    try:
      import queue, time

      self.queue = queue.Queue()  # Creando objeto para comunicar mensajes entre thread paraleo y GUI.
      ytdl_hook = Hook(self.queue, self.ytdl_opts, url) # Iniciando youtube_dl en un thread paralelo.
      self.check_queue()          # Ejecutando método que busca mensajes constantemente en la queue.

    except ImportError as e:
      print("\n# ERROR: Hubo problemas al cargar módulos.\n- MENSAJE: {0}".format(e))

    return


  def check_queue(self):
    """Método que chequea en queue en búsqueda de dicc. de youtube_dl. Si no se recibe dicc., se vuelve
    a reiniciar el ciclo hasta obtener una. El ciclo finaliza al encontrar un mensaje de status determinado."""

    finish = False
    status_updated = False

    # Mientras el video no descargue o termine en error, se inicia y se mantiene un ciclo de control:
    while not finish:
      try:
        d = self.queue.get(0)           # Obteniendo dicc. desde queue.
        self.video_file = d["filename"] # Obteniendo path y filename desde dicc.
        
        # Si el status actual difiere del último, actualizar el último:
        if self.download_status != d["status"]:
          status_updated = True
          self.download_status = d["status"]

        # Si hubo un cambio de status, chequear el status de la descarga:
        if status_updated:

          # Si se está descargando:
          if self.download_status == "downloading":
            self.status_message.set("Iniciando descarga del video...")
            self.label_status.configure(textvariable=self.status_message, fg=self.white)
            self.change_buttons_state("disabled")         # Para evitar problemas durante la descarga.
            self.window.update_idletasks()                # Actualizar GUI.

          # Si se terminó de descargar:
          if self.download_status == "finished":
            self.status_message.set("Video descargado, convirtiendo ahora a MP3 (espere unos segundos...)")
            self.label_status.configure(textvariable=self.status_message, fg=self.white)
            self.window.update_idletasks()                # Actualizar GUI.
            finish = True                                 # Para terminar con el ciclo y finalizar.

          # Si hubo error al descargar:
          if self.download_status == "error":
            self.change_buttons_state("normal")           # Activando botones nuevamente.
            self.status_message.set("Error al descargar video.")
            self.label_status.configure(textvariable=self.status_message, fg=self.red)
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

    self.mp3_file = self.video_file[0:-5] + ".mp3" # Obteniendo la path del MP3 (aún en conversión).

    # Si finalizó la conversión del video a MP3, se continua:
    if self.check_if_MP3_is_converted():
      self.change_hyphen_in_MP3_filename() # Cambiando posición del guión que suele venir típicamente en los videos.

    return

 
  def check_if_MP3_is_converted(self):
    """Método que chequea si youtube_dl ha terminado de convertir el video a MP3.
    En caso de que detecte el video pero el MP3 siga aún incrementando su tamaño, se espera.
    Si deja de incrementar su tamaño, se da por finalizado y se retorna."""

    last_size = 0
    current_size = 0
    finish = False
      
    # Mientras el video no se termine de convertir a MP3, se inicia y se mantiene un ciclo de control:
    while not finish:
      try:
        import os, time

        current_size = os.path.getsize(self.mp3_file) # Obteniendo el último tamaño mientras se realiza la conversión a MP3.
        # print(current_size)

        # Si el último tamaño coincide con el de la última vez, terminar ciclo:
        if current_size == last_size:
          finish = True

        # Caso contrario, actualizar último tamaño:
        else:
          last_size = current_size

      except OSError as e:
        pass # Se pasa de largo porque suele saltar excepción solo durante la 1ra lectura.
        # print("\n# ERROR: No se pudo obtener el tamaño del archivo MP3.\n- MENSAJE: {0}".format(e))

      except ImportError as e:
        print("\n# ERROR: Hubo problemas al cargar módulo.\n- MENSAJE: {0}".format(e))

      finally:
        time.sleep(1) # Dejar pasar 1 segundo antes de reiniciar el ciclo.

    # Si se finalizó correctamente...
    return finish


  def change_hyphen_in_MP3_filename(self):
    """Método que cambia la posición del guión que suele venir típicamente de los videos de música en Youtube."""

    # Arreglando guión:
    try:
      import os

      # Corrigiendo problema del guión en título original:
      old_name = self.mp3_file
      new_name = self.mp3_file.replace(" - ", "- ")

      # print("- Viejo nombre: {0}".format(old_name)
      # print("- Nuevo nombre: {0}".format(new_name))

      os.rename(old_name, new_name)
      self.mp3_file = new_name

    # En caso de no poder arreglar el guión, se avisa del error en cuestión:
    except OSError as e:
      print("\n# ERROR al renombrar archivo en carpeta destino.\n- Detalles: {0}".format(e))
      self.status_message.set("MP3 descargado, pero no se pudo renombrar correctamente (ver consola).")
      self.label_status.configure(textvariable=self.status_message, fg=self.white)
      self.window.update_idletasks()                # Actualizar GUI.

    except ImportError as e:
      print("\n# ERROR: Hubo problemas al cargar módulo.\n- MENSAJE: {0}".format(e))

    return


  def change_buttons_state(self, action):
    """Método que cambia el estado de todos los botones del programa según un string de estado pasado como argumento."""

    # Cambiando campo y botón URL:
    self.entry_url.config(state=action)
    self.btn_download.config(state=action)

    # Cambiando campo y botón de la carpeta final:
    self.entry_dir.config(state=action)
    self.btn_final_dir.config(state=action)

    return


  def open_target_folder(self):
    """Método que abre una carpeta desde el SO (sea cual sea) a partir de la path de destino."""
    import os, platform, subprocess

    # Intentando chequear plataforma y abrir carpeta destino:
    try:
      if platform.system() == "Windows":
          os.startfile(self.final_path)
      elif platform.system() == "Darwin":
          subprocess.Popen(["open", self.final_path])
      else:
          subprocess.Popen(["xdg-open", self.final_path])

    # En caso de no lograrse, se avisa por consola:
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
