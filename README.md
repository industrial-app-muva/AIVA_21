# Capacitor Detector

Este proyecto está dedicado al diseño, implementación y despliegue del sistema Capacitor Detector. Este proyecto tiene como objetivo implementar un sistema capaz de reconocer condensadores situados en una placa base dentro de una imagen.

## Inicio

Con el siguiente comando la aplicación web y la API REST estarán disponibles en el puerto 80 de la máquina donde se esté ejecutando:

````shell 
python app.py
````

Para acceder a la aplicación web basta con iniciar el navegador e introducir la siguiente URL:

````shell
http://<ip host>:80
````

## API REST

La URL requerida para solicitar el reconocimiento sobre una imagen comunicándose exclusivamente con la API REST es la siguiente:

````shell 
http://<ip host>:80/process_img 
````

Es necesario que la petición sea un método POST y la imagen debe ir adjuntada en la petición como un fichero.

## Docker

El sistema se puede desplegar mediante Docker y docker-compose con el siguiente comando:

`` docker-compose up ``

**Todos los comandos se deben ejecutar desde la carpeta raiz del proyecto.**