import flopy
import matplotlib.pyplot as plt
import numpy as np

# Read the MODFLOW 6 model and calculated heads
sim = flopy.mf6.MFSimulation.load(sim_ws=".")
model = sim.get_model("beginner")

head_file = flopy.utils.HeadFile("beginner.hds")
heads = head_file.get_data()       # shape: (layer, row, column)
head = heads[0]

print(f"Minimum head: {np.nanmin(head):.3f} m")
print(f"Maximum head: {np.nanmax(head):.3f} m")
print(f"Head at pumping well: {head[10, 10]:.3f} m")

# Plot heads
fig, ax = plt.subplots(figsize=(8, 7))

model_grid = flopy.plot.PlotMapView(model=model, ax=ax)

image = model_grid.plot_array(
    head,
    cmap="viridis",
    alpha=0.85,
)

contours = model_grid.contour_array(
    head,
    levels=15,
    colors="black",
    linewidths=0.7,
)

ax.clabel(contours, fmt="%.1f", fontsize=8)
model_grid.plot_bc("CHD", color="cyan")

# Centre of row 11, column 11
ax.plot(1050, 1050, "rv", markersize=9, label="Pumping well")

fig.colorbar(image, ax=ax, label="Hydraulic head (m)")
ax.set_title("MODFLOW 6 calculated heads")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.legend()
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig("calculated_heads.png", dpi=200)
plt.show()