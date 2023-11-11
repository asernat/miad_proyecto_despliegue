from dash import Input, Output, html, dcc
import dash_mantine_components as dmc
import pickle
from app import app
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State

def create_dropdown(id, label, options_list):
    return dmc.Select(
        id=id,
        label=label,
        data=[{'value': i, 'label': i} for i in options_list],
        value=options_list[0]
    )

datos = pickle.load(open("../datos/datos_tablero.pkl", "rb"))

layout = html.Div(
    style={'margin-top': '70px', 'background-color': 'WhiteSmoke', 'width': '100%', 'height': '100%',
           'align': 'center', 'display': 'inline'},
    children=[
        dmc.Text('Este sitio le permite obtener el precio justo de vivienda para compra o venta en Colombia relacionada '
                 'a sus preferencias', style={'font-family': 'Arial', 'fontSize': 12, 'font-weight': 'bold',
                                              'width': '100%', 'height': '100%'}, align='center'),
        dmc.Space(h=30),
        dmc.Group(
            align='center',
            position='center',
            children=[
                dmc.Paper(
                    radius="md",  # or p=10 for border-radius of 10px
                    withBorder=True,
                    shadow='xs',
                    p='sm',
                    style={'height': '155px', 'width': '300px', 'align': 'center'},
                    children=[
                        dmc.Text('Total inmuebles', color='black',
                                 style={'font-family': 'Arial', 'font-size': 14, 'font-weight': 'bold'}, align='center'),
                        html.Div(
                            style={'background-color': 'WhiteSmoke', 'border-color': 'black', 'border': '1px solid black'},
                            children=[
                                dmc.Text(datos.shape[0], id='total_inmuebles', color='black',
                                         style={'font-family': 'Arial', 'font-size': 50, 'font-weight': 'bold'},
                                         align='center'),
                            ]
                        )
                    ],
                ),
                dmc.Paper(
                    radius="md",  # or p=10 for border-radius of 10px
                    withBorder=True,
                    shadow='xs',
                    p='sm',
                    style={'height': '200px'},
                    children=[
                        dmc.Text('Seleccione el filtro', color='black',
                                 style={'font-family': 'Arial', 'font-size': 14, 'font-weight': 'bold'},
                                 align='center'),
                        dmc.SimpleGrid(
                            cols=3,
                            children=[
                                create_dropdown('select-departamento', 'Departamento',
                                                 ["Ninguno"] + sorted(list(set(datos['departamento_inmueble'])))),
                                create_dropdown('select-ciudad', 'Ciudad',
                                                 ["Ninguno"] + sorted(list(set(datos['municipio_inmueble'])))),
                                create_dropdown('select-estrato', 'Estrato',
                                                 ["Ninguno"] + sorted(list(set(datos['estrato'])))),
                                create_dropdown('select-tipo_inmueble', 'Tipo inmueble',
                                                 ["Ninguno"] + sorted(list(set(datos['tipo_inmueble'])))),
                                html.Div(
                                    children=[
                                        html.Label('Área valorada', style={'font-size': 14, 'font-weight': '500'}),
                                        dmc.RangeSlider(
                                            id='slider-area_valorada',
                                            max=500,
                                            value=[0, 500],
                                            mb=35,
                                        ),
                                    ]
                                ),
                                create_dropdown('select-garajes', 'Garajes',
                                                 ["Ninguno"] + sorted(list(set(datos['numero_total_de_garajes'])))),
                            ]
                        )
                    ],
                ),

                html.Div([
                    html.Label("Seleccionar variable(s) de análisis:"),
                    dcc.Dropdown(
                        id='dropdown-variables-analysis',
                        options=[
                            {'label': col, 'value': col} for col in
                            ['estrato', 'demanda_interes', 'nivel_equipamiento_comercial', 'estado_acabados_pisos',
                             'calidad_acabados_pisos', 'calidad_acabados_muros', 'calidad_acabados_techos',
                             'estado_acabados_madera', 'calidad_acabados_madera', 'calidad_acabados_metal',
                             'calidad_acabados_banos', 'estado_acabados_cocina', 'calidad_acabados_cocina',
                             'tipo_garaje']
                        ],
                        multi=True,
                        value=['estrato']  # Variables por defecto
                    ), dcc.Store(id='selected-variables-store', data=['estrato'])
                ], style={'margin-top': '20px'}),


            ]
        ),
        dmc.Space(h=30),
        dmc.Divider(label='Exploratorio', labelPosition='center', size='xl', style={'width': '100%', 'align': 'center'}),
        dmc.Paper(
            radius="md",  # or p=10 for border-radius of 10px
            withBorder=True,
            shadow='xs',
            p='sm',
            style={'height': '100%', 'width': '100%', 'align': 'center'},
            children=[
                dmc.SimpleGrid(
                    style={'width': '100%', 'align': 'center'},
                    cols=2,
                    children=[
                        dcc.Loading(id="loading-icon-1",
                                    children=[dcc.Graph(id='graph-1', figure=go.Figure(layout={'height': 10}))],
                                    type="default"),
                        dcc.Loading(id="loading-icon-2",
                                    children=[dcc.Graph(id='graph-2', figure=go.Figure(layout={'height': 10}))],
                                    type="default"),
                        dcc.Loading(id="loading-icon-3",
                                    children=[dcc.Graph(id='graph-3', figure=go.Figure(layout={'height': 10}))],
                                    type="default"),
                        dcc.Loading(id="loading-icon-4",
                                    children=[dcc.Graph(id='graph-4', figure=go.Figure(layout={'height': 10}))],
                                    type="default"),
                        dcc.Loading(id="loading-icon-5",
                                    children=[dcc.Graph(id='graph-5', figure=go.Figure(layout={'height': 10}))],
                                    type="default"),
                        dcc.Loading(id="loading-icon-6",
                                    children=[dcc.Graph(id='graph-6', figure=go.Figure(layout={'height': 10}))],
                                    type="default"),
                    ]
                )
            ],
        ),
    ]
)


@app.callback(
    [Output('total_inmuebles', 'children'),
     Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-3', 'figure'),
     Output('graph-4', 'figure')
     ],
    [Input('select-departamento', 'value'),
     Input('select-ciudad', 'value'),
     Input('select-estrato', 'value'),
     Input('select-tipo_inmueble', 'value'),
     Input('slider-area_valorada', 'value'),
     Input('select-garajes', 'value'),
     Input('dropdown-variables-analysis', 'value'),
     Input('selected-variables-store', 'data')]
)
def update_dashboard(departamento, ciudad, estrato, tipo_inmueble, area_valorada, garajes, variables_analysis, selected_variables):
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

    


    for variable in variables_analysis:
        graphs = []
        if variable in df_f.columns:
            
            # Precio Promedio Avaluo 
            fig1 = px.histogram(df_f, x=variable, y='clean_valor_total_avaluo', color=variable, histfunc='avg', width=500, height=400, text_auto=True)
            fig1.update_layout(title=f'{variable} vs Valor Medio Avalúo', title_x=0.5)
            fig1.update_xaxes(title=variable)
            fig1.update_yaxes(title='Valor Medio Avalúo')
            graphs.append(fig1)

            # Precio Minimo Avaluo
            fig2 = px.histogram(df_f, x=variable, y='clean_valor_total_avaluo', color=variable, histfunc='max', width=500, height=400, text_auto=True)
            fig2.update_layout(title=f'{variable} vs Valor Máximo Avalúo', title_x=0.5)
            fig2.update_xaxes(title=variable)
            fig2.update_yaxes(title='Valor Máximo Avalúo')
            graphs.append(fig2)

            # Pie proporcio Variable 
            fig3 = px.pie(df_f, names=variable, title=variable,width=500, height=400)
            fig3.update_layout(title_text=f"Proporción Inmubles X {variable}", title_x=0.5)
            graphs.append(fig3)

            # Valor Avaluo vs Área Valorada
            fig5 = px.scatter(df_f,  y='clean_valor_total_avaluo', x=variable, color='vigilancia_privada',  width=500, height=400)
            fig5.update_xaxes(title=variable)
            fig5.update_yaxes(title='Valor Total Avalúo')
            fig5.update_layout(title=f'Valor Total Avalúo vs {variable}', title_x=0.5)
            graphs.append(fig5)

    return df_f.shape[0], *graphs


@app.callback([Output('select-ciudad', 'value'), Output('select-ciudad', 'data'),
               Output('selected-variables-store', 'data')],
              [Input('select-departamento', 'value'), Input('dropdown-variables-analysis', 'value')])
def update_output_div(input_value, selected_variables):
    if input_value == 'Ninguno':
        ciudades = ['Ninguno'] + sorted(list(set(datos['municipio_inmueble'])))
        return "Ninguno", ciudades, selected_variables
    else:
        f_datos = datos.query(f"departamento_inmueble == '{input_value}'")
        ciudades = ['Ninguno'] + sorted(list(set(f_datos['municipio_inmueble'])))
        return "Ninguno", ciudades, selected_variables


if __name__ == '__main__':
    app.run_server(debug=True)
