# Proyecto SQL Injection Derecho informático

Este proyecto es una aplicación Flask vulnerable utilizada para pruebas de seguridad (SQL Injection) en un entorno local controlado con fines educativos.

---

## Requisitos

- Docker  
- Docker Compose  

---

## Primera ejecución (construcción del ambiente)

```bash
docker compose up --build
````

Esto:
* Construye la imagen Docker
* Levanta el contenedor

---

## Acceso a la aplicación

Abrir en el navegador:

```
http://127.0.0.1:5001
```

o:

```
http://localhost:5001
```

> Se utiliza el puerto **5001** porque el puerto 5000 puede estar ocupado.

---

## Ejecuciones posteriores

Después de la primera vez:

```bash
docker compose up
```

---

## Ver logs del sistema

Para ver las peticiones, ataques y errores en tiempo real:

```bash
docker compose logs -f
```

Aquí se podrá ver:

* Requests HTTP (GET/POST)
* Intentos de ataque (OWASP ZAP / sqlmap)
* Consultas SQL ejecutadas
* Errores del servidor

---

## Detener el contenedor

Para detener completamente el proyecto:

```bash
docker compose down
```

## Notas

* Este proyecto es únicamente para fines educativos.
* Contiene vulnerabilidades intencionales como SQL Injection.
* No debe usarse en producción.

