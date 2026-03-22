# What does the system do?

import numpy as np
import zlib

def row_entropy(row, m):
    #this counts how many times each state appears in the row
    # minlength=m forces solots for 0, 1, ..., m-1 so the length correct
    counts = np.bincount(row, minlength=m)

    # converting counts into probabilities 
    probs = counts / counts.sum()

    # cleanup step: so we don't take log2(0)
    probs = probs[probs > 0]

    # entropy
    return -(probs * np.log2(probs)).sum()


def field_entropy(field, m):
    return np.array([row_entropy(row, m) for row in field])


def row_coherence(row, m):
    
    # first let's compare each cell to its left neighbor
    # and measure local variation
    diffs = np.abs(row - np.roll(row, 1))

    # now let's average 'difference'
    # and normalize to the max possile difference
    norm = diffs.mean() / (m - 1)

    return 1 - norm
    # small diffs: coherence near 1
    # big diffs:   coherence near 0


def field_coherence(field, m):
    return np.array([row_coherence(row, m) for row in field])


## We need a way to compare one row to an earlier row
# This func compares two whole rows and,
# returns 1 is v similar and lower if the diff more
def row_similarity(row1, row2, m):
    diff = np.abs(row1 - row2).mean()
    return 1 - diff / (m - 1)


# For each time, t, compare that to earlier rows
# output is: closure[t] = how much current state resembles something in the past
def closure_index(field, m, max_lag=50):
    T = len(field)
    out = np.zeros(T)

    for t in range(1,T):
        best = 0
        max_back = min(max_lag, t)

        for lag in range(1, min(max_lag, t) + 1):
            sim = row_similarity(field[t], field[t-lag], m)
            if sim > best:
                best = sim

            out[t] = best
        
        return out

def closure_spectrum(field, m, max_lag=50):
    T = len(field)
    spec = np.full((T, max_lag), np.nan)

    for t in range(1, T):
        max_back = min(max_lag, t)
        for lag in range(1, max_back + 1):
            spec[t, lag - 1] = row_similarity(field[t], field[t - lag], m)

    return spec

# Extracting the dominant lag

def best_lag(field, m, max_lag=50):
    T = len(field)
    best = np.zeros(T)

    for t in range(1, T):
        max_back = min(max_lag, t)

        sims = [
            row_similarity(field[t], field[t - lag], m)
            for lag in range(1, max_back + 1)
        ]

        best[t] = np.argmax(sims) + 1 # +1 bc lag starts at 1

    return best

# at each time, t, find the pasy row ost similar to field[t]
# take that lag and compare to the actual next row t+1
def reconstruction_coherence(field, m, max_lag=50):
    T = len(field)
    out = np.full(T, np.nan)

    for t in range(1, T - 1):
        max_back = min(max_lag, t)

        sims = [
            row_similarity(field[t], field[t - lag], m)
            for lag in range(1, max_back + 1)
        ]

        best_lag = np.argmax(sims) + 1

        out[t] = row_similarity(field[t + 1], field[t + 1 - best_lag], m)

    return out


def compression_ratio(row):
    raw = row.astype(np.uint8).tobytes()
    compressed = zlib.compress(raw)
    return len(compressed) / len(raw)

def field_compression(field):
    return np.array([compression_ratio(row) for row in field])