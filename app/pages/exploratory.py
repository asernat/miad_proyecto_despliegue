from dash import Input, Output, html, dcc
import dash_mantine_components as dmc
import pickle
from app import app
import plotly.graph_objects as go
import plotly.express as px

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

    fig1 = px.histogram(df_f, x="vigilancia_privada", color="vigilancia_privada", width=500, height=400, text_auto=True)
    fig1.update_layout(title_text="Vigilancia Privada", title_x=0.5)

    fig2 = px.histogram(df_f, x="calidad_acabados_cocina", color="calidad_acabados_cocina", width=500, height=400, text_auto=True)
    fig2.update_layout(title_text="Calidad acabados cocina", title_x=0.5)

    fig3 = px.histogram(df_f, x="clase_inmueble", color="clase_inmueble", width=500, height=400)
    fig3.update_layout(title_text="clase inmueble", title_x=0.5)

    fig4 = px.pie(df_f, names='administracion', title='Administración',width=500, height=400)
    fig4.update_layout(title_text="Administración", title_x=0.5)

    return df_f.shape[0], fig1, fig2, fig3,fig4

@app.callback([Output('select-ciudad', 'value'),Output('select-ciudad', 'data')],[Input('select-departamento', 'value')])
def update_output_div(input_value):
    
    if input_value == 'Ninguno':
        ciudades = ['Ninguno'] + sorted(list(set(datos['municipio_inmueble'])))
        return "Ninguno", ciudades
    else:
        f_datos = datos.query(f"departamento_inmueble == '{input_value}'")
        ciudades = ['Ninguno'] + sorted(list(set(f_datos['municipio_inmueble'])))
        return "Ninguno", ciudades
    