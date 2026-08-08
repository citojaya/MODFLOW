# Beginner MODFLOW 6 model built with FloPy

This project contains a steady-state groundwater-flow model defined entirely
in [`build_model.py`](build_model.py). FloPy creates the MODFLOW 6 input files
locally. The generated files can then be transferred to a remote server and
run using [`run_mf6.sh`](run_mf6.sh).

## Model definition

- Grid: 1 layer, 21 rows, 21 columns
- Cell size: 100 m by 100 m (2,100 m by 2,100 m domain)
- Layer top and bottom: 100 m and 80 m (20 m thick)
- Layer type: convertible/unconfined (`ICELLTYPE = 1`)
- Hydraulic conductivity: 10 m/day
- Left constant-head boundary: 100 m
- Right constant-head boundary: 90 m
- Uniform recharge: 0.001 m/day
- Central pumping well: layer 1, row 11, column 11 at -1,000 m3/day
- Initial heads: linear decline from 100 m to 90 m, left to right

Recharge over all 441 cells contributes 4,410 m3/day. Pumping is negative
because it removes water. The constant-head boundaries supply or remove the
remainder required to balance the steady-state model.

## Requirements

- Python 3.10 or newer
- FloPy
- NumPy
- Matplotlib (for plotting)
- VTK and PyVista (for ParaView export)
- A MODFLOW 6 executable named `mf6` on the remote server `PATH`

For example, create a Conda environment with:

```powershell
conda create -n mf6 -c conda-forge python=3.12 flopy vtk pyvista matplotlib numpy pandas jupyterlab
conda activate mf6
```

## Generate the MODFLOW 6 files

From this directory, run:

```powershell
python build_model.py
```

The script:

1. Defines the simulation and groundwater-flow model with FloPy.
2. Writes the MODFLOW 6 simulation and package files into this directory.

It does not run MODFLOW 6 and therefore does not require a local `mf6`
executable.

Generated input files include `mfsim.nam`, `beginner.nam`, `beginner.tdis`,
`beginner.ims`, `beginner.dis`, `beginner.ic`, `beginner.npf`, `beginner.chd`,
`beginner.rcha`, `beginner.wel`, and `beginner.oc`.

## Run on the remote server

Transfer the generated input files and `run_mf6.sh` to the same directory on
the remote server, then submit the PBS job:

```bash
qsub run_mf6.sh
```

The job script runs `mf6` directly. The server environment must make the
MODFLOW 6 executable available on `PATH`; adjust the server's `module load`
commands in `run_mf6.sh` if required.

The main calculated outputs are:

- `beginner.hds`: binary simulated heads
- `beginner.cbc`: binary cell-by-cell flows
- `beginner.lst`: model listing and water budget
- `mfsim.lst`: simulation listing

Running the builder replaces generated MODFLOW input files such as
`mfsim.nam`, `beginner.nam`, `beginner.dis`, and the other package files with
the definitions in `build_model.py`.

## Plot results

After a successful model run:

```powershell
python plot_results.py
```

This prints selected head statistics, displays the head contours, and writes
`calculated_heads.png`.

## Export for ParaView

After a successful model run:

```powershell
python export_paraview.py
```

This writes calculated heads and specific-discharge vectors to the
`paraview/` directory.

## PBS/HPC execution

`run_mf6.sh` is a PBS job script that runs the previously generated model with
the remote server's `mf6` executable. It does not require Python or FloPy.
