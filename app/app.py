import dash

app = dash.Dash(__name__, suppress_callback_exceptions = True, 
    title = 'Predicción del precio de vivienda en Colombia', 
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    
)
