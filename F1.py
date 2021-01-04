import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv("data/cleaned.csv")
df2 = pd.read_csv("data/drivers.csv")
df3 = pd.read_csv("data/fastest_lap2020.csv")

# creating the app with flask and initialize bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

# create the app layout
# we use container
nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

app.layout = dbc.Container([
    # create Navbar
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(src="https://cdn.shopify.com/s/files/1/1095/6418/articles/DPkTCh9X0AIJKSx.jpg-large_1200x1200.jpeg?v=1511714320", height="40px")),
                            dbc.Col(dbc.NavbarBrand(
                                "Formula 1", className="ml-4")),
                        ],
                        align="center",
                        no_gutters=True,

                    ),
                    href="https://www.formula1.com/en.html",
                    target="_blank"


                ),

            ]
        ),
        color="dark",
        dark=True,
    ),

    html.Br(),

    # first row for the title
    dbc.Row([
        dbc.Col([
            html.H1(
                "F1 Dashboard",
                className='text-center text-danger mb-4 text-capitalize')
        ], width=12),
    ]),

    # second row
    dbc.Row([
        dbc.Col([
            html.H3(
                "F1 Constructors Standings 2016-2020",
                className='text-center text-danger mb-4 text-capitalize')
        ], width=12),
    ]),



    html.Br(),
    html.Br(),
    # third row
    dbc.Row([
        dbc.Col([
            # dropdown for single line graph
            dcc.Dropdown(id='my-dpdn', multi=False, value='Ferrari',
                         className='text-dark text-capitalize',
                         options=[
                             {'label': 'Ferrari', 'value': 'Ferrari'},
                             {'label': 'Mercedes', 'value': 'Mercedes'},
                            {'label': 'Renault', 'value': 'Renault'},
                             {'label': 'Red Bull Racing',
                                 'value': 'Red Bull Racing'},
                             {'label': 'Williams Mercedes',
                                 'value': 'Williams Mercedes'},
                             {'label': 'AlphaTauri Honda',
                                 'value': 'AlphaTauri Honda'},
                             {'label': 'Haas Ferrari', 'value': 'Haas Ferrari'},
                             {'label': 'McLaren', 'value': 'McLaren'},
                             # for x in sorted(df['Team'].unique())],
                         ]),
            html.Br(),

            # single line graph
            dcc.Graph(id='line-fig', figure={})

        ],
            xs=12, sm=12, md=12, lg=5, xl=5
        ),


        dbc.Col([
            # dropdown for mutiple line chart
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['Ferrari', 'Mercedes'],
                         className='text-dark text-capitalize',

                         options=[{'label': 'Ferrari', 'value': 'Ferrari'},
                                  {'label': 'Mercedes', 'value': 'Mercedes'},
                                  {'label': 'Renault', 'value': 'Renault'},
                                  {'label': 'Red Bull Racing',
                                   'value': 'Red Bull Racing'},
                                  {'label': 'Williams Mercedes',
                                   'value': 'Williams Mercedes'},
                                  {'label': 'AlphaTauri Honda',
                                   'value': 'AlphaTauri Honda'},
                                  {'label': 'Haas Ferrari',
                                      'value': 'Haas Ferrari'},
                                  {'label': 'McLaren', 'value': 'McLaren'},
                                  #  for x in sorted(df['Symbols'].unique())],

                                  ]),
            html.Br(),

            # mutiple line graph
            dcc.Graph(id='line-fig2', figure={})
        ],  # width={'size': 5},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ], justify='around'),

    html.Br(),
    html.Br(),
    html.Br(),


    dbc.Row([
        dbc.Col([
            html.H3(
                "F1 Driver Standings 2020",
                className='text-center text-danger mb-4 text-capitalize'),
            html.Br(),
            dcc.Dropdown(id='my-dpdn3', multi=False, value='Lewis Hamilton',
                         className='text-dark text-capitalize',

                         options=[{'label': x, 'value': x}
                                  for x in sorted(df2['Name'].unique())]),
            html.Br(),

            dcc.Graph(id='line-fig3', figure={}),

        ],
            xs=12, sm=12, md=12, lg=12, xl=12
        ),
    ]),

    html.Br(),
    html.Br(),


    # creating data table
    dbc.Row([
        dbc.Col([
            html.H3(
                "F1 Fastest Lap 2020",
                className='text-center text-danger mb-4 text-capitalize'),
            html.Br(),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df3.columns],
                data=df3.to_dict('records'),
                #className='text-dark text-capatalize'
                style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                style_cell={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white',
                },
            )
        ], xs=12, sm=12, md=12, lg=12, xl=12)
    ]),

    html.Br(),
        html.Br(),
        html.Br(),
])


# Line chart - Single
@ app.callback(
    dash.dependencies.Output('line-fig', 'figure'),
    [dash.dependencies. Input('my-dpdn', 'value')]
)
  

def update_graph(team_slctd):
    dff = df[df['Team'] == team_slctd]
    figln = px.bar(dff, x="Year", y="Position", color="Team", barmode="group")
    return figln


# Line chart - multiple
@ app.callback(
    dash.dependencies.Output('line-fig2', 'figure'),
    [dash.dependencies. Input('my-dpdn2', 'value')]

)
def update_graph(team_slctd):
    dff = df[df['Team'].isin(team_slctd)]
    figln2 = px.bar(dff, x="Year", y="Position", color="Team", barmode="group")
    return figln2


# Line graph - drivers
@ app.callback(
    dash.dependencies.Output('line-fig3', 'figure'),
    [dash.dependencies. Input('my-dpdn3', 'value')]
)
def update_graph(driver_slctd):
    dff = df2[df2['Name'].isin([driver_slctd])]
    figln3 = px.scatter(dff, x="Venue", y="Position")
    return figln3


if __name__ == '__main__':
    app.run_server(debug=True)
