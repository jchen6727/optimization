import pandas
import utils
import plotly.express as px
#import plotly
#import plotly.graph_objs as go
from dash import Dash, html, dcc, callback, Output, Input

app = Dash(__name__)

df = pandas.read_csv("GABAf.csv")
#df = df.drop(['Unnamed: 0'], axis=1).reset_index(drop=True)
df['MSE'] = df.apply(utils.mse, axis=1)

app.layout = html.Div([
    html.H1(children="Fitness (MSE)", style={'textAlign':'center'}),
    dcc.Slider(0.1, 10, 5,
               value=10,
               id='upper-bound'),
    dcc.Graph(id='graph', style={'height': '75vh'})
])


@callback( Output('graph', 'figure'), Input('upper-bound', 'value') )
def update_figure(value):
    dff = df[df['MSE'] < value]
    fig = px.scatter_3d(dff,
                        x='netParams.connParams.BC->BC_GABA.weight',
                        y='netParams.connParams.BC->PYR_GABA.weight',
                        z='netParams.connParams.OLM->PYR_GABA.weight',
                        color='MSE',
                        #range_x=[4.5e-4, 4.5e-2],
                        #range_y=[0.72e-4, 0.72e-2],
                        #range_z=[72e-4, 72e-2]
                        )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)