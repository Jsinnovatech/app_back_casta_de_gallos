# 💳 Schemas Pydantic para Pagos - Sistema Yape
from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from decimal import Decimal

class EstadoPago(str, Enum):
    """Estados de pago"""
    PENDIENTE = "pendiente"
    VERIFICANDO = "verificando"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

class MetodoPago(str, Enum):
    """Métodos de pago soportados"""
    YAPE = "yape"
    PLIN = "plin"
    TRANSFERENCIA = "transferencia"

class PagoBase(BaseModel):
    """Schema base para pagos"""
    plan_codigo: str = Field(..., min_length=3, max_length=20, description="Código del plan")
    monto: Decimal = Field(..., gt=0, le=1000, description="Monto a pagar en soles")
    metodo_pago: MetodoPago = Field(default=MetodoPago.YAPE, description="Método de pago")
    
    @validator('monto')
    def validar_monto(cls, v):
        if v <= 0:
            raise ValueError('El monto debe ser mayor a 0')
        if v > 1000:
            raise ValueError('El monto máximo es S/. 1000')
        return round(v, 2)

class PagoCreate(PagoBase):
    """Schema para crear pago"""
    referencia_yape: Optional[str] = Field(None, max_length=100, description="Número de operación Yape")
    
class PagoResponse(PagoBase):
    """Schema de respuesta para pago"""
    id: int
    user_id: int
    estado: EstadoPago
    qr_data: Optional[str] = None
    qr_url: Optional[HttpUrl] = None
    comprobante_url: Optional[HttpUrl] = None
    referencia_yape: Optional[str] = None
    
    # Fechas
    fecha_pago_usuario: Optional[datetime] = None
    fecha_verificacion: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Verificación admin
    verificado_por: Optional[int] = None
    notas_admin: Optional[str] = None
    
    # Datos adicionales
    intentos: int = 0
    
    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: float,
            datetime: lambda v: v.isoformat()
        }

class QRYapeResponse(BaseModel):
    """Schema de respuesta para QR Yape"""
    pago_id: int
    qr_data: str = Field(..., description="Datos del QR en formato texto")
    qr_url: HttpUrl = Field(..., description="URL de imagen QR en Cloudinary")
    monto: Decimal
    plan_nombre: str
    
    # Instrucciones paso a paso
    instrucciones: List[str] = [
        "1. Abre tu app Yape",
        "2. Escanea este código QR",
        "3. Confirma el pago por el monto exacto",
        "4. Toma captura del comprobante",
        "5. Sube la captura en la siguiente pantalla"
    ]
    
    # Info adicional
    tiempo_expiracion_minutos: int = 30
    numero_contacto: str = "+51 999 999 999"
    
    class Config:
        json_encoders = {
            Decimal: float
        }