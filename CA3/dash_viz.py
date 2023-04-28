import pandas
import utils
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children="Fitness (MSE)", style={'textAlign':'center'}),
    dcc.Slider(0, 50, 5,
               value=25,
               id='UB'),
    html.Div(id='plot')
])

@app.callback(




)
def filter_MSE(df: pandas.DataFrame, ub):
    return df[(self. < ub)]

filenames = ["batch_csv/out{}.csv".format(i) for i in range(11)]

df = pandas.concat(
    [pandas.read_csv(filename) for filename in filenames]
)
df = df.drop(['Unnamed: 0'], axis=1).reset_index(drop=True)

df['MSE'] = df.apply(utils.mse, axis=1)

fig = px.scatter_3d(df,
                    x='netParams.connParams.PYR->BC_AMPA.weight',
                    y='netParams.connParams.PYR->OLM_AMPA.weight',
                    z='netParams.connParams.PYR->PYR_AMPA.weight',
                    color='MSE'
                    )
