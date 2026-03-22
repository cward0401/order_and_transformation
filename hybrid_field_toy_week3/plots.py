# Wha does the system look like?
import matplotlib.pyplot as plt 


def plot_field_2d(field, m):
    plt.figure(figsize=(10, 6))
    plt.imshow(field, aspect='auto', cmap='turbo', interpolation='nearest', vmin=0, vmax=m-1)
    plt.colorbar(ticks=range(m))
    plt.xlabel("cell position")
    plt.ylabel("time step")
    plt.title("Hybrid Modular Field")
    plt.show()



def plot_entropy(entropy_curve):
    plt.figure(figsize=(10, 4))
    plt.plot(entropy_curve)
    plt.xlabel("time step")
    plt.ylabel("entropy")
    plt.title("Field Entropy Over Time")
    plt.show()


def plot_coherence(coherence_curve):
    plt.figure(figsize=(10, 4))
    plt.plot(coherence_curve)
    plt.xlabel("time step")
    plt.ylabel("cpherence")
    plt.title("Field Coherence Over Time")
    plt.show()

def plot_reconstruction(recon_curve):
    plt.figure(figsize=(10, 4))
    plt.plot(recon_curve)
    plt.xlabel("time step")
    plt.ylabel("reconstruction coherence")
    plt.title("Reconstruction Coherence")
    plt.show()

def plot_compression(compression_curve):
    plt.figure(figsize=(10, 4))
    plt.plot(compression_curve)
    plt.xlabel("time step")
    plt.ylabel("compression ratio")
    plt.title("Structural Compression Ratio")
    plt.show()

def plot_diagnostic_panel(field, entropy_curve, coherence_curve, recon_curve, compression_curve, m):
    plt.figure(figsize=(12, 12))

    plt.subplot(5, 1, 1)
    plt.imshow(field, aspect='auto', cmap='turbo', interpolation='nearest', vmin=0, vmax=m-1)
    plt.ylabel("time")
    plt.title("Pattern Field")

    plt.subplot(5, 1, 2)
    plt.plot(entropy_curve)
    plt.ylabel("entropy")
    plt.title("Entropy")

    plt.subplot(5, 1, 3)
    plt.plot(coherence_curve)
    plt.ylabel("coherence")
    plt.title("Coherence")

    plt.subplot(5, 1, 4)
    plt.plot(recon_curve)
    plt.ylabel("recon")
    plt.title("Reconstruction Coherence")

    plt.subplot(5, 1, 5)
    plt.plot(compression_curve)
    plt.ylabel("compress")
    plt.xlabel("time step")
    plt.title("Structural Compression Ratio")

    plt.tight_layout()
    plt.show()
