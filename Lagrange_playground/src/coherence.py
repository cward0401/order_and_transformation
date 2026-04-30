from __future__ import annotations

import numpy as np

"""
"In the neuter austerity of that terrain all phenomena were bequeathed
a strange equality, and no one thing nor spider nor stone nor blade of grass
could put forth claim to precedence. The very clarity of these articles
belies their familiarity, for the eye predicates the whole on some feature
or part and here was nothing more luminous than another and nothing more
enshadowed and in the optical democracy of such landscapes all preference
is made whimsical and a man and a rock become endowed with unguessed
kinships."

- Cormac McCarthy, Blood Meridian

Coherence
=========
This module measures the field's capacity to remain intelligible to itself.

where entropy tracks differentiation and recurrence tracks return, 
coherence tracks consonance: the degree to which neighboring structures,
successive states, and reconstructed forms preserve a lawful relation accross change.

A field may move, shear, twist, recurse, or unfold - but if it's relations remain 
legible across neighboring cells, across time, or across compressed representations,
then it retains structural continuity.
"""

def neighbor_agreement(field: np.ndarray) -> np.ndarray:            # measures local phase consonance b/w each cell
    center = field                                                  # and it's four wrapped neighbors

    neighbors = np.stack(
        [
            np.roll(field, 1, axis=0),
            np.roll(field, -1, axis=0),
            np.roll(field, 1, axis=1),
            np.roll(field, -1, axis=1),
        ],
        axis=0,
    )

    return np.mean(np.cos(center - neighbors), axis=0)

def _rowwise_corr(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a.reshape(a.shape[0], -1)
    b = b.reshape(b.shape[0], -1)

    a_centered = a - a.mean(axis=1, keepdims=True)
    b_centered = b - b.mean(axis=1, keepdims=True)

    numerator = np.sum(a_centered * b_centered, axis=1)
    denominator = np.sqrt(
        np.sum(a_centered**2, axis=1) * np.sum(b_centered**2, axis=1)
    )

    return np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, np.nan, dtype=float),
        where=denominator > 0,
    )

def structural_persistence(history: np.ndarray) -> np.ndarray:                  # Measures frame-to-frame continuity across an evolving 
    previous_frames = history[:-1]                                              # field history
    next_frames = history[1:]

    return _rowwise_corr(previous_frames, next_frames)

def closure_coherence(history: np.ndarray, lag: int = 6) -> np.ndarray:         # Measures delayed self-relation: does the field preserves
    earlier_frames = history[:-lag]                                             # recognizeable form after a specified temporal interval
    later_frames = history[lag:]

    return _rowwise_corr(earlier_frames, later_frames)

def reconstruction_coherence(history: np.ndarray, rank: int = 3) -> np.ndarray: # Measures how well each field state can be reconstructed from a 
    U, S, VT = np.linal.svd(history, full_matrices=False)                       # reduced singular-value structure
                                                                                # for each frame in histry, SVD is performed and reconstructs 
    recon = (U[:, :, :rank] * S[:, None, :rank]) @ VT[:, :rank, :]              # the frame using only the top rank singular components
                                                                                # then we measure how close the reconstruction is to the original
    return _rowwise_corr(history, recon)                                        # how much of the field's structure survives compression?
                                                                                # 'Is your best good enough?', basically.


def coherence_tensor(field: np.ndarray):                                        # Combines local agreement and directional flow alignment 
    agreement = neighbor_agreement(field)                                       # into a composite coherence surface
                                                                                # Numpy returns gradients in axis order: rows, then columns
    gy, gx = np.gradient(field)                                                 # get's the angle of the gradient direction 
    flow_alignment = np.cos(np.arctan2(gy, gx))                                 # and turns that angle into an alignment value weighted 70/30

    tensor = 0.7 * agreement + 0.3 * flow_alignment

    return agreement, flow_alignment, tensor