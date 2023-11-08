from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pickle

from app import app

def create_dropdown(id,label, options_list):
    return dmc.Select(
        id = id,
        label = label,
        data = [{'value':i, 'label': i} for i in options_list],
        value = options_list[0]
    )

datos = pickle.load(open("../datos/datos_tablero.pkl","rb"))

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
                                create_dropdown('selectp-pdepartamento','Departamento', sorted(list(set(datos['departamento_inmueble'])))),
                                create_dropdown('selectp-pciudad','Ciudad', sorted(list(set(datos['municipio_inmueble'])))),
                                create_dropdown('selectp-pestrato','Estrato', sorted(list(set(datos['estrato'])))),
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
                                            max = 20,
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
                        dmc.Button(id = 'submit-customer', children = 'Enviar'),
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
                                        dmc.Text("$ 0", id='pred_precio', color='black', style={'font-family':'Arial', 'font-size': 30, 'font-weight': 'bold'}, align='center'),
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

