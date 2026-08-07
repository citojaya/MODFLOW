# Beginner MODFLOW 6 model

This directory contains a complete, steady-state MODFLOW 6 groundwater-flow
model. Run it from this directory with:

```powershell
mf6
```

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

Recharge over all 441 cells contributes 4,410 m3/day. Pumping is represented
by a negative rate because it removes water. The side boundaries supply or
remove the remainder needed to balance the steady-state model.

## Important files

- `mfsim.nam`: simulation entry point
- `beginner.dis`: grid and layer elevations
- `beginner.npf`: hydraulic properties
- `beginner.chd`: left and right constant heads
- `beginner.rcha`: recharge
- `beginner.wel`: pumping well
- `beginner.oc`: head and budget output controls

After a successful run, the main outputs are `beginner.hds` (binary heads),
`beginner.cbc` (binary cell-by-cell flows), and `beginner.lst` (listing and
water-budget information).
