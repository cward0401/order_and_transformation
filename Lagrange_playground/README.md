# Lagrange Playground

A single static field is closer to Being.  
An evolved history is Becoming.  
The update rule is the investment mechanism.  

Diagnostics tell you what the investment produced:

- Entropy = how much openness remains
- Coherence = whether form survived the passage
- Recurrence = whether the process can return to itself

Lagrange Playground is a 3D-first structural sandbox for exploring entropy, recurrence, coherence, closure, resonance, transformation, and state-space geometry.

## Design Principles

- 3D-first, not line-plot-first
- structure over prediction
- reusable modules
- visualization separated from logic
- parameter regimes treated as landscapes

## First Visual Targets

1. Entropy Surface
2. Recurrence Landscape
3. Coherence Topography
4. 3D Resonance Vector Field
5. State-Space Trajectory Cloud

## Quick Start

```python
from src.utils import ensure_output_dirs

from src.fields import (
    make_grid_2d,
    make_grid_3d,
    transformed_scalar_field,
    evolve_field,
    resonance_vector_field_3d,
)

from src.entropy import (
    local_entropy_map,
    entropy_over_time,
)

from src.recurrence import recurrence_matrix
from src.coherence import coherence_tensor
from src.geometry import state_space_from_history
from src.trajectories import multi_seed_trajectories

from src.visualizations_3d import (
    surface_3d,
    vector_field_3d,
    trajectories_3d,
    recurrence_landscape_3d,
    state_space_cloud_3d,
)