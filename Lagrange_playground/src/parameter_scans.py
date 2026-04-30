from __future__ import annotations

from itertools import product
import numpy as np
import pandas as pd

from .fields import evolve_field
from .entropy import global_entropy
from .recurrence import recurrence_matrix, recurrence_density
from .coherence import structural_persistence

"""
"But someplace in the scheme of things 
this world must touch the other."

- Cormac McCarthy, Blood Meridian


Parameter Scans
===============

This module treats model parameters as terrain.

Rather than asking what a single rule does, it scans across parameter space 
and records how the system behaves under each local law. The result is a map:
a surface of entropy, recurrence, persistenv, or other diagnostics over field 
of possible transformations.

A parameter scans is a way of turning rule variation into landscape. 

"""

def _evaluate_rule_point(                                           # Evaluates one parameter coordinate, computes diagnostics
        initial_field: np.ndarray,                                  # and returns one result row as a dictionary
        a: float,
        b: float,
        steps: int,
        recurrence_epsilon: float,
)-> dict[str, float]:
    history = evolve_field(                                         # runs the field evolution
        initial_field,                                              # forced NumPy scalar values ino regular Python floats
        steps=steps,                                                # which avoids the linspace value shenanigans.
        a=float(a),
        b=float(b),
    )

    final_field = history[-1]                                       # gets the last item -> the field after all evolution steps

    entropy = global_entropy(final_field, bins=24)

    R, _ = recurrence_matrix(                                       # This builds the recurrence marix for the whole history
        history,                                                    # R is the binary matrix, _ ignores the distance matric
        epsilon=recurrence_epsilon,
    )
    recurrence = recurrence_density(R)                              # compresses the recureence matrix into one scalar
                                                                    # it is a fraction of recurrent state pairs
    persistence = np.nanmean(structural_persistence(history))       # computes frame-to-frame persistence, then averages it
                                                                    # we return a series taking the mean and ignoring NaN vals
    return {
        "a": float(a),                                              # This returns one tidy row as a dictionary where each key becomes a
        "b": float(b),                                              # Dataframe column later, and this is why Python is king.
        "final_entropy": float(entropy),                            # And Numpy, his civil service agent.
        "recurrence_density": float(recurrence),
        "mean_persistence": float(persistence)
    }


def scan_rule_surface(                                              # Scans all (a,b) parameter combinations and returns a DF of diagnostics
        initial_field: np.ndarray,                                  # by calling an inner-scoped list comprehension 
        a_values: np.ndarray,                                       # that says, try every a with every b and for each pair 
        b_values: np.ndarray,                                       # evaluate rule point returns a dictionary so the rows become
        steps: int = 60,                                            # [{"a":..., "b":..., "final_entropy":...}, ..]
        recurrence_epsilon: float = 0.14,                           # and finally we return the list of dictionares as a pandas DataFrame
)-> pd.DataFrame:                                                   # tables are shapes to work with
    rows = [
        _evaluate_rule_point(
            initial_field=initial_field,
            a=float(a),
            b=float(b),
            steps=steps,
            recurrence_epsilon=recurrence_epsilon,
        )
        for a, b in product(a_values, b_values)
    ]
    return pd.DataFrame(rows)

def dataframe_to_surface(                                           # Here we are taking our Darafame and converting it into X, Y, Z arrays 
        df: pd.DataFrame,                                           # for a 3D surface plot and out we get 
        x_col: str,                                                 # X = grid of a vals, Y = grid of b vals, Z = metric values at each a/b 
        y_col: str,                                                 # then we sort into columns of unique values
        z_col: str,                                                 # !Important: pivot-table reshapes tindiess into a matrix 
):                                                                  # in which the rows are the y vals and columns are the x values
    x_vals = np.sort(df[x_col].unique())                            # and the cells are recurrence_density
    y_vals = np.sort(df[y_col].unique())

    surface = (
        df.pivot_table(
            index=y_col,
            columns=x_col,
            values=z_col,
            aggfunc="first",                                        # there shouldn't be dupes by now but pandas reqs an agg rule
        )
        .reindex(index=y_vals, columns=x_vals)                      # this forced the row/column order to match the sorted values
    )                                                               # keeping surface gemetry stable

    X, Y = np.meshgrid(x_vals, y_vals)                              # creates coordinate grids
    Z = surface.to_numpy(dtype=float)                               # turns pivot table into a Numpy Matrix- the height/elev surface

    return X, Y, Z
