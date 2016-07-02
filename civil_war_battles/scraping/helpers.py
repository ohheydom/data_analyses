import pandas as pd

def file_to_list(f):
    with open(f) as l:
        return l.read().splitlines()

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
