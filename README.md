# Capacitor Detector

Este proyecto está dedicado al diseño, implementación y despliegue del sistema Capacitor Detector. Este proyecto tiene como objetivo implementar un sistema capaz de reconocer condensadores situados en una placa base dentro de una imagen.

## Inicio

Con el siguiente comando la aplicación web y la API REST estarán disponibles en el puerto 80 de la máquina donde se esté ejecutando:

`` python app.py ``

Para acceder a la aplicación web basta con iniciar el navegador e introducir la siguiente URL:

`` http://localhost:80 ``

## API REST

La URL requerida para solicitar el reconocimiento sobre una imagen comunicandose exclusivamente con la API REST es la siguiente:

`` http://localhost:80/process_img ``

Es necesario que la petición sea un método POST y la imagen debe ir adjuntada en la petición como un fichero.