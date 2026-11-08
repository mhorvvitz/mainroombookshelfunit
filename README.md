# Main-room nook unit — carpenter package

**Status: PROVISIONAL. Nothing here may be cut.** Every controlling dimension
(2900 run, 2600 ceiling) is an architect's plan dimension. A plan dimension is
an intention; a wall is a fact. Fill in the yellow cells on the **Measure first**
tab of the workbook, send them back, and the whole package regenerates from the
same source in minutes.

## What's in the folder

| File | What it is |
|---|---|
| `Nook_unit_shop_drawing.pdf` | A3 sheet — front elevation 1:15, section A–A, plan 1:20, critical notes, title block |
| `Nook_unit_cutlist.xlsx` | 30 line items / 99 pieces, sheet take-off, hardware schedule, site-measurement checklist |
| `assembly_plan.md` | Build order + per-part drilling coordinates (cam-and-dowel, System 32) |
| `cutlist.md` | Same cut list as plain text, for pasting into a quote request |
| `spec.json` | The positioned-part spec — the single source of truth |
| `spec_build.py` | Regenerates everything above. Change a number here, not in the outputs |
| `shopdrawing.svg` | Editable vector source of the drawing sheet |

Everything downstream is derived from `spec.json`, so the drawing, the cut list
and the assembly plan cannot disagree with one another. Never hand-edit an
output to fix a number — fix `spec_build.py` and re-run.

## The design in one paragraph

A 2900 × 2600 sprayed-MDF built-in on the 200mm concrete external wall, with a
reading nook recessed into the centre. Symmetrical about the centreline: four
389 shelf columns, a 1200 nook, and above the header one continuous seven-bay
rhythm at ~388 running the full width. Three depth planes — 320 upper shelves,
430 base cabinets with routed shaker doors, 500 bench projecting 70 proud. A
counter at 900 ties the base run together. Plinth at 100, crown from 2500 to the
ceiling, both scribed.

## The three numbers that are load-bearing

Each of these came out of a calculation, not a preference. Changing one without
redoing the arithmetic produces something that looks fine on day one and is
visibly wrong in three years.

**1. The header is an L-beam, not a plank.** Over the 1200 nook, a 36mm
laminated deck carrying three bays of books deflects 6.5mm immediately and
~9.8mm once MDF creep is counted. A 40×6 steel flat bar on edge only gets it to
3.5mm. The 80mm fascia glued *and* screwed to the front edge raises the second
moment of area from 1.24×10⁶ to 1.05×10⁷ mm⁴ and brings it to 1.2mm. **Do not
omit the fascia. Do not substitute a single 18mm deck.**

**2. The bench deck is 22mm over two mullions.** 18mm over one mullion gives
4.8mm under an 80kg adult — a seat that visibly flexes. 22mm over two mullions
gives 0.51mm. The three resulting drawer fronts at 388 also line up with the
three upper centre bays, so the vertical rhythm carries through the nook.

**3. Shelf bays are 386–389 everywhere.** That is not an aesthetic accident —
it keeps every shelf at 0.23mm sag under a full book load with plain 18mm MDF,
with no nosing, no steel and no thicker stock anywhere in the unit.

## Open items — these need answers, not assumptions

1. **Site measurement.** Three widths, three heights, both diagonals. Build to
   the *smallest* reading. The 2900 here is nominal: the carcass must be built
   to the measured minimum **minus a 15–20mm scribe** at the right-hand end.
   This allowance is **not** yet in the cut list, because the measurement that
   sets it does not exist yet.
2. **Is 2600 finished floor to finished ceiling?** A bulkhead, fan-coil or
   curtain pelmet changes the entire upper stack.
3. **Depth available behind the left 600 for the closet.** The bookcase takes
   430 there; the closet gets whatever remains. Hanging coats wants ~600.
4. **Does the right-hand end meet a wall?** Scribe filler if yes, finished
   return panel if no.
5. **Handles.** Not chosen, and the choice changes front machining.
6. **Electrical.** Two sconces and a socket. The conduit goes in before plaster
   and cannot be retrofitted behind a fixed built-in. Positions to be set with
   the חשמלאי on site.
7. **The 4" drain stack** runs in this wall. Have the plumber mark it before
   anyone drills. One anchor into a 110mm PVC stack ruins the wall.

## Notes for the נגר

- **No edge banding anywhere.** All MDF edges are sealed, filled and sprayed.
- **Backs sit in a 4mm dado**, not on cam fittings. The assembly plan covers the
  structural carcass only, because the script would otherwise specify a Ø15 cam
  housing in a 4mm back panel.
- **Upper backs are visible** inside the open shelving — 10mm MDF, sprayed both
  faces. Base backs are hidden behind doors — 4mm hardboard, one face.
- **Piers are 2×18 laminated to 36mm**, full height 100–2500, glued across the
  full face. They carry the header and the whole upper centre.
- **No vertical panel lands on the wall/closet junction at x=600** — it falls
  inside bay 2. The bookcase carcass is self-supporting; the closet is a
  separate box behind it.
- **Crown is two lengths** with a scarf joint on the left pier centreline
  (x=832), where a vertical shadow line already falls. A single 2900 piece
  exceeds every sheet in the catalogue.
- **Fixing is into 200mm concrete** — M8 sleeve or chemical anchors. Anti-tip
  fixing is mandatory; children climb open drawers.
- The sheet take-off is an area estimate plus 30%, **not** an optimised nesting
  plan. Run OpenCutList or CutList Optimizer for the real cut plan.

## Confidence

| Claim | Confidence |
|---|---|
| Geometry is internally consistent; 99 parts, zero collisions | **high** — `check_overlaps()` clean, every part validated against real sheet stock |
| Deflection calculations | **high** on the method (standard beam theory), **moderate** on MDF E=3000 N/mm² — it varies by board; the margins are wide enough to absorb it |
| Material thicknesses exist in Israeli stock | **moderate** — from the skill's seeded supplier data, confirm with your yard |
| Runner and hinge clearances | **moderate** — typical values, confirm against the actual product datasheet before machining |
| That 2900 × 2600 is what is actually on site | **unknown** — nobody has measured it |
