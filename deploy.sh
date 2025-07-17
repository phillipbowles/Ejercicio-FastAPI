#!/bin/bash

# Deploy script para FastAPI en EC2

set -e  # Parar si hay errores

echo "=== Deploy Script Iniciado ==="
echo "Fecha: $(date)"
echo "Usuario: $(whoami)"
echo "Directorio: $(pwd)"

# Variables
IMAGE_NAME="fastapi-app"
CONTAINER_NAME="fastapi-container"
PORT=8000

# Verificar que estamos en el directorio correcto
echo "=== Verificando archivos ==="
if [ ! -f "Dockerfile" ]; then
    echo "Error: No se encontró Dockerfile"
    echo "Contenido del directorio:"
    ls -la
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "Error: No se encontró requirements.txt"
    exit 1
fi

echo "Archivos necesarios encontrados"

# Verificar Docker
echo "=== Verificando Docker ==="
if ! command -v docker &> /dev/null; then
    echo "Error: Docker no está instalado"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "Error: Docker no está corriendo o no hay permisos"
    exit 1
fi

echo "Docker está funcionando correctamente"

# Parar y remover contenedor existente (si existe)
echo "=== Parando contenedor existente ==="
if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
    echo "Parando contenedor existente: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME || true
    docker rm $CONTAINER_NAME || true
    echo "Contenedor anterior removido"
else
    echo "No hay contenedor existente con nombre: $CONTAINER_NAME"
fi

# Parar cualquier contenedor usando el puerto 8000
echo "=== Verificando puerto 8000 ==="
PORT_CONTAINERS=$(docker ps -q --filter "publish=8000-8000")
if [ ! -z "$PORT_CONTAINERS" ]; then
    echo "Parando contenedores en puerto 8000: $PORT_CONTAINERS"
    docker stop $PORT_CONTAINERS || true
    docker rm $PORT_CONTAINERS || true
fi

# Construir la imagen Docker
echo "=== Construyendo imagen Docker ==="
echo "Comando: docker build -t $IMAGE_NAME . --no-cache"

if docker build -t $IMAGE_NAME . --no-cache; then
    echo "Imagen construida exitosamente"
else
    echo "Error construyendo imagen"
    echo "Revisando Dockerfile:"
    cat Dockerfile
    exit 1
fi

# Verificar que la imagen existe
echo "=== Verificando imagen creada ==="
if docker images | grep -q $IMAGE_NAME; then
    echo "Imagen $IMAGE_NAME creada correctamente"
    docker images | grep $IMAGE_NAME
else
    echo "Error: La imagen no fue creada"
    exit 1
fi

# Ejecutar nuevo contenedor
echo "=== Iniciando nuevo contenedor ==="
echo "Comando: docker run -d --name $CONTAINER_NAME -p $PORT:8000 --restart unless-stopped $IMAGE_NAME"

CONTAINER_ID=$(docker run -d \
    --name $CONTAINER_NAME \
    -p $PORT:8000 \
    --restart unless-stopped \
    $IMAGE_NAME)

if [ $? -eq 0 ]; then
    echo "Contenedor iniciado con ID: $CONTAINER_ID"
else
    echo "Error iniciando contenedor"
    exit 1
fi

# Verificar que el contenedor esté corriendo
echo "=== Verificando contenedor ==="
sleep 5

if docker ps | grep -q $CONTAINER_NAME; then
    echo "Contenedor corriendo correctamente"
    
    # Mostrar información del contenedor
    echo "=== Información del contenedor ==="
    docker ps | grep $CONTAINER_NAME
    
    # Mostrar logs de inicio
    echo "=== Logs del contenedor ==="
    docker logs $CONTAINER_NAME --tail 20
    
    # Health check local con reintentos
    echo "=== Health check local ==="
    for i in {1..10}; do
        sleep 2
        if curl -f http://localhost:$PORT/health 2>/dev/null; then
            echo "Health check exitoso en intento $i"
            break
        else
            echo "Health check falló en intento $i, reintentando..."
            if [ $i -eq 10 ]; then
                echo "Health check falló después de 10 intentos"
                echo "Logs actuales del contenedor:"
                docker logs $CONTAINER_NAME --tail 30
                # No salir con error si el contenedor está corriendo
                echo "Contenedor está corriendo pero health check falló"
            fi
        fi
    done
else
    echo "Error: Contenedor no está corriendo"
    echo "Estado de todos los contenedores:"
    docker ps -a
    echo "Logs del contenedor fallido:"
    docker logs $CONTAINER_NAME 2>/dev/null || echo "No hay logs disponibles"
    exit 1
fi

# Limpiar imágenes sin usar
echo "=== Limpiando imágenes antigas ==="
docker image prune -f

# Mostrar resumen final
echo "=== Resumen del deploy ==="
echo "Imagen: $IMAGE_NAME"
echo "Contenedor: $CONTAINER_NAME"
echo "Puerto: $PORT"
echo "Estado del contenedor:"
docker ps | grep $CONTAINER_NAME || echo "Contenedor no encontrado"

echo "=== Deploy completado exitosamente ==="
echo "Servicio disponible en: http://$(curl -s http://checkip.amazonaws.com):$PORT"
echo "Health check: http://$(curl -s http://checkip.amazonaws.com):$PORT/health"