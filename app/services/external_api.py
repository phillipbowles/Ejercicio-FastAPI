import httpx
from typing import List, Dict, Any, Optional
import asyncio
from fastapi import HTTPException, status

class ExternalAPIService:
    """
    Servicio para consumir la API externa de JSONPlaceholder
    """
    
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.timeout = 30.0  # Timeout de 30 segundos
        
    async def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Método privado para realizar peticiones HTTP
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                
                # Verificar status code
                if response.status_code == 404:
                    return None
                
                # Lanzar excepción si hay error HTTP
                response.raise_for_status()
                
                # Retornar JSON
                return response.json()
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Timeout al consultar API externa"
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error en API externa: {e.response.status_code}"
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error de conexión con API externa"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los usuarios desde JSONPlaceholder
        """
        try:
            users_data = await self._make_request("/users")
            
            if users_data is None:
                return []
                
            # Validar que sea una lista
            if not isinstance(users_data, list):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Respuesta inválida de API externa"
                )
            
            return users_data
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al obtener usuarios"
            )
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un usuario específico por ID desde JSONPlaceholder
        """
        try:
            # Validar que el ID sea válido
            if user_id <= 0:
                return None
                
            user_data = await self._make_request(f"/users/{user_id}")
            
            if user_data is None:
                return None
                
            # Validar que sea un diccionario
            if not isinstance(user_data, dict):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Respuesta inválida de API externa"
                )
            
            return user_data
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al obtener usuario"
            )
    
    async def health_check(self) -> bool:
        """
        Verifica si la API externa está disponible
        """
        try:
            # Intentar obtener el primer usuario como health check
            result = await self._make_request("/users/1")
            return result is not None
            
        except Exception:
            return False
    
    async def get_multiple_users(self, user_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Obtiene múltiples usuarios por ID de forma concurrente
        Método útil para optimizar múltiples consultas
        """
        try:
            # Crear tareas concurrentes
            tasks = [self.get_user_by_id(user_id) for user_id in user_ids]
            
            # Ejecutar todas las tareas concurrentemente
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filtrar resultados válidos
            valid_users = []
            for result in results:
                if isinstance(result, dict):
                    valid_users.append(result)
                elif isinstance(result, Exception):
                    # Log error but continue with other users
                    continue
            
            return valid_users
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al obtener múltiples usuarios"
            )