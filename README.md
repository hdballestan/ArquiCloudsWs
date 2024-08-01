# URL Status Monitor -  Avísame

Este proyecto es una aplicación basada en FastAPI que permite monitorear el estado de una URL. La aplicación permite verificar si una URL está activa (status 200) o ha dejado de estar disponible. Los usuarios pueden configurar el intervalo de tiempo para las verificaciones y recibir notificaciones por correo electrónico cuando se produzca el cambio deseado.
### Requisitos Previos
```bash
Python 3.8+
Docker (si se utiliza para monitorizar eventos de Docker)
Entorno virtual de Python (recomendado)
```

### Instalación

    Clonar el repositorio:

```bash
git clone https://github.com/tu_usuario/url-status-monitor.git
cd url-status-monitor
```

### Crear y activar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Instalar las dependencias:

```bash
pip install -r requirements.txt
```


## Configurar el entorno:

Crear un archivo environment.py que contenga las variables necesarias, como el ARN de SNS (ver el env_example.txt):

Hay que verificar las credenciales de AWS para que boto3 pueda publicar las notificaciones.

### Ejecución

#### Iniciar la aplicación:

```bash
uvicorn monitor:app --reload
```
    

Esto iniciará el servidor en `http://127.0.0.1:8000`.

#### Acceder a la aplicación:

Navegar a `http://127.0.0.1:8000` en el navegador para acceder al formulario de monitoreo de URL.

## Uso

### Formulario Web

Introducir la URL que deseas monitorear en el campo "URL".
Seleccionar el intervalo de tiempo para las verificaciones en "Check every".
Elegir si deseas monitorear cuando la URL esté "On" (activa) o "Off" (caída).
Clic en "Start Monitoring" para iniciar el monitoreo.

### API Endpoints

`POST /start-monitoring`: Inicia el monitoreo de una URL. Recibe un JSON con los campos url, time y status.

Ejemplo de cuerpo de la solicitud:

```json
{
  "url": "https://example.com",
  "time": 300,
  "status": "on"
}
```


Respuesta:


```json
{
"status": "Monitoring started",
"url": "https://example.com",
"check_interval": 300,
"desired_status": "on"
}
```

`GET /`: Devuelve el formulario HTML para iniciar el monitoreo desde el navegador.

Notificaciones

La aplicación envía notificaciones a través de AWS SNS cuando detecta que una URL ha cambiado al estado deseado. Asegúrate de que tu ARN de SNS esté correctamente configurado en el archivo environment.py.
Ejecución como servicio (opcional)


Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
