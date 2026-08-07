from pathlib import Path

import flopy
from flopy.export.vtk import Vtk
from flopy.utils import HeadFile, CellBudgetFile

workspace = Path(".")
output = workspace / "paraview"
output.mkdir(exist_ok=True)

# Load the MODFLOW 6 model geometry
sim = flopy.mf6.MFSimulation.load(
    sim_ws=workspace,
    load_only=["dis"],
    verbosity_level=0,
)
model = sim.get_model("beginner")

# Export calculated heads
heads = HeadFile(workspace / "beginner.hds")

head_vtk = Vtk(
    model=model,
    xml=True,
    binary=True,
    pvd=True,
    point_scalars=True,
    vertical_exageration=5,
)
head_vtk.add_heads(heads)
head_vtk.write(output / "beginner_heads.vtu")

# Export compatible cell-budget results separately
budget = CellBudgetFile(workspace / "beginner.cbc")

budget_vtk = Vtk(
    model=model,
    xml=True,
    binary=True,
    pvd=True,
    vertical_exageration=5,
)
budget_vtk.add_cell_budget(budget)
budget_vtk.write(output / "beginner_budget.vtu")

print(f"ParaView files written to: {output.resolve()}")