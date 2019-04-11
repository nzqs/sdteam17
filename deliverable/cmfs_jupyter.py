import pandas as pd
from collections import Counter, namedtuple
# from gooey import Gooey, GooeyParser
from argparse import ArgumentParser

def cmfs(args):
    Key = namedtuple('Key', ['Machine', 'Material', 'Estimate'])
    Probabilities = namedtuple('Probabilities', ['Probability', 'Cumulative'])

    df = pd.read_excel(args.CMF_Input, sheet_name = args.sheet)
    print(df)
    subset = [args.mat_col, args.mach_col, args.estim_col, args.actual_col]
    df = df.dropna(subset = subset)
    df = df[df[args.actual_col] != 0]
    machines = df[args.mach_col].unique()
    keys = []
    for machine in machines:
        df1 = df[df[args.mach_col] == machine]
        for mat in df1[args.mat_col].unique():
            df2 = df1[df1[args.mat_col] == mat]
            for est in df2[args.estim_col].unique():
                keys.append(Key(machine, mat, est))
    del df1, df2

    cmfs = dict()
    for key in keys:
        data = df[(df[args.mach_col] == key[0]) & (df[args.mat_col] == key[1]) & (df[args.estim_col] == key[2])]
        counts = Counter(data[args.actual_col])
        total = sum(counts.values())
        cumulated = 0
        lengths = sorted(list(counts.keys()))
        for length in lengths:
            freq = counts[length] / total
            cumulated += freq
            counts[length] = Probabilities(freq, round(cumulated, 5))
        cmfs[key] = dict(counts)
    return cmfs

def p_star(cmf, theta, delta):
    # cmf = {Time1: Probabilities(Probability, Cumulative), Time2: ... }
    fractile = delta / (theta + delta)
    for key in sorted(cmf.keys()):
        if cmf[key].Cumulative >= fractile:
            return key
        else:
            pass
