def file_to_list(self, f):
    with open(f) as l:
        return l.read().splitlines()

def print_full(self, x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
