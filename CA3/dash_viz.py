import pandas
import utils
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input

app = Dash(__name__)

df = pandas.read_csv("frequencies.csv")
df = df.drop(['Unnamed: 0'], axis=1).reset_index(drop=True)
df['MSE'] = df.apply(utils.mse, axis=1)

app.layout = html.Div([
    html.H1(children="Fitness (MSE)", style={'textAlign':'center'}),
    dcc.Slider(0.1, 2.5, 0.1,
               value=1.2,
               id='upper-bound'),
    dcc.Graph(id='graph', style={'width': '75vh', 'height': '75vh'}, animate=True)
])


@callback( Output('graph', 'figure'), Input('upper-bound', 'value') )
def update_figure(value):
    dff = df[df['MSE'] < value]
    fig = px.scatter_3d(dff,
                        x='netParams.connParams.PYR->BC_AMPA.weight',
                        y='netParams.connParams.PYR->OLM_AMPA.weight',
                        z='netParams.connParams.PYR->PYR_AMPA.weight',
                        color='MSE'
                        )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)