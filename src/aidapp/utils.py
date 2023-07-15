from numpy import around as np_round


def rd(value, decs=12):
    return np_round(value, decs)
