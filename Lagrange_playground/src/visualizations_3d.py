from __future__ import annotations

from pathlib import Path
import numpy as np
import plotly.graph_objects as go 


# Internal validation helpers


def _require_same_shape(*arrays: np.ndarray) -> None:
    shapes = [np.shape(arr) for arr in arrays]

    if len(set(shapes)) != 1:
        raise ValueError(f"all arrays must have the same shape, got: {shapes}")


def _require_square_matrix(matrix: np.ndarray, name: str = "matrix") -> None:
    matrix = np.asarray(matrix)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{name} must be a square 2D matrix")


def _require_points_3d(points: np.ndarray) -> None:
    points = np.asarray(points)

    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (n_points, 3)")


# Shared save/style helper


def save_plotly(fig: go.Figure, html_path: str | Path | None = None):
    fig.update_layout(template="plotly_dark")

    if html_path is not None:
        html_path = Path(html_path)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(html_path))

    return fig



def surface_3d(
    X,
    Y,
    Z,
    title: str = "3D Surface",
    html_path: str | None = None,
):
    _require_same_shape(X, Y, Z)

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                contours={"z": {"show": True, "usecolormap": True}},
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
    )

    return save_plotly(fig, html_path)


def coherence_topography_3d(
    X,
    Y,
    coherence_map,
    title: str = "Coherence Topography",
    html_path: str | None = None,
):
    _require_same_shape(X, Y, coherence_map)

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=coherence_map,
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Coherence",
        ),
    )

    return save_plotly(fig, html_path)


def parameter_resonance_surface(
    X,
    Y,
    Z,
    title: str = "Parameter Resonance Surface",
    html_path: str | None = None,
):
    _require_same_shape(X, Y, Z)

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="a",
            yaxis_title="b",
            zaxis_title="Metric",
        ),
    )

    return save_plotly(fig, html_path)


# Vector field visualization

def vector_field_3d(
    X,
    Y,
    Z,
    U,
    V,
    W,
    mag=None,
    title: str = "3D Vector Field",
    html_path: str | None = None,
    scale: float = 0.6,
):
    _require_same_shape(X, Y, Z, U, V, W)

    if mag is not None:
        _require_same_shape(X, mag)

    fig = go.Figure(
        data=go.Cone(
            x=X.ravel(),
            y=Y.ravel(),
            z=Z.ravel(),
            u=U.ravel(),
            v=V.ravel(),
            w=W.ravel(),
            sizemode="scaled",
            sizeref=scale,
            anchor="tail",
            colorscale="Viridis",
            showscale=True,
        )
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
    )

    return save_plotly(fig, html_path)

# Trajectory visualization


def trajectories_3d(
    traces,
    title: str = "3D Trajectories",
    html_path: str | None = None,
):
    fig = go.Figure()

    for i, tr in enumerate(traces):
        tr = np.asarray(tr)
        _require_points_3d(tr)

        fig.add_trace(
            go.Scatter3d(
                x=tr[:, 0],
                y=tr[:, 1],
                z=tr[:, 2],
                mode="lines",
                name=f"seed_{i}",
                line=dict(width=5),
            )
        )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
    )

    return save_plotly(fig, html_path)



# Recurrence visualization

def recurrence_landscape_3d(
    R: np.ndarray,
    title: str = "Recurrence Landscape",
    html_path: str | None = None,
):
    _require_square_matrix(R, name="R")

    n = R.shape[0]
    axis = np.arange(n)
    X, Y = np.meshgrid(axis, axis)

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=R,
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="Time i",
            yaxis_title="Time j",
            zaxis_title="Recurrence",
        ),
    )

    return save_plotly(fig, html_path)



# State-space visualization

def state_space_cloud_3d(
    points: np.ndarray,
    color_values: np.ndarray | None = None,
    title: str = "State-Space Cloud",
    html_path: str | None = None,
):
    points = np.asarray(points)
    _require_points_3d(points)

    if color_values is None:
        color_values = np.arange(points.shape[0])
    else:
        color_values = np.asarray(color_values)

    if len(color_values) != points.shape[0]:
        raise ValueError("color_values must have one value per point")

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode="lines+markers",
                marker=dict(
                    size=4,
                    color=color_values,
                ),
                line=dict(width=4),
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="Component 1",
            yaxis_title="Component 2",
            zaxis_title="Component 3",
        ),
    )

    return save_plotly(fig, html_path)