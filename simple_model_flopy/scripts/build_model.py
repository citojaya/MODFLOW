"""Build the beginner MODFLOW 6 input files entirely with FloPy."""

from pathlib import Path

import flopy
import numpy as np


SIMULATION_NAME = "beginner_simulation"
MODEL_NAME = "beginner"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_INPUT = PROJECT_ROOT / "model_input"
MODEL_OUTPUT = PROJECT_ROOT / "model_output"


def build_model(workspace: str | Path = MODEL_INPUT, executable: str = "mf6"):
    """Create the MODFLOW 6 simulation in memory and return it."""
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    MODEL_OUTPUT.mkdir(parents=True, exist_ok=True)

    # Model dimensions and hydraulic properties.
    nlay, nrow, ncol = 1, 21, 21
    delr = delc = 100.0
    top, bottom = 100.0, 80.0
    hydraulic_conductivity = 10.0
    recharge_rate = 0.001

    simulation = flopy.mf6.MFSimulation(
        sim_name=SIMULATION_NAME,
        version="mf6",
        exe_name=executable,
        sim_ws=workspace,
    )

    flopy.mf6.ModflowTdis(
        simulation,
        time_units="DAYS",
        nper=1,
        perioddata=[(1.0, 1, 1.0)],
    )

    groundwater_flow = flopy.mf6.ModflowGwf(
        simulation,
        modelname=MODEL_NAME,
        model_nam_file=f"{MODEL_NAME}.nam",
        save_flows=True,
    )

    flopy.mf6.ModflowIms(
        simulation,
        print_option="SUMMARY",
        complexity="SIMPLE",
        outer_dvclose=1.0e-6,
        outer_maximum=100,
        inner_dvclose=1.0e-6,
        rcloserecord=1.0e-3,
        inner_maximum=100,
        linear_acceleration="BICGSTAB",
    )

    flopy.mf6.ModflowGwfdis(
        groundwater_flow,
        length_units="METERS",
        nlay=nlay,
        nrow=nrow,
        ncol=ncol,
        delr=delr,
        delc=delc,
        top=top,
        botm=bottom,
        idomain=1,
    )

    # Initial heads decline linearly from 100 m to 90 m, west to east.
    initial_heads = np.tile(np.linspace(100.0, 90.0, ncol), (nlay, nrow, 1))
    flopy.mf6.ModflowGwfic(groundwater_flow, strt=initial_heads)

    flopy.mf6.ModflowGwfnpf(
        groundwater_flow,
        icelltype=1,
        k=hydraulic_conductivity,
        save_flows=True,
        save_specific_discharge=True,
    )

    # FloPy cell identifiers are zero-based: (layer, row, column).
    constant_heads = []
    for row in range(nrow):
        constant_heads.append(((0, row, 0), 100.0))
        constant_heads.append(((0, row, ncol - 1), 90.0))

    flopy.mf6.ModflowGwfchd(
        groundwater_flow,
        pname="CHD",
        stress_period_data={0: constant_heads},
        save_flows=True,
    )

    flopy.mf6.ModflowGwfrcha(
        groundwater_flow,
        pname="RCHA",
        recharge={0: recharge_rate},
        save_flows=True,
    )

    flopy.mf6.ModflowGwfwel(
        groundwater_flow,
        pname="WEL",
        stress_period_data={0: [((0, 10, 10), -1000.0)]},
        save_flows=True,
    )

    flopy.mf6.ModflowGwfoc(
        groundwater_flow,
        head_filerecord=f"../model_output/{MODEL_NAME}.hds",
        budget_filerecord=f"../model_output/{MODEL_NAME}.cbc",
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
        printrecord=[("HEAD", "LAST"), ("BUDGET", "ALL")],
    )

    return simulation


def main() -> None:
    """Write the MODFLOW 6 input files without running the model."""
    simulation = build_model()
    simulation.write_simulation()
    print(f"MODFLOW 6 input files written to: {MODEL_INPUT}")
    print("Submit run_mf6.sh on the remote server to run the model.")


if __name__ == "__main__":
    main()
