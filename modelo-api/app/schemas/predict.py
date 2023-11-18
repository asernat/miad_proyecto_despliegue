from typing import Any, List, Optional

from pydantic import BaseModel
from model.processing.validation import DataInputSchema

# Esquema de los resultados de predicción
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]

# Esquema para inputs múltiples
class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                    "departamento_inmueble": "ANTIOQUIA",
                    "municipio_inmueble": "MEDELLIN",
                    "estrato": 3.0,
                    "tipo_inmueble": "Apartamento",
                    "ajustes_sismoresistentes": "No disponible",
                    "numero_piso": 2.0,
                    "administracion": "Si",
                    "habitaciones": 3.0,
                    "bano_privado": 1.0,
                    "vetustez": 10.0,
                    "area_valorada": 75.295,
                    "barrio": 'POBLADO',
                    "ocupante": 'SinOcupante',
                    "total_cupos_parquedaro": 0.0,
                    "cocina": 1.0,
                    "clase_inmueble": 'Multifamiliar',
                    "estructura_reforzada": 'No disponible',
                    "tipo_garaje": 0.0,
                    "detalle_material": 'Pórticos',
                    "closet": 2.0,
                    "balcon": 0.0,
                    "calidad_acabados_madera": 2.0

                    }
                ]
            }
        }
