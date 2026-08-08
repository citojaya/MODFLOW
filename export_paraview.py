from pathlib import Path

import flopy
from flopy.export import vtk
from flopy.utils import HeadFile, CellBudgetFile
from flopy.utils.postprocessing import get_specific_discharge

workspace = Path(".")
output = workspace / "paraview"
output.mkdir(exist_ok=True)

print("Loading model...")

simulation = flopy.mf6.MFSimulation.load(
    sim_ws=workspace,
    load_only=["dis"],
    verbosity_level=0,
)

model = simulation.get_model("beginner")

# Export calculated heads
head_file = HeadFile(workspace / "beginner.hds")

head_export = vtk.Vtk(
    model=model,
    xml=True,
    binary=True,
    pvd=True,
    point_scalars=True,
    vertical_exageration=5,
)

head_export.add_heads(head_file)
head_export.write(output / "beginner_heads.vtu")

# Export specific discharge as a three-component flow vector.  Do not pass the
# entire CBC file to add_cell_budget(): FLOW-JA-FACE contains one value per
# cell connection (2,121 here), rather than one value per model cell (441).
budget_file = CellBudgetFile(workspace / "beginner.cbc")
spdis = budget_file.get_data(text="DATA-SPDIS")[-1]
qx, qy, qz = get_specific_discharge(spdis, model)

budget_export = vtk.Vtk(
    model=model,
    xml=True,
    binary=True,
    vertical_exageration=5,
)

budget_export.add_vector((qx, qy, qz), "specific_discharge")
budget_export.write(output / "beginner_flow.vtu")

print("ParaView files:")
for filename in sorted(output.iterdir()):
    print(filename)
