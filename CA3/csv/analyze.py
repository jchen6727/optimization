import pandas

import argparse

import plotly.express as px

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--csv", type=str, help="csv file to analyze",)
parser.add_argument("-o", "--output", type=str, help="output file name",)
parser.add_argument("-f", "--filename", type=str, help="I & O filename", default=None)
#args, call= parser.parse_known_args()

args, call= parser.parse_known_args([ "--csv", "optuna_AMPA/optuna_15_500.csv", "--output",
                                      "optuna_AMPA/optuna_15_500_min.html"])

args= dict(args._get_kwargs())

if args.filename:
    args.csv = args.filename + '.csv'
    args.output = args.filename + '.html'

df = pandas.read_csv(args['csv'])

df['min'] = [df['loss'][0:i].min() for i in range(len(df))]

fig = px.line(
    df,
    x=df.index,
    y='min'
)

fig.write_html(args['output'])
