# Configuración de Nginx


Servir tu aplicación [[FastAPI]] con **Nginx** como proxy inverso es una configuración común y efectiva para aplicaciones en producción.

### Teoría: ¿Qué es Nginx y por qué usarlo?

**Nginx** es un servidor web que también puede actuar como proxy inverso, balanceador de carga, y caché HTTP. Como proxy inverso, Nginx recibe las solicitudes HTTP del cliente y las reenvía a un servidor de aplicaciones como Uvicorn, que maneja la lógica de la aplicación. Luego, Nginx devuelve la respuesta al cliente.

**Ventajas de usar Nginx:**

1. **Manejo de Carga**: Nginx puede manejar decenas de miles de conexiones simultáneas, mejorando la capacidad de manejo de tu aplicación.
2. **Seguridad**: Puede actuar como una capa de seguridad adicional, filtrando tráfico malicioso antes de que llegue a tu aplicación.
3. **SSL/TLS**: Nginx puede gestionar certificados SSL/TLS, ofreciendo conexiones seguras (HTTPS).
4. **Balanceo de Carga**: Puede distribuir el tráfico entre varios servidores de aplicaciones.

### Pasos para Configurar Nginx con Uvicorn

1. **Instala Nginx**: En Ubuntu, puedes instalar Nginx usando:

	```bash
	sudo apt update
	sudo apt install nginx
	```

2. **Configura Uvicorn para Despliegue**: Para producción, hay que ejecutar Uvicorn sin la opción `--reload` (que es para desarrollo). Puede hacerse como un servicio o con un administrador de procesos como **supervisord** o **systemd**.

   Un ejemplo básico para lanzar Uvicorn como servicio:

	```bash
	uvicorn monitor:app --host 0.0.0.0 --port 8002
	```

3. **Configura Nginx**: Abrir el archivo de configuración de Nginx (por ejemplo, `/etc/nginx/sites-available/tu-sitio`), o crear uno nuevo si no existe, y editar el bloque del servidor:

	```nginx
		server {
		listen 80;
		server_name avisame.com;
		
		location / {
			proxy_pass http://127.0.0.1:8002;
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
		}
		}
	```

   - **Explicación de los parámetros:**
    
    - `proxy_pass`: Especifica el backend (Uvicorn) al que Nginx enviará las solicitudes.
    - `proxy_set_header`: Estos headers aseguran que la solicitud original mantenga su integridad cuando pase por Nginx.
    
4. **Habilitar la Configuración y Reiniciar Nginx**: Si se crea un nuevo archivo de configuración en `sites-available`, crear un enlace simbólico en `sites-enabled`:

	```bash
	sudo ln -s /etc/nginx/sites-available/sitio /etc/nginx/sites-enabled/
	```

   Luego, probar la configuración de Nginx para asegurarse de que no hay errores:

	```bash
	sudo nginx -t
	```

   Si todo está bien, reiniciar Nginx:

	```bash
	sudo systemctl restart nginx
	```

5. **Configura un Firewall**: Si se está usando `ufw`, permite el tráfico en el puerto 80 (HTTP) y 443 (HTTPS si se planea usar SSL):

	```bash
	sudo ufw allow 'Nginx Full'
	```


### Extras:

- **SSL/TLS**: Para agregar soporte HTTPS, puedes obtener un certificado gratuito usando Let's Encrypt:

	```bash
	sudo apt install certbot python3-certbot-nginx
	sudo certbot --nginx -d tu-dominio.com
	```

- **Supervisar y Reiniciar Automáticamente Uvicorn**: Puedes usar `systemd` para que Uvicorn se ejecute como un servicio de sistema:

  Crea un archivo de servicio en `/etc/systemd/system/uvicorn.service`:

	```json
	[Unit]
	Description=Uvicorn FastAPI server
	After=network.target
	
	[Service]
	User=tu_usuario
	WorkingDirectory=/ruta/a/tu/proyecto
	ExecStart=/usr/bin/env uvicorn monitor:app --host 127.0.0.1 --port 8002
	Restart=always
	
	[Install]
	WantedBy=multi-user.target
	```

Luego, habilita y arranca el servicio:

```bash
sudo systemctl enable uvicorn
sudo systemctl start uvicorn
```

Con esto, la aplicación FastAPI estará servida en producción con Nginx y Uvicorn.

### Pasos para configurar Nginx con una dirección personalizada (`127.0.0.2`)

1. **Modificar el archivo `hosts`:** Primero,  se necesita editar el archivo `hosts` para asociar `127.0.0.2` con un nombre de dominio personalizado (por ejemplo, `avisame.com`).
    
    - Abrir el archivo `hosts`:

	```bash
	sudo nano /etc/hosts
	# Dentro del achivo
	127.0.0.2 avisame.com
	```

2. **Configura Nginx:** Luego, se debe ajustar la configuración de Nginx para que escuche en `127.0.0.2`.

- Configura el bloque `server` en Nginx para usar `127.0.0.2`:

```nginx
	server {
    listen 80;
    server_name avisame.com;

    location / {
        proxy_pass http://127.0.0.2:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Inicia Uvicorn en `127.0.0.2`:** Cuando se hacen este tipo de cambios hay que asegurarse que Uvicorn esté configurado para escuchar en `127.0.0.2` en lugar de `0.0.0.0` o `127.0.0.1`.

	```bash
	uvicorn monitor:app --host 127.0.0.2 --port 8002
	```

4. **Reinicia Nginx:** Después de realizar los cambios, reiniciar Nginx para que los aplique:

	```bash
	sudo systemctl restart nginx
	```

### Accediendo a la Aplicación

Una vez configurado todo:

- **Acceso desde el navegador:** Acceder a la aplicación en el navegador utilizando `http://avisame.com`.
- **Puerto:** No necesita especificarse el puerto 80, ya que es el puerto predeterminado para HTTP.


Una vez configurado todo:

- **Acceso desde el navegador:** Acceder a la aplicación en el navegador utilizando `http://avisame.com`.
- **Puerto:** No necesita especificarse el puerto 80, ya que es el puerto predeterminado para HTTP.

### Usando varios nombres de "dominio"

Sí, se definen varios nombres de servidor en la directiva `server_name` dentro de un bloque `server` de Nginx, se podrá acceder a la aplicación utilizando cualquiera de esos nombres o direcciones IP. Nginx responderá a las solicitudes que coincidan con cualquiera de esos valores.

Por ejemplo, con esta configuración:

```nginx
server {
    listen 80;
    server_name localhost 127.0.0.2 avisame.com;

    location / {
        proxy_pass http://127.0.0.2:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Puede accederse a la aplicación usando:

- `http://localhost`
- `http://127.0.0.1`
- `http://avisame.com`

Nginx manejará cualquiera de estas solicitudes, siempre que la configuración esté correcta y que el nombre de dominio (como `avisame.com`) esté correctamente mapeado a una IP en el archivo `hosts` (en el caso de un entorno local).

### Consideraciones:

- **Prioridad:** Nginx seleccionará el servidor cuya directiva `server_name` coincida más específicamente con el nombre de host de la solicitud.
- **Alias:** Puedes usar múltiples alias para el mismo servidor si quieres que diferentes nombres o direcciones IP apunten a la misma aplicación.

### Práctico:

Si estás trabajando en un entorno de desarrollo local, es muy útil poder usar diferentes nombres de host o [[IP]] para la misma aplicación, lo que te permite simular diferentes configuraciones o condiciones sin cambiar la configuración del servidor ni la aplicación.
