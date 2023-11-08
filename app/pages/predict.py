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
                                create_dropdown('selectp-barrio','Barrio', sorted(list(set(datos['barrio'])))),
                                create_dropdown('selectp-ocupante','Ocupantes', sorted(list(set(datos['ocupante'])))),
                                create_dropdown('selectp-total_cupos_parquedaro','Cupos parqueadero', sorted(list(set(datos['total_cupos_parquedaro'])))),
                                create_dropdown('selectp-cocina','Cocina', sorted(list(set(datos['cocina'])))),
                                create_dropdown('selectp-clase_inmueble','Clase inmueble', sorted(list(set(datos['clase_inmueble'])))),
                                create_dropdown('selectp-estructura_reforzada','Estructura reforzada', sorted(list(set(datos['estructura_reforzada'])))),
                                create_dropdown('selectp-tipo_garaje','Tipo garaje', sorted(list(set(datos['tipo_garaje'])))),
                                create_dropdown('selectp-detalle_material','Detalle material', sorted(list(set(datos['detalle_material'])))),
                                create_dropdown('selectp-closet','Closet', sorted(list(set(datos['closet'])))),
                                create_dropdown('selectp-balcon','Balcon', sorted(list(set(datos['balcon'])))),
                                create_dropdown('selectp-calidad_acabados_madera','Calidad acabados madera', sorted(list(set(datos['calidad_acabados_madera'])))),


                                
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
                Output('selectp-barrio', 'value'),
                Output('selectp-ocupante', 'value'),
                Output('selectp-total_cupos_parquedaro', 'value'),
                Output('selectp-cocina', 'value'),
                Output('selectp-clase_inmueble', 'value'),
                Output('selectp-estructura_reforzada', 'value'),
                Output('selectp-tipo_garaje', 'value'),
                Output('selectp-detalle_material', 'value'),
                Output('selectp-closet', 'value'),
                Output('selectp-balcon', 'value'),
                Output('selectp-calidad_acabados_madera', 'value'),

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
                State('selectp-barrio', 'value'),
                State('selectp-ocupante', 'value'),
                State('selectp-total_cupos_parquedaro', 'value'),
                State('selectp-cocina', 'value'),
                State('selectp-clase_inmueble', 'value'),
                State('selectp-estructura_reforzada', 'value'),
                State('selectp-tipo_garaje', 'value'),
                State('selectp-detalle_material', 'value'),
                State('selectp-closet', 'value'),
                State('selectp-balcon', 'value'),
                State('selectp-calidad_acabados_madera', 'value'),

                prevent_inital_update = True,
                )
def update_prob(n , randomize, pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado,barrio,ocupante,total_cupos_parquedaro,cocina,clase_inmueble,estructura_reforzada,tipo_garaje,detalle_material,closet,balcon,calidad_acabados_madera):
    
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
        inmueble_promedio['barrio'] = barrio
        inmueble_promedio['ocupante'] = ocupante
        inmueble_promedio['total_cupos_parquedaro'] = total_cupos_parquedaro
        inmueble_promedio['cocina'] = cocina
        inmueble_promedio['clase_inmueble'] = clase_inmueble
        inmueble_promedio['estructura_reforzada'] = estructura_reforzada
        inmueble_promedio['tipo_garaje'] = tipo_garaje
        inmueble_promedio['detalle_material'] = detalle_material
        inmueble_promedio['closet'] = closet
        inmueble_promedio['balcon'] = balcon
        inmueble_promedio['calidad_acabados_madera'] = calidad_acabados_madera

        inmueble_promedio_t = cat_econder.transform(pd.DataFrame.from_dict(inmueble_promedio, orient='index').T)
        inmueble_promedio_selected = fwiz.transform(inmueble_promedio_t)
        pred_precio = model.predict(inmueble_promedio_selected)[0]
        pred_precio = "$ {:.2f}".format(pred_precio)

        return pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado,barrio,ocupante,total_cupos_parquedaro,cocina,clase_inmueble,estructura_reforzada,tipo_garaje,detalle_material,closet,balcon,calidad_acabados_madera
    
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

        barrio = random.choice(list(set(f_datos['barrio'])))
        f_datos = datos.query(f"barrio == {barrio}")
        
        ocupante = random.choice(list(set(f_datos['ocupante'])))
        f_datos = datos.query(f"ocupante == {ocupante}")

        total_cupos_parquedaro = random.choice(list(set(f_datos['total_cupos_parquedaro'])))
        f_datos = datos.query(f"total_cupos_parquedaro == {total_cupos_parquedaro}")

        cocina = random.choice(list(set(f_datos['cocina'])))
        f_datos = datos.query(f"cocina == {cocina}")

        clase_inmueble = random.choice(list(set(f_datos['clase_inmueble'])))
        f_datos = datos.query(f"clase_inmueble == {clase_inmueble}")

        estructura_reforzada = random.choice(list(set(f_datos['estructura_reforzada'])))
        f_datos = datos.query(f"estructura_reforzada == {estructura_reforzada}")

        tipo_garaje = random.choice(list(set(f_datos['tipo_garaje'])))
        f_datos = datos.query(f"tipo_garaje == {tipo_garaje}")

        detalle_material = random.choice(list(set(f_datos['detalle_material'])))
        f_datos = datos.query(f"detalle_material == {detalle_material}")

        closet = random.choice(list(set(f_datos['closet'])))
        f_datos = datos.query(f"closet == {closet}")

        balcon = random.choice(list(set(f_datos['balcon'])))
        f_datos = datos.query(f"balcon == {balcon}")

        calidad_acabados_madera = random.choice(list(set(f_datos['calidad_acabados_madera'])))
        f_datos = datos.query(f"calidad_acabados_madera == {calidad_acabados_madera}")



        return pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado ,barrio,ocupante,total_cupos_parquedaro,cocina,clase_inmueble,estructura_reforzada,tipo_garaje,detalle_material,closet,balcon,calidad_acabados_madera
    else:
        return pred_precio, departamento, ciudad, estrato, tipo_inmueble, area_valorada, sismoresistentes, numero_piso, antiguedad, administracion, habitaciones, bano_privado ,barrio,ocupante,total_cupos_parquedaro,cocina,clase_inmueble,estructura_reforzada,tipo_garaje,detalle_material,closet,balcon,calidad_acabados_madera

