from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.services.external_api import ExternalAPIService

# Crear router para usuarios
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Instancia del servicio para consumir API externa
api_service = ExternalAPIService()

@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_users():
    """
    Obtiene todos los usuarios con id, name y email
    """
    try:
        # Obtener usuarios desde JSONPlaceholder
        users_data = await api_service.get_all_users()
        
        # Transformar respuesta - solo devolver id, name y email
        users_filtered = []
        for user in users_data:
            users_filtered.append({
                "id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("email")
            })
        
        return users_filtered
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener usuarios"
        )

@router.get("/{user_id}", response_model=Dict[str, Any])
async def get_user_by_id(user_id: int):
    """
    Obtiene todos los datos de un usuario específico por ID
    """
    try:
        # Obtener usuario específico desde JSONPlaceholder
        user_data = await api_service.get_user_by_id(user_id)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        # Devolver todos los datos del usuario (transformados)
        return {
            "id": user_data.get("id"),
            "name": user_data.get("name"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "phone": user_data.get("phone"),
            "website": user_data.get("website"),
            "address": {
                "street": user_data.get("address", {}).get("street"),
                "suite": user_data.get("address", {}).get("suite"),
                "city": user_data.get("address", {}).get("city"),
                "zipcode": user_data.get("address", {}).get("zipcode"),
                "geo": {
                    "lat": user_data.get("address", {}).get("geo", {}).get("lat"),
                    "lng": user_data.get("address", {}).get("geo", {}).get("lng")
                }
            },
            "company": {
                "name": user_data.get("company", {}).get("name"),
                "catchPhrase": user_data.get("company", {}).get("catchPhrase"),
                "bs": user_data.get("company", {}).get("bs")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener usuario"
        )

@router.get("/{user_id}/contact", response_model=Dict[str, Any])
async def get_user_contact(user_id: int):
    """
    Obtiene información de contacto de un usuario (name, email, phone)
    """
    try:
        # Obtener usuario específico desde JSONPlaceholder
        user_data = await api_service.get_user_by_id(user_id)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        # Devolver solo información de contacto
        return {
            "name": user_data.get("name"),
            "email": user_data.get("email"),
            "phone": user_data.get("phone")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener información de contacto"
        )

@router.get("/{user_id}/address", response_model=Dict[str, Any])
async def get_user_address(user_id: int):
    """
    Obtiene información de dirección de un usuario (street, city, zipcode, geo.lat, geo.lng)
    """
    try:
        # Obtener usuario específico desde JSONPlaceholder
        user_data = await api_service.get_user_by_id(user_id)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        # Extraer información de dirección
        address_data = user_data.get("address", {})
        geo_data = address_data.get("geo", {})
        
        # Devolver solo información de dirección
        return {
            "street": address_data.get("street"),
            "city": address_data.get("city"),
            "zipcode": address_data.get("zipcode"),
            "geo": {
                "lat": geo_data.get("lat"),
                "lng": geo_data.get("lng")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener información de dirección"
        )