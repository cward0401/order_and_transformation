from __future__ import annotations

from pathlib import Path
from typing import Iterable
import numpy as np

"""
"The sun was just down and to the west lay reefs of bloodred clouds
up out of which rose little desert nighthawks like fugutives from 
some great fire at the earth's end."

- Cormac McCarthy, Blood Meridian


Utilities
=========

This module holds the small structural tools that keep the rest of the codebase
clean: output paths, scaling functions, vector normaliztion, rolling windows— 
albeit the kind of window which roll here are not highly recommended by Numpy,
and simle export helpers.

These functions are not the central objects of study. They are the instruments,
measuring rods, hinges, clamps, and quiet servants that allow the larger field
machinery to move without clutter.

"""



def ensure_output_dirs(base: str = "outputs") -> dict[str, Path]:
    base_path = Path(base)
    figures = base_path / "figures"
    html    = base_path / "html"
    tables  = base_path / "tables"
    for p in [base_path, figures, html, tables]:
        p.mkdir(parents=True, exist_ok=True)
    return {"base": base_path, "figures": figures, "html": html, "tables": tables}

def minmax_scale(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    xmin = np.nanmin(x)
    xmax = np.nanmax(x)
    return (x - xmin) / (xmax - xmin + eps)

def zscore(x: np.ndarray, eps: float=1e-12) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return (x-x.mean()) / (x.std() + eps)


def normalize_vector_field( 
    u: np.ndarray,                                                              # computing the magnitude of each vector
    v: np.ndarray,                                                              # then turning each vector into a unit direction vector
    w: np.ndarray,                                                              # making the directional pattern of the field easier to inspect
    eps: float=1e-12,                   
    
)-> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:                      # return 4 arrays together in a tuple
    mag = np.sqrt(u**2 + v**2 + w**2)
                                                                                # returning now the the normalized field direction
                                                                                # and the original length field
    return u / (mag + eps), v / (mag + eps), w / (mag + eps), mag





def rolling_window(a: np.ndarray, window:int) -> np.ndarray:
    if window > a.shape[0]:                                                      # making overlapping windows from an array
        raise ValueError("window must be <= first dimension length")             # for the fancy guys like rolling entropy, local seq analysis
                                                                                 # feeding short temporal analysis segments into another function
    shape = (a.shape[0] - window +1, window) + a.shap[1:]                        # leveraging NumPy walks through memory 
                                                                                 # an array => values + shapes + stride interpretation
                                                                                 # def the shape of the output array + keep all non-time dimensions in tact
    strides = (a.strides[0],) + a.strides                                        # a stride -> how many bytes do I move in memory to get to the next element
                                                                                 # along a given axis. so low-level, it's the underworld.
                                                                                 # new strides -> overlapping windows without copying data
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)      # reinterpret my reality. old a, new array 
                                                                                 # IF SHAPE = DOCTRINE, STRIDE = LITURGY
                                                                                 # SHAPE NAMES THE WORLD, STRIDE IS THE LIGHT PASSING THROUGH IT 

    
    

   
    


