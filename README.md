# YoutubeToMP3 1.01b

Una simple app de escritorio que hace de frontend del programa *youtube_dl* y que permite descargar música en formato MP3 desde Youtube mismo.

Creado con *Python 3*, usando *Tkinter* para la interfaz gráfica y *Youtube_dl* para descargar y convertir los videos a MP3 (usando *FFmpeg* internamente para la conversión de video a audio).

![Imagen](./screenshots/captura-1.jpg)

## Instalación:

Descargar el zip según el SO usado y descomprimirlo en cualquier carpeta para ejecutar finalmente el binario que viene dentro.

- GNU/Linux <sup>1</sup>:  [Descargar](./downloads/YoutubeToMP3-1.01b-Linux.zip)
- Windows<sup>2</sup>:  Pendiente
- Mac<sup>3</sup>:  Pendiente

<sup>1: Testeado solamente en Linux Mint 18.3 y 19.2.</sup>

<sup>2: Próximamente a testear en Windows 10.</sup>

<sup>3: Sin planes de portar y testear de momento.</sup>

## Uso:

Para descargar música, basta con copiar y pegar la url del video y elegir una carpeta de destino:

![Imagen](./screenshots/captura-2.jpg)


### Más info:
- [Youtube_dl Doc](https://github.com/ytdl-org/youtube-dl/blob/master/README.md)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html/)
