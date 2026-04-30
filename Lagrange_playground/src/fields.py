from __future__ import annotations

import numpy as np
from .utils import normalize_vector_field

"""
"The slant black shapes of the mounted men stenciled across
the stone with a definition austere and implacable like 
shapes capable of violating their covenant with the flesh
that authored them, and continuing autonomous across the 
naked rock without reference to sun or man or god." 

- Cormac McCarthy, Blood Meridian


Fields
=======

This module creates the terrains in which the system acts.

A field is treated as more than an array of values. It is a structured
surface: a domain where rhythm, curvature, phase, distortion, and 
neighbor influence can be made visible and allowed to evolve.

The functions here generate scalar fields, transformed fields, 
vector fields, and field histories. They establish the initial 
conditions and transformation rules from which later diagnostics can
read entropy, coherence, recurrence, and trajectory.
"""
 

def make_grid_2d(n: int=140, span: float = 3.0):            # Let's create the domain on which the field will live
    x = np.linspace(-span, span, n)                         # (it's just a 2-D coordinate grid)- spanning the...
    y = np.linspace(-span, span, n)                         # span, and interspaced by the value of n
    X, Y = np.meshgrid(x, y)
    return X, Y 
                                                            # taking our 1D axis arrays..
def make_grid_3d(n: int = 16, span: float = 2.0):           # and expanding them into 2D because-- what would Rudolph Steiner do?
    axis = np.linspace(-span, span, n)                      # basis expansion cosplaying as meshgrid
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")  # which, is the matrix-valued representation of all ordered
    return X, Y, Z                                          # pairs from the cartesian product of the two axes
                                                            # This is the fabric of the plane. 


                                                            # takes the coordinate grid from make_grid_2d and..
                                                            # assigns a number to every point in the plane. 
                                                            # evaluating the whole plane at once via tuning knobs: alpha, beta, gamma
def scalar_field(
    X: np.ndarray,                                          # these are not single No.s..
    Y:np.ndarray,                                           # they are whole 2D arrays
    alpha: float = 1.5,                                     # the EQ knobs...
    beta: float = 2.0,                                      # (don't touch my settings!)
    gamma: float = 0.35                                     # j/k... you can change them to get diff structures
):
    R = np.sqrt(X**2 + Y**2)                                # distance for every point from the origin
                                                            # angle of each point around the origin
    Theta = np.arctan2(Y, X)                                # arctan2 bc she's self-aware (knows which quadrant she's in)
    field = np.sin(alpha * X**2 + beta * Y) * np.cos(beta * Y**2 - alpha * X)   # <-HEADLINER: 
                                                            # squared terms create curvature in the pattern.
                                                            # alpha: creates one oscillation input: a curved x contributes to a linear y
                                                            # beta: reverses what's upstairs
                                                            # then multiply the two oscillatory α and ß for a woven variation.(facbric[warp/weft])
    field += gamma * np.cos(4 * Theta) * np.exp(-0.35 * R**2)
                                                            # take what's just happened and, make it nice!
                                                            # With a repeating pattern around the circle + 4-fold symmetry
                                                            # scaled by a radial decay term: as R get's bigger, gamma gets smaller..
                                                            # making the angular adornment strongest near the center and fade outward...
                                                            # gamma is a central four-fold resonance knob
    return field                                            # Say it, again: angular symmetry, center-emphasis, decay with distance.


def transformed_scalar_field(                               # and now we ask the plane to remember that its visible geometry...
    X: np.ndarray,                                          # is not its only geometry 
    Y: np.ndarray,                                          # it starts with ordinary coordinates, then warp em'
    warp: float = 0.65,                                     # the field is manifest through warped coordinates, 
    twist: float = 2.5,                                     # and its coordinate substrate emerges with the karmic imprint of torsion.
):
    R = np.sqrt(X**2 + Y**2)                                # here's our friend: distance from the origin
    Theta = np.arctan2(Y, X)                                # and his friend: angle around the origin
    Xw = X + warp * np.sin(twist * Theta) * np.exp(-0.2 * R**2)
    Yw = Y + warp * np.cos(twist * Theta) * np.exp(-0.2 * R**2) # take the coordinates and add an amgular, radially damped nudge; ever-so-slightly
                                                            # WE ARE NOT WRITING A NEW FIELD FORMULA!
                                                            # We are feeding the warped coordinates into the existing field generator
                                                            # the transformation happens in the geometry of the domain...
                                                            # not in the field law itself
    return scalar_field(Xw, Yw, alpha=1.8, beta=1.35, gamma=0.45)


def scalar_to_vector_field(                                 # how do we derive directional tendency from a scalar landscape?
    X: np.ndarray,                                          # scalar to vector because Linear Algebra is my Love Language
    Y: np.ndarray,                                          # scalar field -> Topography
    F: np.ndarray,                                          # vector field -> Instruction of movement
    rotational_weight: float = 0.35                         # This guy asks: given the terrain, what directional bias lives inside?
):                                                          # A: gradient-derived directional structure w/added rotational bias
                                                            # gradient => how steeply the field changes in x and y (directional signature)
                                                            # (It's just the slope.)
                                                            # Numpy: axis 0= rows(y-direction), axis 1=columns(x-direction)
    dFy, dFx = np.gradient(F)                               # computes how F changes along each axis
    U = dFx  - rotational_weight * Y                        # (-Y, X) -> classic 'swirl' ..
    V = dFy + rotational_weight * X                         # field around the origin- its two flips-> up, left
                                                            # It is gradient structure plus orbital tendency'
    return U, V                                             # U = x component;V = y component 
    

                                                            # We are going to take one field and evolve it through discrete time.
                                                            # so instead of one field, we will have a history of fields. 
                                                            # scalar_field is the law of manifestation, 
                                                            # transformed_scalar_field is the field manifest with its karmic imprints
                                                            # evolve_field is recurrence-renewed participation in possibility ...
                                                            # (new phone, new live-love-laugh)
def evolve_field(
    initial_field: np.ndarray,                              # start
    steps: int = 80,                                        # No. of updates 
    a: float = 1.0,                                         # how strong is neighborhood coupling
    b: float = 0.25,                                        # how strong is the local nonlinear self
    m: float = 2 * np.pi                                    # modulus to wrap values
):
    state = np.array(initial_field, dtype=float)            # float fax of the initial field
    history = [state.copy()]                                # initializing a list to store every time step...
                                                            # .copy() otherwise we'd append references to the same changing array
                                                            # Building a local neighborhood aggregate - or a food COOP. 
                                                            # It's not all about you, look around.
    for _ in range(steps):
        nbr = (
            np.roll(state, 1, axis=0)
            + np.roll(state, -1, axis=0)
            + np.roll(state, 1, axis=1)
            + np.roll(state, -1, axis=1)
            + state
        )                                                   # let's call this a 'neighborhood walk'-
        state = np.mod(a * nbr + b * np.sin(state), m)      # it's a neighborhood-coupled update law
                                                            # a*nbr is the neighborhood aggr
        history.append(state.copy())                        # it's own personal, non-linear baggage is b*...(state)
                                                            # m reminds you that this neighborhood is really a donut,
    return np.stack(history, axis=0)                        # (and it's your turn to stock melons)

def resonance_vector_field_3d(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    a: float = 1.2,
    b: float = 0.9,
    c: float = 0.7,
    twist: float = 0.65,
):
    U = np.sin(a * Y) - twist * Z + 0.35 * np.cos(X * Z)
    V = np.sin(b * Z) + twist * X + 0.35 * np.cos(X * Y)
    W = np.sin(c * X) - twist * Y + 0.35 * np.cos(Y * Z)

    return normalize_vector_field(U, V, W)                                                                                   
        
        
    
