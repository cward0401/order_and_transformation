from __future__ import annotations

import numpy as np
from .utils import rolling_window

"""
"A Legion of horribles, hundreds in number, half naked or 
clad in costumes attic or biblical or wardrobed out of a 
fevered dream with the skins of animals and silk finery and 
pieces of uniform still tracked with the blood of prior owners,
coats of slain dragoons, frogged and braided cavalry jackets,
one in a stovepipe hat and one with an umbrealla and one in white
stockings and a bloodstained wedding veil and some in headgear
of cranefeathers or rawhide helmets that bore the horns of bull
or buffalo and one in a pigeontailed coat worn backwards and 
otherwise naked and one in the armor of a Spanish conquistador,
the breastplate and pauldrons deeply dented with old blows of mace 
or sabre done in another country by men whose very bones were dust
and many with their braids spliced up with the hair of other beasts
until they railed upon the ground and their horses' ears and tails 
worked with bits of brightly colored cloth and one whose horse's
whole head was painted crimson red and all the horsemen's faces
gaudy and grotesque with daubings like a company of mounted clowns,
death hilarious, all howling in a barbarous tongue and riding down
upon them like a horde from hell more horrible yet than the brimstone
land of christian reckoning, screeching and yammering and clothed in smoke 
like those vaporous beings in regions beyond right knowing where the eye wanders
and the lip jerks and drools."


- Cormac McCarthy, Blood Meridian


Entropy
=======

This module measures differentiation within the field.

Entropy is used here as a diagnostic of distribution: 
how values spread, concentrate, diversify, or collapse 
across a scalar surface or time series.

Entropy is not 'chaos', in the cheap sense. It is the 
breadth of live possibility still circulating in 
the system. 

"""




def shannon_entropy_from_hist(values: np.ndarray, bins: int = 24,                        # Shannon - unertainty made measureable via symbolic distribution.
value_range=None, eps: float = 1e-12)-> float:                                           # Because, we are not running a casino here. 
    hist, _ = np.histogram(values.ravel(), bins=bins, range=value_range, density=False)  # ravel() flattens the array into one long vector. 
    p = hist / (hist.sum() + eps)                                                        # (Raw vals-> bins to histograms-> converts counts intp probs-> computes Shannon)
    p = p[p > 0]                                                                         # we boolean our way our of zero probabilities
    return float(-(p * np.log2(p + eps)).sum())                                          # log gives us the depth of specification and we negate it to deal with
                                                                                         # the log values between zero and one. 

def global_entropy(field: np.ndarray, bins: int = 24) -> float:                          # This is an uber taking the whole field to the Shannon Entropy function
    return shannon_entropy_from_hist(field, bins=bins)                                   # It returns one scalar rating.


def local_entropy_map(field: np.ndarray, window: int = 7, bins: int = 12) -> np.ndarray:  # This block computes Shannon Entropy around each shell of a 2D field for every (i, j)
    pad = window // 2                                                                    #it grabs the 7 x a7 locals, computes entropy of the area and stores the results in the same positing at shipping
    padded = np.pad(field, pad, mode="wrap")                                             # this adds a border around the field the No of cells specified by pad, and our mode is periodic (TOROIDAL)

    patches = np.lib.stride_tricks.sliding_window_view(                                  # Numpy docs caution against using it.  
        padded,                                                                          # I will stride like a Subaru rallying through the forest at sunset.
        window_shape=(window, window),                                                   
    )

    entropy_values = [                                                                   # Well, hello. Welcome to my list comprehension.
        shannon_entropy_from_hist(patch, bins=bins)                                      # We can calculate one entropy _ per patch, without nested column/row indexing
        for patch in patches.reshape(-1, window, window)
    ]

    return np.array(entropy_values).reshape(field.shape)                                 # we send the field back out as its original shape.

def entropy_over_time(history: np.ndarray, bins: int = 24) -> np.ndarray:                # We are taking a time-history of fields and computing one global entropy value per frame
    return np.array([global_entropy(frame, bins=bins) for frame in history])             # Math says: at time t, compute the hits distro of field values, then get Shannon on the phone
                                                                                         # gotcha: this loops over time, not space. spacial/local gets compressed into one scalar
def entropy_gradient_tensor(field: np.ndarray):                                          # Tensors: What remains lawfully legible when the frame changes?
    gy, gx = np.gradient(field)                                                          # we're taking a scalar field and extracting it's directional transformation pressure
    mag = np.sqrt(gx**2 + gy**2)                                                         # gx= horizontal change, gy=vertical change, mag=instenity of chane-> gradient bundle
    return gx, gy, mag

def windowed_entropy_series(series: np.ndarray, window: int = 24, bins: int = 12) -> np.ndarray:
    wins = rolling_window(np.asanyarray(series), window)                                # This block takes a 1D series, cuts it into roling windows and coputes Shannon for each view
    return np.array([shannon_entropy_from_hist(w, bins) for w in wins])                 # This gives entropy as a moving diagnostic over a time series
                                                                                        # gotcha: the output is shorter than the input
                                                                                        