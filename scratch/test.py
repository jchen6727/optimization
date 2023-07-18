import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--concurrency', default=1)
parser.add_argument('-t', '--trials', default=5)
parser.add_argument('-j', '--json', default={})
#parser.add_argument('-python')
args, call= parser.parse_known_args()
args = dict(args._get_kwargs())
print(args)

