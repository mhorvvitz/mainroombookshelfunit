# Main-room nook unit — carpenter package

**Status: DRAFT. Cuts are not locked.** Two things stand between this and a
buildable package:

1. **Thirteen design decisions are open.** They live on the Decisions tab of the
   review artifact, each with a recommendation and the reasoning behind it.
2. **Nobody has measured the wall.** Every controlling dimension (2900 run, 2600
   ceiling) is an architect's plan dimension. A plan dimension is an intention;
   a wall is a fact.

Settle both and the whole package regenerates from the same source in minutes.

## What's in the repo

| Path | What it is |
|---|---|
| `drawings/Nook_unit_drawings.pdf` | Three A3 sheets — (1) front elevation keyed to a dimension table, (2) section + plan, (3) electrical |
| `drawings/Nook_unit_cutlist.xlsx` | 31 line items / 99 pieces, sheet take-off, hardware schedule, site-measurement checklist |
| `drawings/assembly_plan.md` | Build order + per-part drilling coordinates (cam-and-dowel, System 32) |
| `drawings/cutlist.md` | Same cut list as plain text, for pasting into a quote request |
| `src/spec_build.py` | **The source.** Change a number here, never in an output |
| `src/spec.json` | The positioned-part spec that every output derives from |
| `src/sheets.py`, `src/make_cutlist.py`, `src/make_xlsx.py` | The emitters |
| `src/review_src.html` | The review artifact (3D + elevation + decisions) |

Everything downstream derives from `spec.json`, so the drawing, the cut list and
the assembly plan cannot disagree. Never hand-edit an output to fix a number.

```
python3 src/spec_build.py && python3 src/make_cutlist.py \
  && python3 src/sheets.py && python3 src/make_xlsx.py
```

## The design in one paragraph

A 2900 × 2600 sprayed-MDF built-in on the 200mm concrete external wall, with a
reading nook recessed into the centre. Symmetrical about the centreline: four
389 shelf columns and a 1200 nook, the nook running full width top to bottom
with no divider above the header. Three depth planes — 320 upper shelves,
430 base cabinets with routed shaker doors, 500 bench projecting 70 proud. A
counter at 900 ties the base run together. Plinth at 100, crown from 2500 to the
ceiling, both scribed. Behind the left 600 the wall ends and a closet sits
back-to-back, opening toward the door.

## The four numbers that are load-bearing

Each came out of a calculation, not a preference. Change one without redoing the
arithmetic and you get something that looks fine on day one and is visibly wrong
in three years.

**1. The header is an L-beam, not a plank.** Over the 1200 nook, a 36mm
laminated deck carrying three bays of books deflects 6.5mm immediately and
~9.8mm once MDF creep is counted. A 40×6 steel flat bar on edge only reaches
3.5mm. The 80mm fascia glued *and* screwed to the front edge raises the second
moment of area from 1.24×10⁶ to 1.05×10⁷ mm⁴ and brings it to 1.2mm. **Do not
omit the fascia. Do not substitute a single 18mm deck.**

**2. The centre shelf is 36mm with a 40mm nosing.** With the dividers removed
it spans the full 1200. Plain 18mm there sags 21mm, going to 32mm with creep —
span punishes you to the fourth power. 36mm laminated alone is still 4.0mm. A
30×5 steel bar only reaches 5.0mm. 36mm plus a 40mm front nosing is an L-beam
at 1.45mm, and the band lines up under the header's 80mm fascia.

**3. The bench deck is 28mm over one mullion.** Two drawers means one mullion
and a 591 span. 18mm gives 4.8mm under an 80kg adult and 22mm gives 2.63mm —
both are seats you can feel move. 28mm gives 1.28mm. 25mm would do it too but
is not a stocked MDF thickness.

**3b. Side shelf bays are 386–389.** That keeps every one of the twelve side
shelves at 0.23mm under a full book load with plain 18mm MDF — no nosing, no
steel, no thicker stock.

**4. The nook back is furred 30mm off the concrete.** There is an existing
outlet low and central, directly behind the bench drawers. A live box may not be
buried behind fixed joinery with no access. The furring creates a service void
so the relocated socket and both sconces wire through it with **no chasing of
the external wall**, and the old box stays reachable by pulling the centre bench
drawer out. This turned a code problem into a saving.

## Open items

**Thirteen design decisions** — on the review artifact's Decisions tab: paint,
nook back treatment, counter material, shelf-back colour, handles, what goes
behind the base doors, the skinny drawer, crown profile, plinth profile, socket
position, sconce type, concealed LED, cushion.

**Site measurement** — three widths, three heights, both diagonals. Build to the
*smallest* reading. The 2900 here is nominal: the carcass must be built to the
measured minimum **minus a 15–20mm scribe** at the right-hand end. That
allowance is **not** in the cut list, because the measurement that sets it does
not exist yet.

**Four facts nobody has established:**

1. Depth available behind the left 600 for the closet. The bookcase takes 430
   there; the closet gets what remains, and hanging coats wants ~600.
2. Whether the right-hand end meets a wall (scribe) or is open (return panel).
3. Where the 4" drain stack runs. Have the plumber mark it before anyone drills
   — one anchor into a 110mm PVC stack opens the wall.
4. The exact height and offset of the existing outlet.

## Notes for the נגר

- **No edge banding anywhere.** All MDF edges are sealed, filled and sprayed.
- **Backs sit in a 4mm dado**, not on cam fittings. The assembly plan covers the
  structural carcass only — left to itself the generator specifies a Ø15 cam
  housing in a 4mm back panel.
- **Upper backs are visible** inside the open shelving: 10mm MDF, sprayed both
  faces. Base backs are hidden behind doors: 4mm hardboard, one face.
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
| Deflection calculations | **high** on the method (standard beam theory), **moderate** on MDF E=3000 N/mm² — it varies by board; the margins absorb it |
| Material thicknesses exist in Israeli stock | **moderate** — from seeded supplier data, confirm with your yard |
| Runner and hinge clearances | **moderate** — typical values, confirm against the product datasheet before machining |
| That 2900 × 2600 is what is actually on site | **unknown** — nobody has measured it |
