import dash
from dash import Input, Output, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px

app = dash.Dash(__name__, suppress_callback_exceptions = True, 
    title = 'Predicción del precio de vivienda en Colombia', 
    #update_title=None, 
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    
)
server = app.server

import pages

global_values = {}


@app.callback([
    Output('total_inmuebles','children'),
    Output('graph-1','figure'),
    Output('graph-2','figure'),
    ],[
    Input('select-departamento', 'value'),
    Input('select-ciudad', 'value'),
    Input('select-estrato', 'value'),
    Input('select-tipo_inmueble', 'value'),
    Input('slider-area_valorada', 'value'),
    Input('select-garajes', 'value'),
    ])
def update_dashbord(departamento, ciudad, estrato, tipo_inmueble, area_valorada, garajes):
    df_f = pages.exploratory.datos.copy()

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

    return df_f.shape[0], fig1, fig2

@app.callback([Output('select-ciudad', 'value'),Output('select-ciudad', 'data')],[Input('select-departamento', 'value')])
def update_output_div(input_value):
    
    if input_value == 'Ninguno':
        ciudades = ['Ninguno'] + sorted(list(set(pages.exploratory.datos['municipio_inmueble'])))
        return "Ninguno", ciudades
    else:
        f_datos = pages.exploratory.datos.query(f"departamento_inmueble == '{input_value}'")
        ciudades = ['Ninguno'] + sorted(list(set(f_datos['municipio_inmueble'])))
        return "Ninguno", ciudades


def create_main_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            align='row',
            position='center',
            spacing=10,
            style={'margin-bottom':5},
            children=[
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=25,
                    radius=5,
                    color='gray',
                    variant="filled",
                    style={'margin-left':10}
                ),
                dmc.Text(label, size="sm", color="black", style={'font-family':'Arial'}),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )

app.layout = dmc.MantineProvider(
    id = 'dark-moder', 
    withGlobalStyles=True, 
    children = [        
        html.Div(
            children = [
                dmc.Header(
                    height=80,
                    fixed=True,
                    pl=0,
                    pr=0,
                    pt=0,
                    style = {'background-color':'lightgray', 'color':'black'},
                    children=[
                        dmc.Container(
                            fluid=True,
                            children=[
                                dmc.Group(
                                    position="center",
                                    align="center",
                                    children=[
                                        dmc.Group(
                                            position="center",
                                            align="center",
                                            spacing="md",
                                            style = {'background-color':'white', 'margin-top':7, 'width':950},
                                            children=[                                                                                                                                                
                                                DashIconify(icon ='cil:house', color='black', width=50, height=50),                                                 
                                                html.Div(
                                                    children=[
                                                        dmc.Text('Comprar o vender una vivienda en Colombia', style = {'font-family':'Arial', 'fontSize':40}, size = 'lg', weight=700)                                                        
                                                    ]
                                                )
                                            ],
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
    
                dmc.Navbar(
                    fixed=True,
                    width={"base": 270},

                    hidden=True,
                    hiddenBreakpoint='sm',
                    style = {'background-color':'white'},
                    children=[
                        dmc.ScrollArea(
                            offsetScrollbars=True,
                            type="scroll",
                            children=[
                                dmc.Divider(style={"marginBottom": 20, "marginTop": 20}),
                                dmc.Group(
                                    children=[
                                        create_main_nav_link(
                                            icon="cil:house",
                                            label="EXPLORATORIO VIVIENDAS",
                                            href=app.get_relative_path("/"),
                                        ),
                                        create_main_nav_link(
                                            icon="carbon:machine-learning-model",
                                            label="PREDICCIÓN PRECIO",
                                            href=app.get_relative_path("/predict"),
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                ),

                dcc.Location(id='url'),

                html.Div(
                    id='content',
                    style={'margin-top':'90px', 'margin-left':'300px', 'height':'100%'}
                ),
            ]
        )
    ]
)


@app.callback(Output('content', 'children'),[Input('url', 'pathname')])
def display_content(pathname):
    page_name = app.strip_relative_path(pathname)
    if not page_name:  # None or ''
        return pages.exploratory.layout
    elif page_name == 'predict':
        return pages.predict.layout

if __name__ == '__main__':
    app.run_server(debug=True)

