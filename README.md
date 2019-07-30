# YoutubeToMP3 1.0b

Una sencilla app de escritorio para descargar música en formato mp3 desde Youtube.

Hecho en *Python 3*, usando *Tkinter* para la interfaz gráfica y *Youtube_dl* para descargar y convertir los videos a mp3.

![Imagen](https://github.com/FedeHC/YoutubeToMP3/blob/master/images/captura.jpg)

## Aclaraciones:
- De momento no es es un ejecutable y solo fue probado en Linux Mint 18. Faltaría probar en otras distros y en Windows y Mac. Estimo que en un principio debería poder correr sin problemas en cualquier S.O. si se cumplen con los requisitos.

## Requisitos:
- [Python >=3.5]((https://www.python.org/downloads/)).
- Tener instalado el módulo [Youtube_dl](http://ytdl-org.github.io/youtube-dl/download.html) (en Windows es necesario tener *Microsoft Visual C++ 2010 Redistributable Package (x86)*, ver link).


## Uso:
Simplemente ejecutar el script de python:
```
    python3 YouTubeToMP3.pyw
```

Para descargar música basta con copiar y pegar la url del video y elegir una carpeta de destino.

### Más info:
- [Youtube_dl Doc](https://github.com/ytdl-org/youtube-dl/blob/master/README.md)
