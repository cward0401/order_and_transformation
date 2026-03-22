# How does the system evolve?

# each row is one timestamp + 
# each column is one spatial position across time
# so- entropy/coherence become row-wise metrics

import numpy as np
from rules import modular_update

def run_simulation(state0, steps, a, b, m):
    n_cells = len(state0)
    field = np.zeros((steps, n_cells), dtype=int)
    field[0] = state0

    for t in range(steps - 1):
        field[t + 1] = modular_update(field[t], a, b, m)

    return field