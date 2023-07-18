import pandas
import utils
import plotly.express as px
#import plotly
#import plotly.graph_objs as go
from dash import Dash, html, dcc, callback, Output, Input
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', default="NMDAf.csv")

args, call= parser.parse_known_args()
args= dict(args._get_kwargs())

app = Dash(__name__)

df = pandas.read_csv(args['filename'])

#get synaptic weight parameters
x, y, z = [key for key in df.keys() if '->' in key]

range_x = [df[x].min(), df[x].max()]
range_y = [df[y].min(), df[y].max()]
range_z = [df[z].min(), df[z].max()]

#df = df.drop(['Unnamed: 0'], axis=1).reset_index(drop=True)
df['MSE'] = df.apply(utils.mse, axis=1, target=utils.target)


app.layout = html.Div([
    html.H1(children="Fitness (MSE)", style={'textAlign':'center'}),
    dcc.Slider(0.1, 2.5, 0.1,
               value=1.3,
               id='upper-bound'),
    dcc.Graph(id='graph', style={'height': '75vh'})
])


@callback( Output('graph', 'figure'), Input('upper-bound', 'value') )
def update_figure(value):
    dff = df[df['MSE'] < value]
    fig = px.scatter_3d(dff,
                        x=x,
                        y=y,
                        z=z,
                        color='MSE',
                        range_x=range_x,
                        range_y=range_y,
                        range_z=range_z,
                        )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)