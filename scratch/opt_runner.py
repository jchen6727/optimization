from avatk.runtk.runners import runner
import pandas
import numpy

optuna_runner = runner()
inputs = pandas.Series(optuna_runner.mappings)
results = numpy.square(inputs) - numpy.average(inputs)

print("{}DELIM{}".format(inputs.to_json(), results.to_json))
