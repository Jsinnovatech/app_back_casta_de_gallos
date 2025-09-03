# 📋 Schemas Pydantic para Suscripciones - Validaciones Completas
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from datetime import datetime, date
from enum import Enum
from decimal import Decimal

class PlanTipo(str, Enum):
    """Tipos de plan disponibles"""
    GRATUITO = "gratuito"
    BASICO = "basico"
    PREMIUM = "premium"
    PROFESIONAL = "profesional"

class EstadoSuscripcion(str, Enum):
    """Estados de suscripción"""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"

class SuscripcionBase(BaseModel):
    """Schema base para suscripciones"""
    plan_type: str = Field(..., description="Tipo de plan")
    plan_name: str = Field(..., description="Nombre del plan")
    precio: Decimal = Field(..., ge=0, description="Precio del plan")
    
    # Límites
    gallos_maximo: int = Field(..., ge=1, le=999, description="Máximo de gallos permitidos")
    topes_por_gallo: int = Field(..., ge=1, le=999, description="Topes por gallo")
    peleas_por_gallo: int = Field(..., ge=1, le=999, description="Peleas por gallo")
    vacunas_por_gallo: int = Field(..., ge=1, le=999, description="Vacunas por gallo")

class SuscripcionCreate(SuscripcionBase):
    """Schema para crear suscripción"""
    user_id: int = Field(..., gt=0, description="ID del usuario")
    fecha_inicio: date = Field(default_factory=date.today, description="Fecha de inicio")
    fecha_fin: Optional[date] = Field(None, description="Fecha de finalización")
    
    @validator('fecha_fin')
    def validar_fecha_fin(cls, v, values):
        if v and 'fecha_inicio' in values and v <= values['fecha_inicio']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v

class SuscripcionResponse(SuscripcionBase):
    """Schema de respuesta para suscripción"""
    id: int
    user_id: int
    status: str
    fecha_inicio: date
    fecha_fin: Optional[date]
    created_at: datetime
    updated_at: datetime
    
    # Campos calculados
    dias_restantes: Optional[int] = None
    esta_activa: bool = Field(default=True)
    es_premium: bool = Field(default=False)
    
    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: float,
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

class PlanCatalogoResponse(BaseModel):
    """Schema de respuesta para plan del catálogo"""
    id: int
    codigo: str
    nombre: str
    precio: Decimal
    duracion_dias: int
    
    # Límites
    gallos_maximo: int
    topes_por_gallo: int
    peleas_por_gallo: int
    vacunas_por_gallo: int
    
    # Características
    soporte_premium: bool
    respaldo_nube: bool
    estadisticas_avanzadas: bool
    videos_ilimitados: bool
    
    # UI
    destacado: bool
    activo: bool
    orden: int
    
    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: float
        }