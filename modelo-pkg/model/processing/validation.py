from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_cfg.features
        if validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    relevant_data = input_data[config.model_cfg.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class DataInputSchema(BaseModel):
    departamento_inmueble: Optional[str]
    municipio_inmueble: Optional[str]
    estrato: Optional[float]
    tipo_inmueble: Optional[str]
    ajustes_sismoresistentes: Optional[str]
    numero_piso: Optional[float]
    administracion: Optional[str]
    habitaciones: Optional[float]
    bano_privado: Optional[float]
    vetustez: Optional[float]
    area_valorada: Optional[float]
    barrio: Optional[str]
    ocupante: Optional[str]
    total_cupos_parquedaro: Optional[float]
    cocina: Optional[float]
    clase_inmueble: Optional[str]
    estructura_reforzada: Optional[str]
    tipo_garaje: Optional[float]
    detalle_material: Optional[str]
    closet: Optional[float]
    balcon: Optional[float]
    calidad_acabados_madera: Optional[float]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
