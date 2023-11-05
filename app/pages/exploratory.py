import dash
from dash import html, dcc
import dash_mantine_components as dmc
import pickle
from app import app
import plotly.graph_objects as go

def create_dropdown(id,label, options_list):
    return dmc.Select(
        id = id,
        label = label,
        data = [{'value':i, 'label': i} for i in options_list],
        value = options_list[0]
    )

datos = pickle.load(open("../datos/datos_tablero.pkl","rb"))

layout = html.Div(
    style= {'margin-top':'70px', 'background-color':'WhiteSmoke', 'width':'100%', 'height':'100%', 'align':'center', 'display':'inline'},
    children=[
        dmc.Text('Este sitio le permite obtener el precio justo de vivienda para compra o venta en Colombia relacionada a sus preferencias', style = {'font-family':'Arial', 'fontSize':12, 'font-weight': 'bold', 'width':'100%', 'height':'100%'}, align='center'),
        dmc.Space(h=30),
        dmc.Group(
            align = 'center',
            position = 'center',
            children=[
                dmc.Paper(
                    radius="md", # or p=10 for border-radius of 10px
                    withBorder=True,
                    shadow='xs',
                    p='sm',
                    style={'height':'155px', 'width':'300px', 'align':'center'},
                    children=[
                        dmc.Text('Total inmuebles', color='black', style={'font-family':'Arial', 'font-size': 14, 'font-weight': 'bold'}, align='center'),
                        html.Div(
                            style= {'background-color':'WhiteSmoke', 'border-color':'black', 'border':'1px solid black'},
                            children=[ 
                                dmc.Text(datos.shape[0], id='total_inmuebles', color='black', style={'font-family':'Arial', 'font-size': 50, 'font-weight': 'bold'}, align='center'),
                            ]
                        )                       
                    ],
                ),    
                dmc.Paper(
                    radius="md", # or p=10 for border-radius of 10px
                    withBorder=True,
                    shadow='xs',
                    p='sm',
                    style={'height':'200px'},
                    children=[
                        dmc.Text('Seleccione el filtro', color='black', style={'font-family':'Arial', 'font-size': 14, 'font-weight': 'bold'} , align='center'),
                        dmc.SimpleGrid(
                            cols = 3,
                            children = [
                                create_dropdown('select-departamento','Departamento', ["Ninguno"]+sorted(list(set(datos['departamento_inmueble'])))),
                                create_dropdown('select-ciudad','Ciudad', ["Ninguno"]+sorted(list(set(datos['municipio_inmueble'])))),
                                create_dropdown('select-estrato','Estrato', ["Ninguno"]+sorted(list(set(datos['estrato'])))),
                                create_dropdown('select-tipo_inmueble','Tipo inmueble', ["Ninguno"]+sorted(list(set(datos['tipo_inmueble'])))),
                                html.Div(
                                    children = [
                                        html.Label('Área valorada', style={'font-size': 14, 'font-weight': '500'}),
                                        dmc.RangeSlider(
                                            id='slider-area_valorada',
                                            max = 500,
                                            value=[0, 500],
                                            mb=35,
                                        ),
                                    ]
                                ),
                                create_dropdown('select-garajes','Garajes', ["Ninguno"]+sorted(list(set(datos['numero_total_de_garajes'])))),
                            ]
                        )
                    ],                    
                ),
            ]
        ),
        dmc.Space(h=30),
        dmc.Divider(label = 'Exploratorio', labelPosition='center', size='xl', style={'width':'90%', 'align':'center'}),
        dmc.Paper(
            radius="md", # or p=10 for border-radius of 10px
            withBorder=True,
            shadow='xs',
            p='sm',
            style={'height':'100%', 'width':'90%', 'align':'center'},
            children=[
                dmc.SimpleGrid(
                    cols = 2,
                    children = [
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-1', figure=go.Figure(layout={'height': 10}))], type="default"),
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-2', figure=go.Figure(layout={'height': 10}))], type="default"),
                    ]
                )
            ],            
        ),                    
    ]
)
