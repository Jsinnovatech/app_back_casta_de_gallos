# 🏋️ Schemas para Topes - MEJORES PRÁCTICAS
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from datetime import datetime, date
from enum import Enum

class TipoEntrenamientoEnum(str, Enum):
    """Enum para tipos de entrenamiento"""
    SPARRING = "sparring"
    TECNICA = "tecnica"
    RESISTENCIA = "resistencia"
    VELOCIDAD = "velocidad"
    TOP_ESPUELAS = "top_espuelas"
    TOP_SIN_ESPUELAS = "top_sin_espuelas"
    SPARRING_TECNICO = "sparring_tecnico"
    ACONDICIONAMIENTO_FISICO = "acondicionamiento_fisico"

class TipoEvaluacionEnum(str, Enum):
    """Enum para evaluación de desempeño"""
    EXCELENTE = "excelente_desempeno"
    BUENO = "buen_desempeno"
    REGULAR = "regular"
    NECESITA_MEJORAR = "necesita_mejorar"

class TopeBase(BaseModel):
    """Schema base para topes con validaciones mejoradas"""
    gallo_id: int = Field(..., gt=0, description="ID del gallo (debe ser positivo)")
    titulo: str = Field(..., min_length=3, max_length=255, description="Título del tope/entrenamiento")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Descripción detallada del entrenamiento")
    fecha_tope: datetime = Field(..., description="Fecha y hora del tope")
    ubicacion: Optional[str] = Field(None, min_length=2, max_length=255, description="Lugar del entrenamiento")
    duracion_minutos: Optional[int] = Field(None, ge=1, le=480, description="Duración en minutos (1-480 min)")
    tipo_entrenamiento: Optional[TipoEntrenamientoEnum] = Field(None, description="Tipo de entrenamiento")
    des_sparring: Optional[str] = Field(None, max_length=255, description="Descripción de sparring")
    tipo_resultado: Optional[TipoEvaluacionEnum] = Field(None, description="Evaluación del resultado")
    tipo_condicion_fisica: Optional[TipoEvaluacionEnum] = Field(None, description="Evaluación de condición física")
    peso_post_tope: Optional[str] = Field(None, max_length=255, description="Peso después del tope")
    fecha_proximo: Optional[datetime] = Field(None, description="Fecha del próximo entrenamiento")
    observaciones: Optional[str] = Field(None, max_length=2000, description="Observaciones del entrenamiento")

    @validator('fecha_tope')
    def validar_fecha_tope(cls, v):
        """La fecha no puede ser muy futura (máximo 1 año)"""
        if v > datetime.now().replace(year=datetime.now().year + 1):
            raise ValueError('La fecha del tope no puede ser más de 1 año en el futuro')
        return v
    
    @validator('titulo')
    def validar_titulo(cls, v):
        """Título no puede ser solo espacios"""
        if not v.strip():
            raise ValueError('El título no puede estar vacío')
        return v.strip()

class TopeCreate(TopeBase):
    """Schema para crear tope"""
    pass

class TopeUpdate(BaseModel):
    """Schema para actualizar tope con validaciones"""
    titulo: Optional[str] = Field(None, min_length=3, max_length=255, description="Título del tope")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Descripción del entrenamiento")
    fecha_tope: Optional[datetime] = Field(None, description="Fecha y hora del tope")
    ubicacion: Optional[str] = Field(None, min_length=2, max_length=255, description="Lugar del entrenamiento")
    duracion_minutos: Optional[int] = Field(None, ge=1, le=480, description="Duración en minutos")
    tipo_entrenamiento: Optional[TipoEntrenamientoEnum] = Field(None, description="Tipo de entrenamiento")
    des_sparring: Optional[str] = Field(None, max_length=255, description="Descripción de sparring")
    tipo_resultado: Optional[TipoEvaluacionEnum] = Field(None, description="Evaluación del resultado")
    tipo_condicion_fisica: Optional[TipoEvaluacionEnum] = Field(None, description="Evaluación de condición física")
    peso_post_tope: Optional[str] = Field(None, max_length=255, description="Peso después del tope")
    fecha_proximo: Optional[datetime] = Field(None, description="Fecha del próximo entrenamiento")
    observaciones: Optional[str] = Field(None, max_length=2000, description="Observaciones")

class TopeResponse(TopeBase):
    """Schema para respuesta de tope"""
    id: int
    user_id: Optional[int]
    video_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True