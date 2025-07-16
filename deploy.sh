#!/bin/bash

# Detener y eliminar contenedor anterior
echo "Eliminando contenedor anterior (si existe)..."
docker stop fastapi-proxy || true
docker rm fastapi-proxy || true

# Construir imagen
echo "Construyendo imagen..."
docker build -t fastapi-proxy .

# Correr contenedor
echo "Levantando contenedor en puerto 8000..."
docker run -d --name fastapi-proxy -p 8000:8000 fastapi-proxy

# Verificar estado
echo "Contenedor en ejecución:"
docker ps | grep fastapi-proxy
