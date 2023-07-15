from numpy import around as np_round


def rd(value, decs=12):
    """Round a value to a given number of decimals."""
    return np_round(value, decs)
