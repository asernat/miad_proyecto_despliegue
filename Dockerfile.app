FROM python:3.9

# Crear usuario que ejecuta la app
RUN adduser --disabled-password --gecos '' app-user

# Definir directorio de trabajo 
WORKDIR /opt/app

# Instalar dependencias
ADD ./app /opt/app/
RUN pip install --upgrade pip
RUN pip install -r /opt/app/requirements.txt

# Hacer el directorio de trabajo ejecutable 
RUN chmod +x /opt/app/run.sh
# Cambiar propiedad de la carpeta a app-user 
RUN chown -R app-user:app-user ./

USER app-user
# Puerto a exponer para el tablero 
EXPOSE 8001

# Comandos a ejecutar al correr el contenedor 
CMD ["bash", "./run.sh"]
