import typing as t
import pandas as pd
from model import __version__ as _version
from model.config.core import config
from model.processing.data_manager import load_pipeline
from model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}-{_version}.joblib"
inmueble_promedio_file_name = f"{config.app_config.pipeline_inmueble_promedio}-{_version}.pkl"
_avaluos_pipe, _inmueble_promedio = load_pipeline(file_name=pipeline_file_name, inmueble_promedio_file_name=inmueble_promedio_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)

    # Complementar variables con inmueble promedio
    for k,v in _inmueble_promedio.items():
        if k not in validated_data.columns:
            validated_data[k] = v
    
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _avaluos_pipe.predict(
            X=validated_data
        )
        results = {
            "predictions": [pred for pred in predictions], 
            "version": _version,
            "errors": errors,
        }

    return results
