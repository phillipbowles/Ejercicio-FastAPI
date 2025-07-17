# FastAPI JSONPlaceholder Proxy

Una API intermediaria desarrollada con **FastAPI** que consume la API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com) y expone endpoints limpios y transformados para el consumo de datos de usuarios.

## Características

- **Framework**: FastAPI con documentación automática
- **Cliente HTTP**: httpx para peticiones asíncronas
- **Containerización**: Docker para deployment
- **CI/CD**: GitHub Actions para deploy automático
- **Cloud**: Desplegado en AWS EC2
- **Sin base de datos**: Consultas en tiempo real a JSONPlaceholder

## Endpoints Disponibles

### API Base
- `GET /` - Información básica de la API
- `GET /health` - Health check del servicio
- `GET /docs` - Documentación interactiva (Swagger)
- `GET /redoc` - Documentación alternativa

### Usuarios
- `GET /api/v1/users` - Lista todos los usuarios (id, name, email)
- `GET /api/v1/users/{id}` - Obtiene todos los datos de un usuario
- `GET /api/v1/users/{id}/contact` - Información de contacto (name, email, phone)
- `GET /api/v1/users/{id}/address` - Información de dirección (street, city, zipcode, geo)

## API en Vivo

**URL Base**: http://3.137.152.28:8000

### Ejemplos de uso:

```bash
# Health check
curl http://3.137.152.28:8000/health

# Obtener todos los usuarios
curl http://3.137.152.28:8000/api/v1/users

# Obtener usuario específico
curl http://3.137.152.28:8000/api/v1/users/1

# Obtener contacto de usuario
curl http://3.137.152.28:8000/api/v1/users/1/contact

# Obtener dirección de usuario
curl http://3.137.152.28:8000/api/v1/users/1/address
```

### Documentación interactiva:
- **Swagger UI**: http://3.137.152.28:8000/docs
- **ReDoc**: http://3.137.152.28:8000/redoc

## Tecnologías Utilizadas

- **Python 3.11**
- **FastAPI** - Framework web moderno y rápido
- **httpx** - Cliente HTTP asíncrono
- **Uvicorn** - Servidor ASGI
- **Docker** - Containerización
- **GitHub Actions** - CI/CD
- **AWS EC2** - Hosting en la nube

## Estructura del Proyecto

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── routes/
│   │   ├── __init__.py
│   │   └── users.py           # Endpoints de usuarios
│   └── services/
│       ├── __init__.py
│       └── external_api.py    # Servicio para consumir JSONPlaceholder
├── .github/
│   └── workflows/
│       └── deploy.yml         # Pipeline CI/CD
├── Dockerfile                 # Configuración Docker
├── deploy.sh                  # Script de deployment
├── requirements.txt           # Dependencias Python
└── README.md                  # Documentación
```

## Instalación y Ejecución

### Requisitos Previos
- Python 3.11+
- Docker (opcional, para containerización)
- Git

### Instalación Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/phillipbowles/Ejercicio-FastAPI.git
cd Ejercicio-FastAPI
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Acceder a la API:**
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

### Ejecución con Docker

1. **Construir la imagen:**
```bash
docker build -t fastapi-app .
```

2. **Ejecutar el contenedor:**
```bash
docker run -d --name fastapi-container -p 8000:8000 fastapi-app
```

3. **Verificar que está corriendo:**
```bash
docker ps
curl http://localhost:8000/health
```

4. **Ver logs:**
```bash
docker logs fastapi-container
```

5. **Detener el contenedor:**
```bash
docker stop fastapi-container
docker rm fastapi-container
```

### Script de Deploy Automatizado

Para deployment en producción, usar el script incluido:

```bash
chmod +x deploy.sh
./deploy.sh
```

## CI/CD con GitHub Actions

El proyecto incluye un pipeline automatizado que se ejecuta en cada push a la rama `main`:

1. **Checkout del código**
2. **Conexión SSH a EC2**
3. **Actualización del código**
4. **Limpieza de contenedores existentes**
5. **Build y deploy de nueva versión**
6. **Health checks automáticos**

### Configuración de Secrets

Para el deployment en AWS EC2, configurar estos secrets en GitHub:

```
EC2_HOST=3.137.152.28
EC2_USER=ec2-user
EC2_SSH_KEY=-----BEGIN RSA PRIVATE KEY-----
[contenido de la clave privada]
-----END RSA PRIVATE KEY-----
```

## Testing

### Health Check Manual
```bash
curl -f http://3.137.152.28:8000/health
```

### Pruebas de Endpoints
```bash
# Probar todos los usuarios
curl http://3.137.152.28:8000/api/v1/users | jq '.[0:3]'

# Probar usuario específico
curl http://3.137.152.28:8000/api/v1/users/1 | jq '.'

# Probar contacto
curl http://3.137.152.28:8000/api/v1/users/1/contact | jq '.'

# Probar dirección
curl http://3.137.152.28:8000/api/v1/users/1/address | jq '.'
```

## Respuestas de la API

### GET /api/v1/users
```json
[
  {
    "id": 1,
    "name": "Leanne Graham",
    "email": "Sincere@april.biz"
  },
  {
    "id": 2,
    "name": "Ervin Howell",
    "email": "Shanna@melissa.tv"
  }
]
```

### GET /api/v1/users/1
```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
}
```

### GET /api/v1/users/1/contact
```json
{
  "name": "Leanne Graham",
  "email": "Sincere@april.biz",
  "phone": "1-770-736-8031 x56442"
}
```

### GET /api/v1/users/1/address
```json
{
  "street": "Kulas Light",
  "city": "Gwenborough",
  "zipcode": "92998-3874",
  "geo": {
    "lat": "-37.3159",
    "lng": "81.1496"
  }
}
```

## Configuración de Desarrollo

### Variables de Entorno (Opcional)
```bash
# .env
API_BASE_URL=https://jsonplaceholder.typicode.com
API_TIMEOUT=30
LOG_LEVEL=INFO
```

### Dependencias de Desarrollo
```bash
pip install pytest pytest-asyncio httpx
```

## Troubleshooting

### Puerto 8000 ocupado
```bash
# Encontrar proceso usando el puerto
sudo lsof -i :8000

# Detener contenedores Docker en el puerto
docker stop $(docker ps -q --filter "publish=8000-8000")
```

### Logs del contenedor
```bash
docker logs fastapi-container --tail 50 -f
```

### Reiniciar servicio
```bash
./deploy.sh
```

## Notas de Desarrollo

- La API consume datos en tiempo real desde JSONPlaceholder
- No se utiliza base de datos local
- Todos los endpoints incluyen manejo de errores HTTP
- La aplicación incluye middleware CORS para desarrollo
- Logs estructurados para monitoreo en producción

## Contribución

1. Fork el proyecto
2. Crear una rama para la feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto es parte de un ejercicio técnico.

## Autor

**Phillip Bowles**
- GitHub: [@phillipbowles](https://github.com/phillipbowles)
- Proyecto: [Ejercicio-FastAPI](https://github.com/phillipbowles/Ejercicio-FastAPI)

---

⚡ **API en vivo**: http://3.137.152.28:8000 | 📚 **Docs**: http://3.137.152.28:8000/docs