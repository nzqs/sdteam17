import pandas as pd
from collections import Counter, namedtuple
# from gooey import Gooey, GooeyParser
from argparse import ArgumentParser
import dill

def cmfs(args):
    Key = namedtuple('Key', ['Machine', 'Material', 'Estimate', 'Mean'])
    Probabilities = namedtuple('Probabilities', ['Probability', 'Cumulative'])

    df = pd.read_excel(args.CMF_Input, sheet_name = args.sheet)
    subset = [args.mat_col, args.mach_col, args.estim_col, args.actual_col]
    df = df.dropna(subset = subset)
    df = df[df[args.actual_col] != 0]
    keys = []
    machines = df[args.mach_col].unique()
    for machine in machines:
        df1 = df[df[args.mach_col] == machine]
        for mat in df1[args.mat_col].unique():
            df2 = df1[df1[args.mat_col] == mat]
            for est in df2[args.estim_col].unique():
                mean = df[(df[args.mach_col] == machine) & (df[args.estim_col] == est) & (df[args.mat_col] == mat)]['Actual Run Time'].mean()
                keys.append(Key(machine, mat, est, mean))
    del df1, df2
    # df3 = df.groupby(['Mach #', 'Material Description', 'Estim. Run Time']).mean()['Actual Run Time']

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

def p_star(cmf, mean, theta, delta):
    # cmf = {Time1: Probabilities(Probability, Cumulative), Time2: ... }
    # delta = delta/(72 - 36 - mean) # Deprecated
    fractile = delta / (theta + delta)
    # print(fractile)
    for key in sorted(cmf.keys()):
        if cmf[key].Cumulative >= fractile:
            return key
        else:
            # print(cmf[key])
            pass

def save_cmfs(args):
    monty = cmfs(args)
    with open('cmfs.pickle', 'rb') as read:
        pickled_cmfs =dill.load(read)
    for key in monty.keys():
        pickled_cmfs[key] = monty[key]
    with open('cmfs.pickle', 'wb') as save:
        dill.dump(pickled_cmfs, save)
