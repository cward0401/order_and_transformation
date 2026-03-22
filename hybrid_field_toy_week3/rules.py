
import numpy as np

def modular_update(state, a, b, m):
    left  = np.roll(state, 1)
    right = np.roll(state, -1)

    neighborhood = left + state + right
    next_state = (a * neighborhood + b) % m
    return next_state

