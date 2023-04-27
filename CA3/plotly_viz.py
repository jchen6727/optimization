import pandas
import utils
import plotly.express as px
#import dash

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

fig.write_html("plotly3d.html")
