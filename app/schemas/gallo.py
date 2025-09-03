# 🔥 app/schemas/gallo.py - Schemas ÉPICOS para Técnica Recursiva Genealógica
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from decimal import Decimal

# ========================
# 🎯 SCHEMAS BASE
# ========================

class RazaBase(BaseModel):
    """📋 Schema base para razas"""
    id: int
    nombre: str
    descripcion: Optional[str] = None
    origen: Optional[str] = None
    
    class Config:
        from_attributes = True

class PhotoData(BaseModel):
    """📸 Schema para datos de foto"""
    url: str
    public_id: Optional[str] = None
    photo_type: str = Field(..., description="principal, adicional, thumbnail")
    width: Optional[int] = None
    height: Optional[int] = None
    size_bytes: Optional[int] = None
    created_at: Optional[datetime] = None

class PhotoUrls(BaseModel):
    """📸 Schema para URLs de fotos con transformaciones"""
    original: str
    thumbnail: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None
    optimized: Optional[str] = None

# ========================
# 🐓 SCHEMAS DE GALLO
# ========================

class GalloBase(BaseModel):
    """🐓 Schema base de gallo"""
    nombre: str = Field(..., min_length=2, max_length=255)
    codigo_identificacion: str = Field(..., min_length=3, max_length=20)
    raza_id: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    peso: Optional[Decimal] = Field(None, ge=0.5, le=10.0)
    altura: Optional[int] = Field(None, ge=20, le=100)
    color: Optional[str] = Field(None, max_length=100)
    estado: str = Field(default="activo", max_length=20)
    procedencia: Optional[str] = Field(None, max_length=255)
    notas: Optional[str] = None
    
    # Campos adicionales detallados
    color_plumaje: Optional[str] = Field(None, max_length=100)
    color_placa: Optional[str] = Field(None, max_length=50)
    ubicacion_placa: Optional[str] = Field(None, max_length=50)
    color_patas: Optional[str] = Field(None, max_length=50)
    criador: Optional[str] = Field(None, max_length=255)
    propietario_actual: Optional[str] = Field(None, max_length=255)
    observaciones: Optional[str] = None
    numero_registro: Optional[str] = Field(None, max_length=100)
    
    @validator('codigo_identificacion')
    def validate_codigo(cls, v):
        if v:
            return v.strip().upper()
        return v
    
    @validator('estado')
    def validate_estado(cls, v):
        estados_validos = ['activo', 'inactivo', 'padre', 'madre', 'campeon', 'retirado', 'vendido']
        if v and v.lower() not in estados_validos:
            raise ValueError(f"Estado debe ser uno de: {', '.join(estados_validos)}")
        return v.lower() if v else "activo"

class GalloCreate(GalloBase):
    """🔥 Schema para crear gallo con técnica recursiva genealógica"""
    
    # Control de padres
    crear_padre: bool = Field(default=False, description="Crear padre automáticamente")
    crear_madre: bool = Field(default=False, description="Crear madre automáticamente")
    padre_id: Optional[int] = Field(None, description="ID de padre existente")
    madre_id: Optional[int] = Field(None, description="ID de madre existente")
    
    # Datos del padre (si crear_padre=True)
    padre_nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    padre_codigo: Optional[str] = Field(None, min_length=3, max_length=20)
    padre_raza_id: Optional[int] = None
    padre_color: Optional[str] = Field(None, max_length=100)
    padre_peso: Optional[Decimal] = Field(None, ge=0.5, le=10.0)
    padre_procedencia: Optional[str] = Field(None, max_length=255)
    padre_notas: Optional[str] = None
    padre_color_plumaje: Optional[str] = Field(None, max_length=100)
    padre_color_patas: Optional[str] = Field(None, max_length=50)
    padre_criador: Optional[str] = Field(None, max_length=255)
    
    # Datos de la madre (si crear_madre=True)
    madre_nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    madre_codigo: Optional[str] = Field(None, min_length=3, max_length=20)
    madre_raza_id: Optional[int] = None
    madre_color: Optional[str] = Field(None, max_length=100)
    madre_peso: Optional[Decimal] = Field(None, ge=0.5, le=10.0)
    madre_procedencia: Optional[str] = Field(None, max_length=255)
    madre_notas: Optional[str] = None
    madre_color_plumaje: Optional[str] = Field(None, max_length=100)
    madre_color_patas: Optional[str] = Field(None, max_length=50)
    madre_criador: Optional[str] = Field(None, max_length=255)
    
    @validator('padre_codigo')
    def validate_padre_codigo(cls, v, values):
        if values.get('crear_padre') and not v:
            raise ValueError("Código del padre es obligatorio si crear_padre=True")
        if v:
            return v.strip().upper()
        return v
    
    @validator('madre_codigo')
    def validate_madre_codigo(cls, v, values):
        if values.get('crear_madre') and not v:
            raise ValueError("Código de la madre es obligatorio si crear_madre=True")
        if v:
            return v.strip().upper()
        return v

class GalloSimple(BaseModel):
    """📋 Schema simple de gallo para listas"""
    id: int
    nombre: str
    codigo_identificacion: str
    peso: Optional[Decimal] = None
    color: Optional[str] = None
    estado: str
    foto_principal_url: Optional[str] = None
    url_foto_cloudinary: Optional[str] = None
    tipo_registro: str
    id_gallo_genealogico: Optional[int] = None
    padre_id: Optional[int] = None
    madre_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class GalloResponse(BaseModel):
    """📋 Schema de respuesta para gallo"""
    success: bool = True
    data: Dict[str, Any]
    message: str = "Operación exitosa"

# ========================
# 🧬 SCHEMAS GENEALÓGICOS
# ========================

class ArbolGenealogico(BaseModel):
    """🌳 Árbol genealógico completo"""
    gallo_base: GalloSimple
    ancestros: List[Dict[str, Any]] = []
    descendientes: List[Dict[str, Any]] = []
    familia_completa: List[GalloSimple] = []
    estadisticas: Dict[str, Any]

# ========================
# 🔍 SCHEMAS DE BÚSQUEDA
# ========================

class GalloSearchParams(BaseModel):
    """🔍 Parámetros de búsqueda de gallos"""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    search: Optional[str] = Field(None, min_length=2)
    raza_id: Optional[int] = None
    estado: Optional[str] = None
    tiene_foto: Optional[bool] = None
    tiene_padres: Optional[bool] = None
    created_after: Optional[date] = None
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    include_genealogy: bool = Field(default=False)

# ========================
# ✅ SCHEMAS DE RESPUESTA
# ========================

class SuccessResponse(BaseModel):
    """✅ Respuesta genérica de éxito"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """❌ Respuesta de error"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None