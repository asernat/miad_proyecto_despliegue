from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pickle
import joblib
from pycaret.regression import load_model 
import random
from app import app
import pandas as pd

def create_dropdown(id,label, options_list):
    return dmc.Select(
        id = id,
        label = label,
        data = [{'value':i, 'label': i} for i in options_list],
        value = options_list[0]
    )

datos = pickle.load(open("../datos/datos_tablero.pkl","rb"))

fwiz = joblib.load("../modelos/fwiz.joblib")
cat_econder = joblib.load("../modelos/cat_econder.joblib")
vars_dict = joblib.load("../modelos/vars_dict.joblib")
model = load_model(r"../modelos\best_model-pipeline") 
inmueble_promedio = pickle.load(open("../modelos\inmueble_promedio.pkl","rb"))

layout = html.Div(
    children=[
        dmc.Title(children = 'Predicción del precio de la vivienda', order = 3, style = {'font-family':'Arial', 'text-align':'center', 'color' :'black'}),
        dmc.Paper(
            m = 'sm',
            pb = 'sm',
            shadow = 'md',
            withBorder = True,
            radius = 'md',
            children = [
                dmc.Stack(
                    align = 'center',
                    children = [
                        dmc.Title('Configure una vivienda', order = 4, style = {'text-align':'center'}),
                        dmc.Button( id = 'randomize', children = 'Vivienda aleatoria', size = 'sm'),
                        dmc.SimpleGrid(
                            cols = 4,
                            children = [
                                create_dropdown('selectp-departamento','Departamento', sorted(list(set(datos['departamento_inmueble'])))),
                                create_dropdown('selectp-ciudad','Ciudad', sorted(list(set(datos['municipio_inmueble'])))),
                                create_dropdown('selectp-estrato','Estrato', sorted(list(set(datos['estrato'])))),
                                create_dropdown('selectp-tipo_inmueble','Tipo inmueble', sorted(list(set(datos['tipo_inmueble'])))),
                                html.Div(
                                    children = [
                                        html.Label('Área valorada', style={'font-size': 14, 'font-weight': '500'}),
                                        dmc.Slider(
                                            id='sliderp-area_valorada',
                                            max = 500,
                                            value=0,
                                            mb=35,
                                        ),
                                    ]
                                ),
                                #create_dropdown('selectp-garajes','Garajes', sorted(list(set(datos['numero_total_de_garajes'])))),
                                create_dropdown('selectp-sismoresistentes','Sismo Resistentes', sorted(list(set(datos['ajustes_sismoresistentes'])))),
                                create_dropdown('selectp-numero_piso','Número de Piso', sorted(list(set(datos['numero_piso'])))),
                                 html.Div(
                                    children = [
                                        html.Label('Antigüedad', style={'font-size': 14, 'font-weight': '500'}),
                                        dmc.Slider(
                                            id='sliderp-vetustez',
                                            max = 80,
                                            value=0,
                                            mb=35,
                                        ),
                                    ]
                                ),
                                create_dropdown('selectp-administracion','Administración', sorted(list(set(datos['administracion'])))),
                                create_dropdown('selectp-habitaciones','Habitaciones', sorted(list(set(datos['habitaciones'])))),
                                create_dropdown('selectp-bano_privado','Número de Baños', sorted(list(set(datos['bano_privado'])))),


                                
                            ]
                        ),
                        dmc.Button(id = 'submit-inmueble', children = 'Enviar'),
                        dmc.Paper(
                            radius="0", # or p=10 for border-radius of 10px
                            withBorder=True,
                            shadow='xs',
                            p='sm',
                            style={'height':'100px', 'width':'400px', 'align':'center'},
                            children=[
                                dmc.Text('Predicción del precio de la vivienda', color='black', style={'font-family':'Arial', 'font-size': 14, 'font-weight': 'bold'}, align='center'),
                                html.Div(
                                    style= {'background-color':'WhiteSmoke', 'border-color':'black', 'border':'1px solid black'},
                                    children=[ 
                                        dmc.Text("-", id='pred_precio', color='black', style={'font-family':'Arial', 'font-size': 30, 'font-weight': 'bold'}, align='center'),
                                    ]
                                )                       
                            ],
                        ),                          
                    ]
                )
            ]
        )
    ]
)

@app.callback(Output('pred_precio', 'children'),
                Output('selectp-departamento', 'value'),
                Output('selectp-ciudad', 'value'),
                Output('selectp-estrato', 'value'),
                Output('selectp-tipo_inmueble', 'value'),
                Output('sliderp-area_valorada', 'value'),
                Output('selectp-sismoresistentes', 'value'),
                Output('selectp-numero_piso', 'value'),
                Output('sliderp-vetustez', 'value'),
                Output('selectp-administracion','value'),
                Output('selectp-habitaciones', 'value'),
                Output('selectp-bano_privado', 'value'),
                Input('submit-inmueble', 'n_clicks'),
                Input('randomize', 'n_clicks'),
                State('pred_precio', 'children'),                
                State('selectp-departamento', 'value'),                
                State('selectp-ciudad', 'value'),
                State('selectp-estrato', 'value'),
                State('selectp-tipo_inmueble', 'value'),
                State('sliderp-area_valorada', 'value'),
                State('selectp-sismoresistentes', 'value'),
                State('selectp-numero_piso', 'value'),
                State('sliderp-vetustez', 'value'),
                State('selectp-administracion','value'),
                State('selectp-habitaciones', 'value'),
                State('selectp-bano_privado', 'value'),
                prevent_inital_update = True,
                )
def update_prob(n , randomize, pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado):
    
    if ctx.triggered_id == 'submit-inmueble':

        inmueble_promedio['departamento_inmueble'] = departamento
        inmueble_promedio['municipio_inmueble'] = ciudad
        inmueble_promedio['estrato'] = estrato
        inmueble_promedio['tipo_inmueble'] = tipo_inmueble
        inmueble_promedio['ajustes_sismoresistentes'] = sismoresistentes
        inmueble_promedio['numero_piso'] = numero_piso
        inmueble_promedio['administracion'] = administracion
        inmueble_promedio['habitaciones'] = habitaciones
        inmueble_promedio['bano_privado'] = bano_privado
        inmueble_promedio['vetustez'] = antiguedad
        inmueble_promedio['area_valorada'] = area_valorada


        inmueble_promedio_t = cat_econder.transform(pd.DataFrame.from_dict(inmueble_promedio, orient='index').T)
        inmueble_promedio_selected = fwiz.transform(inmueble_promedio_t)
        pred_precio = model.predict(inmueble_promedio_selected)[0]
        pred_precio = "$ {:.2f}".format(pred_precio)

        return pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado
    
    elif ctx.triggered_id == 'randomize':
        
        departamento = random.choice(list(set(datos['departamento_inmueble'])))
        f_datos = datos.query(f"departamento_inmueble == '{departamento}'")

        ciudad = random.choice(list(set(f_datos['municipio_inmueble'])))
        f_datos = datos.query(f"municipio_inmueble == '{ciudad}'")

        estrato = random.choice(list(set(f_datos['estrato'])))
        f_datos = datos.query(f"estrato == {estrato}")

        tipo_inmueble = random.choice(list(set(f_datos['tipo_inmueble'])))
        f_datos = datos.query(f"tipo_inmueble == '{tipo_inmueble}'")

        sismoresistentes = random.choice(list(set(f_datos['ajustes_sismoresistentes'])))
        f_datos = datos.query(f"ajustes_sismoresistentes == '{sismoresistentes}'")

        numero_piso = random.choice(list(set(f_datos['numero_piso'])))
        f_datos = datos.query(f"numero_piso == {numero_piso}")

        administracion = random.choice(list(set(f_datos['administracion'])))
        f_datos = datos.query(f"administracion == '{administracion}'")

        habitaciones = random.choice(list(set(f_datos['habitaciones'])))
        f_datos = datos.query(f"habitaciones == {habitaciones}")

        bano_privado = random.choice(list(set(f_datos['bano_privado'])))
        f_datos = datos.query(f"bano_privado == {bano_privado}")

        antiguedad = random.choice(list(set(f_datos['vetustez'])))
        f_datos = datos.query(f"vetustez == {max(min(80,antiguedad),0)}")

        area_valorada = random.choice(list(set(f_datos['area_valorada'])))
        f_datos = datos.query(f"area_valorada == {max(min(500,area_valorada),0)}")

        return pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado
    else:
        return pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado

