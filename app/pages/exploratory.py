from dash import Input, Output, html, dcc
import dash_mantine_components as dmc
import pickle
from app import app
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def create_dropdown(id,label, options_list):
    return dmc.Select(
        id = id,
        label = label,
        data = [{'value':i, 'label': i} for i in options_list],
        value = options_list[0]
    )

datos = pickle.load(open("datos/datos_tablero.pkl","rb"))

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
        dmc.Divider(label = 'Exploratorio', labelPosition='center', size='xl', style={'width':'100%', 'align':'center'}),
        dmc.Paper(
            radius="md", # or p=10 for border-radius of 10px
            withBorder=True,
            shadow='xs',
            p='sm',
            style={'height':'100%', 'width':'100%', 'align':'center'},
            children=[
                dmc.SimpleGrid(
                    style={'width':'100%', 'align':'center'},
                    cols = 2,
                    children = [
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-1', figure=go.Figure(layout={'height': 10}))], type="default"),
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-2', figure=go.Figure(layout={'height': 10}))], type="default"),
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-3', figure=go.Figure(layout={'height': 10}))], type="default"),
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-4', figure=go.Figure(layout={'height': 10}))], type="default"),                        
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-5', figure=go.Figure(layout={'height': 10}))], type="default"),  
                        dcc.Loading(id = "loading-icon", children=[dcc.Graph(id='graph-6', figure=go.Figure(layout={'height': 10}))], type="default"),  
                    ]
                )
            ],            
        ),                    
    ]
)


@app.callback([
    Output('total_inmuebles','children'),
    Output('graph-1','figure'),
    Output('graph-2','figure'),
    Output('graph-3','figure'),
    Output('graph-4','figure'),
    Output('graph-5','figure'),
    Output('graph-6','figure'),
    ],[
    Input('select-departamento', 'value'),
    Input('select-ciudad', 'value'),
    Input('select-estrato', 'value'),
    Input('select-tipo_inmueble', 'value'),
    Input('slider-area_valorada', 'value'),
    Input('select-garajes', 'value'),
    ])
def update_dashbord(departamento, ciudad, estrato, tipo_inmueble, area_valorada, garajes):
    df_f = datos.copy()

    if departamento != "Ninguno":
        df_f = df_f.query(f"departamento_inmueble == '{departamento}'")

    if ciudad != "Ninguno":
        df_f = df_f.query(f"municipio_inmueble == '{ciudad}'")

    if estrato != "Ninguno":
        df_f = df_f.query(f"estrato == {estrato}")

    if tipo_inmueble != "Ninguno":
        df_f = df_f.query(f"tipo_inmueble == '{tipo_inmueble}'")

    if garajes != "Ninguno":
        df_f = df_f.query(f"numero_total_de_garajes == {garajes}")

    if area_valorada[1] == 500:
        df_f = df_f.query(f"area_valorada >= {area_valorada[0]}")
    else:
        df_f = df_f.query(f"area_valorada >= {area_valorada[0]} and area_valorada <= {area_valorada[1]}")

    #Proporción de clases de inmuebles
    fig1 = px.pie(df_f, names='clase_inmueble', width=500, height=400)
    fig1.update_layout(title_text="Proporción de Clases de Inmuebles", title_x=0.5)

    #Distribución de estratos 
    fig2 = px.histogram(df_f, x="estrato", color="estrato", width=500, height=400)
    fig2.update_layout(title_text="Distribución de Estratos", title_x=0.5)
    fig2.update_xaxes(title='Estratos')
    fig2.update_yaxes(title='Cantidad')


    # Relación Habitaciones, Baño y Valor del Avaluo
    fig3 = px.scatter(df_f, x='habitaciones', y='bano_privado', size='clean_valor_total_avaluo', width=500, height=400)
    fig3.update_xaxes(title='Habitaciones')
    fig3.update_yaxes(title='Baño Privado')
    fig3.update_layout(title_text="Relación entre Habitaciones, Baños y Valor Total del Avalúo", title_x=0.5)


    # Box Avaluo Estrato
    fig4 = px.box(df_f, x='estrato', y='clean_valor_total_avaluo', color='estrato', width=500, height=400)
    fig4.update_xaxes(title='Estrato')
    fig4.update_yaxes(title='Valor Total Avalúo')
    fig4.update_layout(title_text="Box Plot de Valor Total de Avalúo por Estrato", title_x=0.5)
    

    ## Valor Avaluo vs Área Valorada
    fig5 = px.scatter(df_f,  y='clean_valor_total_avaluo', x='area_valorada',  width=500, height=400)
    fig5.update_xaxes(title='Estrato')
    fig5.update_yaxes(title='Valor Total Avalúo')
    fig5.update_layout(title='Valor Total Avalúo vs Área Valorada', title_x=0.5)
    fig5.update_traces(marker=dict(color='blue', size=8, line=dict(color='black', width=2)))


    #Radar Calida Acabados y Rangos de Precios 
    # Definir los rangos de valores
    rangos_valor = [0, 150000000, 300000000, 450000000, 600000000, np.inf]
    df_f['rango_valor'] = pd.cut(df_f['clean_valor_total_avaluo'], bins=rangos_valor)

    ## Precio Promedio Por Estrato
    fig6 = go.Figure(data=[
        go.Scatterpolar(
            r=df_f[df_f['rango_valor'] == rango][['calidad_acabados_pisos', 'calidad_acabados_muros',
                                                      'calidad_acabados_techos', 'calidad_acabados_madera',
                                                      'calidad_acabados_metal', 'calidad_acabados_banos',
                                                      'calidad_acabados_cocina']].mean(),
            theta=['Pisos', 'Muros', 'Techos', 'Madera', 'Metal', 'Baños', 'Cocina'],
            fill='toself',
            name=str(rango)
        ) for rango in df_f['rango_valor'].unique()
    ],
    layout=go.Layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title='Calidad de Acabados por Rango de Valor de Inmueble',
        width=500,
        height=400
    ))

    

    return df_f.shape[0], fig1, fig2, fig3,fig4, fig5, fig6

@app.callback([Output('select-ciudad', 'value'),Output('select-ciudad', 'data')],[Input('select-departamento', 'value')])
def update_output_div(input_value):
    
    if input_value == 'Ninguno':
        ciudades = ['Ninguno'] + sorted(list(set(datos['municipio_inmueble'])))
        return "Ninguno", ciudades
    else:
        f_datos = datos.query(f"departamento_inmueble == '{input_value}'")
        ciudades = ['Ninguno'] + sorted(list(set(f_datos['municipio_inmueble'])))
        return "Ninguno", ciudades

	
	
	