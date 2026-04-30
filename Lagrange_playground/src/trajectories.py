from __future__ import annotations
import numpy as np

"""
"They crossed before the sun and vanished one by one and reappeared again
and they were black in the sun and they rode out of that vanished sea 
like burnt phantoms with the legs of the animals kicking up the spume
that was not real and they were lost in the sun and lost in the lake 
and they shimmered and slurred together and separated again and they
augmented by planes in lurid avatars and began to coalesce 
and there began to appear above them in the dawn-broached sky
a hellish likeness of their ranks riding huge and elongate
trampling down the high thin cirrus and the howling antiwarriors 
pendant from their mounts immense and chimeric and the high wild cries
carrying that flat and barren pan like the cries of souls broke through
some misweave in the weft of things into the world below."

- Cormac McCarthy, Blood Meridian


Trajectories
============

This module tracks motion through a field.

A state is not treated as a fixed label, but as a position moving through structured influence.
The trajectory is the record of that movement: where the system begins, what forces act upon it,
and how its path unfolds through time. 

In later applied work, this same logic can describe members, groups, cohorts, 
or whole systems moving through relational state-space.

The point is not only where something is.

The point is how it moves.

"""

def integrate_vector_field(                                                     # This starts at point x0 and repeatedly evaluates
        field_fn,                                                               # a vector field at the current point, 
        x0: np.ndarray,                                                         # moves a small amount in that direction, 
        steps: int = 500,                                                       # and saves the path
        dt: float = 0.03,
        **field_kwargs,
):
    x = np.asarray(x0, dtype=float)
    traj = [x.copy()]                                                           # we send a fax so as not to accidentally mutate later

    for _ in range(steps):
        v = np.asarray(field_fn(x, **field_kwargs), dtype=float)                # Euler(!) integration. 
        if v.shape != x.shape:
            raise ValueError("Field_fn myst return a vector with the same shape as x0")
        
        x = x + dt * v                                                          # ! because Euler has the audacity of divinity, IMO.
        traj.append(x.copy())                                                   # It is rate, state, and self-continuity in one object.
                                                                                # Although what's here is the more mortal version:
    return np.vstack(traj)                                                      # take the present state, ask the field what direction it implies,
                                                                                # then move on e unit of obedience. Not revelation,
                                                                                # but lawful approximation. 

def lagrange_flow(                                                              # The Chamber Door:
        point: np.ndarray,                                                      # The only constant is change - Fortune le veut. 
        a: float = 1.1,                                                         # This func takes a 3D point and returns the local velocity/direction?
        b: float = 0.8,                                                         # It asks: at this position in space, how ya livin'? 
        c: float = 0.6,                                                         # Large and with charge? 
        twist: float = 0.45,                                                    # Unpacking the 3-vector, computing mvmt in the x dir, par example - 
):                                                                              # and evaluating the oscillatory response to y and z pulls/rotates against x
    x, y, z = point                                                             # there's some small nonlinear coupling b/w y and z

    dx = np.sin(a * y) - twist * z + 0.25 * np.cos(y * z)
    dy = np.sin(b * z) + twist * x + 0.25 * np.cos(x * z)
    dz = np.sin(c * x) - twist * y + 0.25 * np.cos(x * y)

    return np.array([dx, dy, dz])

def multi_seed_trajectories(                                                    # What this does is runs the same flow from multiple starting points.
        seeds: np.ndarray,                                                      # Many seeds, many paths.
        steps: int = 400,
        dt: float = 0.025,
        **flow_kwargs,
):
    traces = []                                                                 # Trajectory storage. 

    for seed in seeds:                                                          # Extra parameters are fwd to lagrange_flow
        traces.append(                                                          # lagrange_flow is used as the vector field
            integrate_vector_field(                                             # start from the specified seed and walk fwd a dt-sized step
                lagrange_flow,                                                  # hand off all flow parameters 
                seed,                                                           # Traces is a list of trajectory arrays
                steps=steps,                                                    # This list-retun dtpe is a gotcha bc it's not a Numpy array
                dt=dt,                                                          # but this is Plotly's show and this is how he does it.
                **flow_kwargs,
            )
        )
    return traces

def series_from_history(                                                        # It's a dictionary as dispatch table:
        history: np.ndarray,                                                    # string command -> executable reducer
        reducer: str = "mean",                                                  # It looks up the command, retrieves the matching operation
) -> np.ndarray:                                                                # and gets it done. 
    reducers = {
        "mean": lambda h: h.mean(axis=(1, 2)),
        "std": lambda h: h.std(axis=(1, 2)),
        "energy": lambda h: h.sqrt((h**2).mean(axis=(1, 2))),
    }

    if reducer not in reducer:
        valid = ", ".join(reducers)
        raise ValueError(f"reducer must be of: {valid}")
    
    return reducers[reducer](history)
