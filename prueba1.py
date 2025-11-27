import argparse

parser = argparse.ArgumentParser()
parser.add_argument("a")
parser.add_argument("b")
parser.add_argument("operacion")

args = parser.parse_args()
variables = vars(args)
print(variables)
