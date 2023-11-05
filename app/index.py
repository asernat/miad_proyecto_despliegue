import dash
from dash import Input, Output, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from app import app
import pages

server = app.server

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

