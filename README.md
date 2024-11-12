Setup: 
Se tienen que configurar algunas cosas del entorno de python:

Activar el entorno virtual:
.\env\Scripts\activate

Actualizar dependencias:
pip install -r requirements.txt

Además, hay que instalar Flask, un framework desarrollado en python que permite crear aplicaciones web:
pip install flask 

Un adicional de flask es CORS, que permite que las aplicaciones web de cliente interactúen con recursos de otro dominio, lo que va a hacer que se pueda conectar el backend con el front
pip install flask-cors


Interacción:

Para interactuar con el programa, se debe acceder a la carpeta “obligatorio-back” y luego a la carpeta “controllers”.

En la carpeta controllers se van a encontrar todos los archivos importantes. Está tendrá una sección “database” donde se encuentran las conexiones hacia la base de datos, mientras que los archivos y clases del programa estarán separados. 
En “utils”, “helpers” se encontrarán información de interés y algunos comandos de ayuda.
Finalmente, en el archivo README estará la explicación de ayuda y una guía completa sobre cómo manejar el programa, básicamente la explicación que se está brindando en este documento.


Hay que familiarizarse con la forma de navegar entre carpetas.
Esto se hace utilizando el comando “cd”, seguido del nombre de la carpeta a la cual se quiere acceder.
De forma contraria, para salir de una carpeta se usa cd seguido de 2 puntos (..).


Una vez dentro de controllers, que contiene a todas las clases, se utilizará el comando “python” seguido del nombre de la clase y su extensión (py), por ejemplo, para ejecutar la clase “alumnos” sería:
“python alumnos.py”.

Cada clase tiene pruebas para cada método, es decir, que si se ejecuta una clase se podrá ver el funcionamiento de todos sus métodos localmente si así se desea. 
La funcionalidad principal de este proyecto backend va a estar contenida en el archivo “main”. Dicho archivo tiene lo que se llama “endpoints”, que se encargan de tomar los métodos de cada clase y hacerlos utilizables para aplicaciones externas. 

Una vez se ejecuta, se va a levantar una conexión en un puerto predeterminado, lo que va a permitir realizar una conexión con la parte de frontend del proyecto.
