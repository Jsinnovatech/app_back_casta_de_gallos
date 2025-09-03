# 💰 Schemas para Inversiones
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TipoGastoEnum(str, Enum):
    """Tipos de gastos de inversión"""
    ALIMENTO = "alimento"
    MEDICINAS = "medicinas"
    VACUNAS = "vacunas"
    VITAMINAS = "vitaminas"
    INFRAESTRUCTURA = "infraestructura"
    EQUIPOS = "equipos"
    SERVICIOS_VETERINARIOS = "servicios_veterinarios"
    OTROS = "otros"

class InversionBase(BaseModel):
    """Schema base para inversiones"""
    año: int = Field(..., ge=2020, le=2030, description="Año de la inversión")
    mes: int = Field(..., ge=1, le=12, description="Mes de la inversión")
    tipo_gasto: TipoGastoEnum = Field(..., description="Tipo de gasto")
    costo: Decimal = Field(..., ge=0, description="Costo de la inversión")
    
    @validator('costo')
    def validar_costo(cls, v):
        if v < 0:
            raise ValueError('El costo no puede ser negativo')
        return round(v, 2)

class InversionCreate(InversionBase):
    """Schema para crear inversión"""
    pass

class InversionUpdate(BaseModel):
    """Schema para actualizar inversión"""
    año: Optional[int] = Field(None, ge=2020, le=2030)
    mes: Optional[int] = Field(None, ge=1, le=12)
    tipo_gasto: Optional[TipoGastoEnum] = None
    costo: Optional[Decimal] = Field(None, ge=0)

class InversionResponse(InversionBase):
    """Schema de respuesta para inversión"""
    id: int
    user_id: int
    fecha_registro: datetime
    
    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: float,
            datetime: lambda v: v.isoformat()
        }

class ResumenInversiones(BaseModel):
    """Schema para resumen de inversiones"""
    total_invertido: Decimal
    inversiones_por_tipo: Dict[str, Decimal]
    inversiones_por_mes: Dict[str, Decimal]
    promedio_mensual: Decimal
    
    class Config:
        json_encoders = {
            Decimal: float
        }