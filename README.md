# YoutubeToMP3 1.0b

Una simple app de escritorio, que hace de frontend del programa youtube_dl y que permite descargar música en formato mp3 desde Youtube mismo.

Hecho en *Python 3*, usando *Tkinter* para la interfaz gráfica y *Youtube_dl* para descargar y convertir los videos a mp3 (usando *FFmpeg* para este último cometido).

![Imagen](https://github.com/FedeHC/YoutubeToMP3/blob/master/images/captura.jpg)

## Aclaraciones:
- De momento no es más que un script ejecutable, solo probado en Linux Mint 18/19. Faltaría testear en otras distros ¡y en Windows y Mac! Aunque en principio debería correr sin problemas en cualquiera de estos (o con pequeñas correcciones) si se cumplen con los requisitos.

## Requisitos:
- [Python 3.5 (o superior)](https://www.python.org/downloads/).
    - **Tkinter** suele venir por defecto con Python, pero no está de más en chequear que [esté instalado](https://tkdocs.com/tutorial/install.html) en nuestro sistema.
- Tener instalado [Youtube_dl](http://ytdl-org.github.io/youtube-dl/download.html).
    - En Windows es necesario tener [Microsoft Visual C++ 2010 Redistributable Package (x86)](https://www.microsoft.com/en-US/download/details.aspx?id=5555) (más detalles en [Youtube_dl](http://ytdl-org.github.io/youtube-dl/download.html)).
- Youtube_dl a su vez necesita [FFmpeg](https://ffmpeg.org/download.html) para realizar la conversión de video a MP3.
- En Linux es recomendable usar [Virtualenv](https://virtualenv.pypa.io/en/stable/) para instalar de modo separado *Python* y *youtube_dl* del SO (y los módulos secundarios que estos 2 instalen), dado que muchas distros suelen tener instalado su propia versión de Python para su funcionamiento interno.

## Uso:
Simplemente ejecutar el script de python:
```
    python3 YouTubeToMP3.pyw
```

Para descargar música, basta con copiar y pegar la url del video y elegir una carpeta de destino.

### Más info:
- [Python Doc](https://www.python.org/doc/)
- [Youtube_dl Doc](https://github.com/ytdl-org/youtube-dl/blob/master/README.md)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html/)