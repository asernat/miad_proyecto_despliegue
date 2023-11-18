import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from model import __version__ as _version
from model.config.core import TRAINED_MODEL_DIR, config
import pickle

def load_pipeline(*, file_name: str, inmueble_promedio_file_name:str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    inmueble_promedio_file_path = TRAINED_MODEL_DIR / inmueble_promedio_file_name

    trained_model = joblib.load(filename=file_path)
    inmueble_promedio = pickle.load(open(inmueble_promedio_file_path, "rb"))
    
    return trained_model, inmueble_promedio

