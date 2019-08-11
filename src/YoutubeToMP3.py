#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from extras import *


class YoutubeToMP3():
  """Clase que contiene toda la interfaz gráfica y el grueso de su funcionalidad."""

  def __init__(self, title, path, ytdl_opts, template):

    self.reset_variables()                  # Reseteando las variables principales.
    self.final_path = self.check_path(path) # Seteando el directorio de trabajo.
    self.ytdl_opts = ytdl_opts              # Dicc. de config básica para youtube_dl.
    
    # Seteando path, nombre y extensión final del mp3 convertido en dicc. de youtube_dl:
    self.template = template
    self.ytdl_opts["outtmpl"] = self.final_path + self.template

    self.gui(title)                         # Iniciando la GUI del programa.
    

  def gui(self, title):
    """Método que inicia la GUI del programa, con sus respectivos widgets."""
    
    # [Propiedades generales de la ventana]
    self.window = Tk()
    self.window.title(title)
    self.window.geometry("700x110")
    self.window.resizable(FALSE, FALSE)
    self.window.option_add("*tearOff", FALSE)

    # [Icono del programa]
    logo_file = "logo.png"
    if os.path.exists(logo_file):
      icon_window = Image("photo", file=logo_file)
      self.window.tk.call("wm", "iconphoto", self.window._w, icon_window)

    # [MENU]
    # [Barra de menu]
    self.menubar = Menu(self.window)
    self.window["menu"] = self.menubar

    # [Menu Opciones]
    self.menu_options = Menu(self.menubar)
    self.menubar.add_cascade(menu=self.menu_options, label="Opciones")
    self.menu_options.add_command(label="Preferencias")
    self.menu_options.add_separator()
    self.menu_options.add_command(label="Salir", command=self.window.destroy)

    # [Menu Acerca]
    self.menu_help = Menu(self.menubar)
    self.menubar.add_cascade(menu=self.menu_help, label="Ayuda")
    message_body = title + "\nPor FedeHC"
    self.menu_help.add_command(label="Acerca", command=lambda:
                                               messagebox.showinfo(title="Acerca", message=message_body))

    # [VENTANA]
    # [URL / Botón INICIAR]
    self.label_url = Label(self.window, text="Youtube URL:", font=("Arial", 14))
    self.label_url.grid(column=0, row=0, padx=10, pady=10, sticky=E)

    self.entry_url = Entry(self.window, width=45, font=("Arial", 14), bd=0)
    self.entry_url.grid(column=1, row=0, sticky=W)
    self.entry_url.focus()    # Poner en foco en este campo al arrancar el programa.

    self.btn_download = Button(self.window, text="INICIAR", font=("Arial", 10),
                               command=self.download_and_convert)
    self.btn_download.grid(column=2, row=0, padx=10, sticky=W)

    # [Carpeta de Descarga]
    self.label_dir = Label(self.window, text="Carpeta de descarga:", font=("Arial", 10))
    self.label_dir.grid(column=0, row=1, padx=10, sticky=E)

    self.entry_dir = Entry(self.window, width=64, font=("Arial", 10), bd=0)
    self.entry_dir.insert(0, self.final_path)
    self.entry_dir.grid(column=1, row=1, sticky=W)

    self.btn_final_dir = Button(self.window, text="Seleccionar", font=("Arial", 6),
                                command=self.select_dir)
    self.btn_final_dir.grid(column=2, row=1, padx=10, sticky=W)

    # [Mensaje de status]
    self.label_status_title = Label(self.window, text="Status:", font=("Arial", 10))
    self.label_status_title.grid(column=0, row=2, padx=10, pady=20, sticky=E)

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
    self.red = "#CE201F"
    self.green = "#71FF4F"

    # Ajustando colores de letra y fondo a la ventana:
    self.window.configure(bg=self.black)

    # Ajustando colores de letra y fondo a menues:
    self.menubar.configure(fg=self.white, bg=self.black)
    self.menu_options.configure(fg=self.white, bg=self.black)
    self.menu_help.configure(fg=self.white, bg=self.black)

    # Ajustando colores de letra, fondo y selección al resto de los widgets:
    self.label_url.configure(fg=self.white, bg=self.black)
    self.entry_url.configure(fg=self.white, bg=self.black,
                             disabledbackground=self.grey,
                             highlightthickness=1, highlightcolor=self.red,
                             selectbackground=self.red, selectforeground=self.white)
    self.btn_download.configure(fg=self.white, bg=self.black,
                                disabledforeground=self.grey)
    self.label_dir.configure(fg=self.white, bg=self.black)
    self.entry_dir.configure(fg=self.white, bg=self.black,
                             highlightthickness=1, highlightcolor=self.red,
                             disabledbackground=self.grey,
                             selectbackground=self.red, selectforeground=self.white)
    self.btn_final_dir.configure(fg=self.white, bg=self.black,
                                 disabledforeground=self.grey)
    self.label_status_title.configure(fg=self.white, bg=self.black)
    self.label_status.configure(fg=self.white, bg=self.black)

    return


  def check_path(self, temp_path):
    """Método que chequea una path recibida como argumento, remueve espacios y comprueba si es válida para el 
    S.O. actual. Según el caso se rectifica la path recibida según el caso."""
    
    temp_path = temp_path.strip()       # Removiendo espacios iniciales y finales (si los hay).

    # Chequeando si es una path existente y válida:
    path = Path(temp_path)
    if path.exists() and path.is_dir():
      temp_path = str(path)

    # Si no existe path se avisa por consola:
    else:
      print("# AVISO: la path pasada por constructor no es válida (fijando path actual como carpeta de destino)")
      temp_path = os.getcwd()

    # En cualquier caso, se retorna la path rectificada con "/" al final:
    return temp_path + os.path.sep


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
        self.change_status_message(message="URL vacia, ingrese una.", color=self.red)

      elif status_url["reason"] == "invalid":
        self.change_status_message(message="URL no válida, ingrese una nueva.", color=self.red)
      
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

    # Si la URL es correcta:
    if ok_url:
      url = status_url['url']                         #  Se actualiza a la URL ya rectificada.
      self.change_buttons_state("disabled")           # Habilitando botones y campos nuevamente.
      self.change_status_message(message="URL válida! Iniciando...", color=self.white)
      
      self.youtube_dl_thread(url)                     # Iniciando Youtube_dl en un thread paralelo.
      
      self.mp3_file = self.video_file[0:-5] + ".mp3"  # Actualizando extensión a MP3 (aún en conversión).

      # Si finaliza correctamente la conversión, se continua:
      if self.check_if_MP3_is_converted():
        self.change_hyphen_and_set_uppercase()
        self.open_target_folder()
        self.change_buttons_state("normal")
        self.change_status_message(message="¡Conversión a MP3 finalizada con éxito! :)",
                                   color=self.green)
        
    # En cualquier caso...
    self.reset_variables()
    self.entry_url.select_range(0, END)           # Dejar seleccionado el campo URL.

    return


  def change_status_message(self, message, color):
    """Método que cambia el mensaje de status en el programa, según mensaje y color pasados como argumentos."""

    self.status_message.set(message)                                        # Recibiendo mensaje.
    self.label_status.configure(textvariable=self.status_message, fg=color) # Fijando mensaje.
    self.window.update_idletasks()                                          # Actualizando GUI.

    return


  def youtube_dl_thread(self, url):
    """Método que simplemente llama a youtube_dl a modo de proceso paralelo (para no congelar la GUI),
    recibiendo y pasando una URL como argumento."""

    self.queue = queue.Queue()  # Creando objeto para comunicar mensajes entre thread paraleo y GUI.
    ytdl_hook = Hook(self.queue, self.ytdl_opts, url) # Iniciando youtube_dl en un thread paralelo.
    self.check_queue()          # Ejecutando método que busca mensajes constantemente en la queue.

    return


  def check_queue(self):
    """Método que chequea en queue en búsqueda de dicc. de youtube_dl. Si no se recibe dicc., se vuelve
    a reiniciar el ciclo hasta obtener una. El ciclo finaliza al encontrar un mensaje de status determinado."""

    finish = False                          # Flag de control.
    dicc_ok = False                         # Flag para prueba interna (poner en True para probar).

    # Mientras el video no descargue o termine en error, se inicia y se mantiene un ciclo de control:
    while not finish:
      try:
        # assert self.queue.get(0), "ERROR: No se obtuvo diccionario desde queue."
        d = self.queue.get(0)
        self.download_status = d["status"]  # Actualizando status.
        self.video_file = d["filename"]     # Obteniendo path y filename desde dicc.
        
        # Ver contenido del diccionario por consola (¡solo usar durante pruebas!)
        if dicc_ok:
          print(d)
          dicc_ok = False

        # Si se está descargando:
        if self.download_status == "downloading":
          # print("[Descargando]", end=" ")

          # Obteniendo info necesaria del diccionario: 
          current_size = str(round(d["downloaded_bytes"] / (1024 * 1024), 2)) + " MB"
          total_size = str(round(d["total_bytes"] / (1024 * 1024), 2)) + " MB"
          size = current_size + " / " + total_size
          
          percent = d["_percent_str"].strip()
          speed = d["_speed_str"]

          current_time = str(round(d["elapsed"], 2)) + " seg."
          eta_time = str(d["eta"]) + " seg."
          the_time = current_time + " (est.: " + eta_time + ")."

          # Mostrar info durante descarga en status:
          # print(f"Descargando: {size} ({percent}) | {speed} | {the_time}")
          self.change_status_message(message=f"Descargando: {size} ({percent}) | {speed} | {the_time}",
                                     color=self.white)

          # time.sleep(0.1)     # Dejar un mínimo intervalo para que se vea el mensaje.

        # Si se terminó de descargar:
        elif self.download_status == "finished":
          # self.change_status_message(message="Video descargado.", color=self.white)
          time.sleep(1)         # Dejar un mínimo intervalo para que se vea el nuevo mensaje.
          finish = True         # Para terminar con el ciclo y finalizar.

        # Si hubo error al descargar:
        elif self.download_status == "error":
          self.change_buttons_state("normal") # Activando botones nuevamente.
          self.change_status_message(message="Error durante descarga del video (compruebe conexión a internet y intente nuevamente).",
                                      color=self.red)
          finish = True         # Para terminar con el ciclo y finalizar.

      except queue.Empty:       # En caso de recibir una queue vacía.
          pass                  # No hacer nada, seguir de largo.
  
      """
      except AssertionError as e:
        print("\n{0}\n".format(e))
        sys.exit()              # Forzando finalización del programa.
      """
      
    return

 
  def check_if_MP3_is_converted(self):
    """Método que chequea si youtube_dl ha terminado de convertir el video a MP3.
    En caso de que detecte el video pero el MP3 siga aún incrementando su tamaño, se espera.
    Si deja de incrementar su tamaño, se da por finalizado y se retorna."""

    # Variables necesarias:
    last_size = -1            # No se deja en 0 porque el ciclo terminaría solo al empezar.
    current_size = 0
    attempts = 0 
    finish = False
      
    start_time = time.time()        # Tomando el tiempo inicial.
    current_time = None
    
    # Mientras el video no se termine de convertir a MP3, se inicia y se mantiene un ciclo de control:
    while not finish:
      try:
        current_size = os.path.getsize(self.mp3_file) # Obteniendo el último tamaño (mientras se convierte).
        the_size = str(round(current_size / (1024 * 1024), 2)) + " MB"
        
        current_time = time.time()
        the_time = str(round(current_time - start_time, 2)) + " seg."

        # print(f"Convirtiendo a MP3: {the_size} ({the_time}) | Intentos: {attempts}")
        self.change_status_message(message=f"Convirtiendo a MP3: {the_size} ({the_time})",
                                   color=self.white)

        # Si el último tamaño coincide con el de la última vez:
        if current_size == last_size:
          attempts += 1             # Sumar 1 al contador de intentos.
          if attempts >= 10:        # Si los intentos fueron más de 10 (10 intentos = 1 segundo)
            finish = True           # Terminar entonces el ciclo.
        
        # En caso contrario:
        else:
          attempts = 0              # Se resetea el contador de intentos para evitar problemas.
          last_size = current_size  # ctualizar último tamaño obtenido.
      
        time.sleep(0.1)             # Dejar 1/10 seg. hasta empezar de nuevo el ciclo.

      except (FileNotFoundError, OSError) as e:
        pass                        # Suele surgir mientras no exista/no encuentre archivo en 1° intento.

    return finish


  def change_hyphen_and_set_uppercase(self):
    """Método que arregla ligeramente de posición al guión que separa autor del título en nombre de archivo.
    También pone en máyusculas cada palabra en el nombre del archivo (tanto autor como título)."""

    # Arreglando guión:
    try:

      old_name = self.mp3_file
      
      # Obtener por separado el path y el nombre del MP3 convertido:
      path = self.final_path
      mp3 = old_name.split(os.path.sep)[-1]

      # Corrigiendo el problema del guión en nombre del MP3:
      mp3 = mp3.replace(" - ", "- ")
      
      # Poniendo en mayúsculas al comienzo de cada palabra:
      mp3 = " ".join(word.capitalize() for word in mp3.split())

      # Uniendo nuevamente path con el nuevo nombre corregido:
      new_name = path + mp3

      # print(f"- Viejo nombre: {old_name}")
      # print(f"- Nuevo nombre: {new_name}")

      os.rename(old_name, new_name)
      self.mp3_file = new_name


    # En caso de no poder arreglar el guión, se avisa del error en cuestión:
    except OSError as e:
      print("\n# ERROR al renombrar archivo en carpeta destino.\n- Detalles: {0}".format(e))
      self.change_status_message(message="MP3 convertido, pero no se pudo renombrar correctamente.",
                                 color=self.white)

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

    # Intentando chequear plataforma y abrir carpeta destino:
    if platform.system() == "Windows":
        os.startfile(self.final_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", self.final_path])
    else:
        subprocess.Popen(["xdg-open", self.final_path])

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
  youtubeToMp3 = YoutubeToMP3(title="YoutubeToMP3 v1.01b",
                              path="",
                              ytdl_opts=ytdl_opts,
                              template="%(title)s.%(ext)s")
