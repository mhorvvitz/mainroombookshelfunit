# Main-room nook unit — v1.0

**Design locked.** Every decision is settled and recorded in the review
artifact's store: greige paint, horizontal shiplap nook back, no dividers
anywhere, knobs on doors with bar pulls on drawers in brass, no sconces, socket
inside a bench drawer, LED strip behind the header fascia, sprayed MDF counter,
door with an adjustable shelf behind each base front, skinny drawers kept,
frieze-plus-cove crown, recessed plinth with a cap moulding, 90mm HR foam cushion.

**One thing still blocks cutting: nobody has measured the wall.** Every
controlling dimension (2900 run, 2600 ceiling) is an architect's plan dimension.
A plan dimension is an intention; a wall is a fact. Fill in the yellow cells on
the *Measure first* tab of the workbook and the whole package regenerates from
the same source in minutes.

## Build cost — ₪14,400–23,000 all in, incl. VAT

| | ₪ | confidence |
|---|---:|---|
| Sheet materials | 1,900 | **high** — real quoted price list |
| Hardware | 2,400 | **low** — my estimate, price it |
| Joinery all in (includes both rows above) | 13,000–18,900 | **moderate** |
| Electrician, cushion, fitting | 1,400–4,200 | **low** |
| **All in** | **14,400–23,000** | |

Two independent methods, cross-checked. Sheet prices come from a current
Israeli cutting-service price list; the labour figure is a published benchmark
of ₪1,500–2,000/m² for a custom MDF unit, loaded 15–25% because this piece is
not a plain wardrobe — laminated piers and header, seven nosings, shiplap,
mouldings and three depth planes. Implied labour lands at 67–77% of the total,
which is the right band for sprayed joinery. Full working on the **Cost** tab
of the workbook.

This is a budgeting estimate, not a quote. Get three נגרים to price the actual
cut list and compare.

## What's in the repo

| Path | What it is |
|---|---|
| `drawings/Nook_unit_drawings.pdf` | Three A3 sheets — (1) front elevation keyed to a dimension table, (2) section + plan, (3) electrical |
| `drawings/Nook_unit_cutlist.xlsx` | 32 line items / 86 pieces, sheet take-off, hardware schedule, site-measurement checklist |
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
reading nook recessed into the centre. Symmetrical about the centreline: two
796 side bays and a 1200 nook, with no dividers anywhere — every shelf runs the
full width of its bay. Every shelf shows a 70mm front band.
Three depth planes — 320 upper shelves, 430 base cabinets with routed shaker
doors, 500 bench projecting 70 proud. A
counter at 900 ties the base run together. Plinth at 100, crown from 2500 to the
ceiling, both scribed. Behind the left 600 the wall ends and a closet sits
back-to-back, opening toward the door.

## The five numbers that are load-bearing

Each came out of a calculation, not a preference. Change one without redoing the
arithmetic and you get something that looks fine on day one and is visibly wrong
in three years.

**1. The header is an L-beam, not a plank.** Over the 1200 nook, a 36mm
laminated deck carrying a full book load deflects 6.5mm immediately and ~9.8mm
once MDF creep is counted. A 40×6 steel flat bar on edge only reaches 3.5mm.
The fix is a fascia glued *and* screwed to the front edge. A 70mm visible band
gives 4.5mm and a 90mm band 2.4mm — no margin. **100mm (36 deck + 64 drop) is
the first honest number**, at 1.16mm. It also conceals the LED strip.

**2. Every shelf shows a 70mm front band, and that is structural.** With all
dividers removed the side bays span 796 and the centre spans 1200. Plain 18mm
sags 6.2mm at 796 and 32mm at 1200 — span punishes you to the fourth power.
Side shelves are 18mm deck + a 52mm nosing (0.67mm); the centre shelf is 36mm
deck + a 34mm nosing (1.76mm). Different decks, identical 70mm face, so the
line reads continuous across the whole unit.

**3. The bench deck is 28mm over one mullion.** Two drawers means one mullion
and a 591 span. 18mm gives 4.8mm under an 80kg adult and 22mm gives 2.63mm —
both are seats you can feel move. 28mm gives 1.28mm. 25mm would do it too but
is not a stocked MDF thickness.

**4. The nook back is furred 30mm off the concrete.** The existing outlet sits
low and central, right behind the bench. Rather than move it, it spurs to a
socket **inside the right-hand bench drawer** — a charging drawer that also
houses the LED driver, so the shiplap runs unbroken with no box cut into it. The
old box stays live and reachable by pulling that drawer out, which satisfies the
access rule. The 30mm void then carries exactly one low-voltage cable up to the
LED. Nothing is chased into the external wall.

**5. The LED behind the header fascia is not decoration.** With the sconces
gone it is the only thing lighting the nook. Without it the recess reads as a
black hole from the couch — which is the failure mode of every dark built-in in
a room this size.

## Still open

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
4. The exact height and offset of the existing outlet — it sets the spur
   length to the drawer socket and where the Ø20 hole goes in the bench deck.

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
- **Buy all eleven brass handles in one order.** Unlacquered brass patinates
  and will not match a piece bought later.
- **Everything is 19mm.** 18mm MDF is not a stocked thickness in Israel —
  supplier lists run 17/19/24/28. Carcass, fronts and shelves are all 19mm.
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
| Geometry is internally consistent; 86 parts, zero collisions | **high** — `check_overlaps()` clean, every part validated against real sheet stock |
| Deflection calculations | **high** on the method (standard beam theory), **moderate** on MDF E=3000 N/mm² — it varies by board; the margins absorb it |
| Material thicknesses exist in Israeli stock | **high** — every thickness cross-checked against a live supplier price list |
| Cost estimate | **moderate** overall; **high** on sheet prices, **low** on hardware |
| Runner and hinge clearances | **moderate** — typical values, confirm against the product datasheet before machining |
| That 2900 × 2600 is what is actually on site | **unknown** — nobody has measured it |
