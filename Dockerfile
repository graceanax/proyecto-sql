FROM python:3.11-slim

# carpeta de trabajo
WORKDIR /app

# copiar archivos
COPY . .

# instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# exponer puerto
EXPOSE 5000

# ejecutar app
CMD ["python", "app.py"]