#!/usr/bin/env python3
"""
Horvitz main-room bookshelf unit with recessed bench nook.
Positioned-part spec. ALL DIMENSIONS mm. Origin: X=0 left end of run,
Y=0 finished floor, Z=0 back face (against wall), front face at +Z.

STATUS: PROVISIONAL. Controlling dimensions (2900 run, 2600 ceiling) come from
the architect's plan, NOT site measurement. No part may be cut from this.
"""
import sys, os, json
SKILL = "/root/.claude/skills/synced/50b1bd87-06ff-4b00-829c-fb046f957e69_776f7a00-b6d1-4357-825f-9f68130378de/furniture-design"
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from carcass import Carcass, cutlist_parts, check_overlaps

T       = 18   # carcass panel, MDF
T_FRONT = 19   # routed shaker fronts, MDF
MAT = "mdf"

# ---------------- controlling dimensions ----------------
RUN      = 2900   # plan      total face length
CEIL     = 2600   # plan      finished floor to ceiling
WALL_END = 600    # plan      concrete wall ends here from left; closet behind 0..600

# ---------------- depth planes (Z, from wall face) ----------------
D_UPPER  = 320    # standard  upper shelf carcass — books read properly
D_BASE   = 412    # derived   base carcass; +18 shaker door = 430 face
D_COUNT  = 440    # derived   counter, 10mm proud of doors
D_BENCH  = 482    # user      bench carcass; +18 drawer front = 500 face
D_PIER   = 412    # derived   nook piers, full height
PLINTH_SETBACK = 60

# ---------------- vertical stack (Y) ----------------
Y_PLINTH   = 100   # standard  plinth height
Y_BASE_TOP = 881   # derived   (counter is 19mm MDF, not 20)
Y_COUNT    = 900   # standard  counter surface
Y_BENCH    = 380   # standard  bench platform top (+90 cushion = ~450 seat)
Y_HDR_U    = 1680  # derived   header underside -> 1300 nook clear above platform
Y_HDR_T    = 1716  # derived   header is 36mm (laminated 2x18) for the 1300 span
Y_SHELF2   = 2117  # derived   second full-width shelf line (top face)
Y_SHELF1   = 1308  # derived   side-column-only shelf line (top face)
Y_CARC_TOP = 2500  # derived   carcass top; 2500..2600 = crown, scribes to ceiling

# ---------------- horizontal layout (X) ----------------
# Symmetric about the 2900 centreline: the nook is the focal point of a painted
# shaker piece with crown and plinth, and an off-centre focal point reads as an
# error. Four 389 columns + a 1200 nook; the nook's three upper bays also come
# out at 388, so the band above the header is ONE regular 7-bay rhythm.
# 18 | 389 | 18 | 389 | 36 | 1200 | 36 | 389 | 18 | 389 | 18  = 2900
COL, NOOK = 389, 1200
x = 0
V1   = x; x += T            # 0..18      left end panel (exposed, by the door)
BA   = x; x += COL          # 18..407
V2   = x; x += T            # 407..425
BB   = x; x += COL          # 425..814   (wall starts at 600 inside this bay)
PIER_L = x; x += 2*T        # 814..850
X_NOOK = x; x += NOOK       # 850..2050
PIER_R = x; x += 2*T        # 2050..2086
BC   = x; x += COL          # 2086..2475
V4   = x; x += T            # 2475..2493
BD   = x; x += COL          # 2493..2882
V5   = x; x += T            # 2882..2900 right end, scribes to wall
assert x == RUN, x
SINGLE_V = (V1, V2, V4, V5)
BAYS = [(V1 + T, V2), (V2 + T, PIER_L), (PIER_R + 2*T, V4), (V4 + T, V5)]

c = Carcass(RUN, CEIL, D_BENCH, t=T, material=MAT, name="NookUnit")
A = c.add

# ============ PLINTH (sprayed MDF, set back; carcass on adjustable legs) ====
A("PlinthBase",  0, 0, D_BASE - PLINTH_SETBACK - T, X_NOOK, Y_PLINTH, T, note="left run, set back 60")
A("PlinthBench", X_NOOK, 0, D_BENCH - PLINTH_SETBACK - T, NOOK, Y_PLINTH, T, note="bench, projects 70")
A("PlinthBase",  X_NOOK + NOOK, 0, D_BASE - PLINTH_SETBACK - T, RUN - (X_NOOK + NOOK), Y_PLINTH, T)

# ============ NOOK PIERS — full height, carry header + upper centre =========
for px in (PIER_L, PIER_R):
    A("Pier", px,     Y_PLINTH, 0, T, Y_CARC_TOP - Y_PLINTH, D_PIER, note="laminated leaf 1 of 2")
    A("Pier", px + T, Y_PLINTH, 0, T, Y_CARC_TOP - Y_PLINTH, D_PIER, note="laminated leaf 2 of 2")

# ============ BASE ZONE  Y 100..880 =========================================
# base side panels (end panels + inner dividers); the piers are the nook sides
for xp in SINGLE_V:
    A("BaseSide", xp, Y_PLINTH, 0, T, Y_BASE_TOP - Y_PLINTH, D_BASE)
# base bottoms + tops per bay
for (x0, x1) in BAYS:
    w = x1 - x0
    A("BaseBottom", x0, Y_PLINTH, 0, w, T, D_BASE)
    A("BaseTop",    x0, Y_BASE_TOP - T, 0, w, T, D_BASE)
    A("BaseBack",   x0, Y_PLINTH + T, 0, w, Y_BASE_TOP - Y_PLINTH - 2*T, 4, material="hardboard", grain="none")
    # fronts: skinny top drawer + shaker door pair below
    op0, op1 = Y_PLINTH + T, Y_BASE_TOP - T          # clear opening 118..862 = 744
    g = 3
    DRW_H = 150
    A("BaseDrawerFront", x0 + g, op1 - DRW_H, D_BASE, w - 2*g, DRW_H - g, T_FRONT, kind="door")
    door_h = (op1 - DRW_H - g) - (op0 + g)
    leaves = 2 if w > 620 else 1
    lw = (w - 2*g - (leaves - 1)*g) / leaves
    for i in range(leaves):
        A("BaseDoor", x0 + g + i*(lw + g), op0 + g, D_BASE, lw, door_h, T_FRONT, kind="door")
    # drawer box for the skinny drawer (side-mount ball bearing, -26)
    bw = w - 26
    A("SkinnyBoxSide", x0 + (w - bw)/2, op1 - DRW_H + 10, 40, 12, DRW_H - 35, D_BASE - 70,
      material="plywood_birch", grain="none")
    A("SkinnyBoxSide", x0 + (w - bw)/2 + bw - 12, op1 - DRW_H + 10, 40, 12, DRW_H - 35, D_BASE - 70,
      material="plywood_birch", grain="none")

# ============ COUNTER  Y 880..900 ==========================================
# BUGFIX 1: counter ran 18mm into each pier. Butts to the pier face instead.
A("Counter", 0, Y_BASE_TOP, 0, PIER_L, Y_COUNT - Y_BASE_TOP, D_COUNT, note="20mm, 10 proud of doors")
A("Counter", PIER_R + 2*T, Y_BASE_TOP, 0, RUN - (PIER_R + 2*T), Y_COUNT - Y_BASE_TOP, D_COUNT)

# ============ BENCH MODULE  Y 100..380, between the piers ==================
A("BenchBottom",   X_NOOK, Y_PLINTH, 0, NOOK, T, D_BENCH)
# 25mm deck on TWO mullions. An 80kg adult on an 18mm deck over one mullion
# deflects 4.8mm — a springy seat. 25mm over 388 spans gives 0.51mm.
# The three drawer fronts at 388 also line up with the three upper centre bays.
T_DECK = 28   # TWO drawers = one mullion = 591 span. 22mm gives 2.63mm under
              # an 80kg adult; 28mm gives 1.28mm. 28 is stocked, 25 is not.
A("BenchPlatform", X_NOOK, Y_BENCH - T_DECK, 0, NOOK, T_DECK, D_BENCH, note="28mm seat deck; 90 cushion on top")
bo0, bo1 = Y_PLINTH + T, Y_BENCH - T_DECK
BW = (NOOK - T) / 2                                # 591.0 clear per drawer
A("BenchMullion", X_NOOK + BW, bo0, 0, T, bo1 - bo0, D_BENCH)
for i in range(2):
    fw = (NOOK - 3*3) / 2
    A("BenchDrawerFront", X_NOOK + 3 + i*(fw + 3), bo0 + 3, D_BENCH, fw, (bo1 - bo0) - 6, T_FRONT, kind="door")
    bx = X_NOOK + i*(BW + T)
    for off in (0, BW - 26 - 15):
        A("BenchBoxSide", bx + 13 + off, bo0 + 8, 30, 15, (bo1 - bo0) - 30, 440,
          material="plywood_birch", grain="none")

# ============ NOOK BACK — board & batten on a 30mm SERVICE VOID =============
# There is an existing outlet low down and central: it lands behind the bench
# drawers. Burying a live box behind fixed joinery with no access is not on.
# Furring the nook back 30mm off the concrete creates a service void, so the
# socket and both sconces are wired WITHOUT chasing the external wall — and the
# existing box stays reachable by pulling the centre bench drawer out.
VOID = 30
NB_H = Y_HDR_U - Y_BENCH
for i in range(5):
    fx_ = X_NOOK + 6 + i * (NOOK - 57) / 4
    A("NookFurring", fx_, Y_BENCH, 0, 45, NB_H, VOID,
      note="vertical furring; leaves a 30mm service void against the concrete")
A("NookBack", X_NOOK, Y_BENCH, VOID, NOOK, NB_H, T,
  note="18 MDF ground on the furring; cut the socket + 2 sconce boxes on site")
n_bat = 7
bat_w = 70
pitch = (NOOK - bat_w) / (n_bat - 1)
for i in range(n_bat):
    A("NookBatten", X_NOOK + i*pitch, Y_BENCH, VOID + T, bat_w, NB_H, 12,
      note="12mm applied face batten at 189 centres")

# ============ HEADER over the nook — 36mm laminated =========================
A("Header", X_NOOK, Y_HDR_U, 0, NOOK, T, D_UPPER, note="laminated leaf 1 of 2")
A("Header", X_NOOK, Y_HDR_U + T, 0, NOOK, T, D_UPPER, note="laminated leaf 2 of 2")
# 80mm fascia glued+screwed to the front edge turns the flat deck into an L-beam:
# I goes 1.24e6 -> 1.05e7, sag 9.8mm -> 1.2mm over time. Also conceals an LED strip.
for k in (0, 1):
    A("HeaderFascia", X_NOOK, Y_HDR_U - 80, D_UPPER - 2*T + k*T, NOOK, 80, T,
      note=f"80 downstand, laminated leaf {k+1} of 2; makes the header an L-beam")

# ============ UPPER ZONE  Y 900..2500 ======================================
for xp in SINGLE_V:
    A("UpperSide", xp, Y_COUNT, 0, T, Y_CARC_TOP - Y_COUNT, D_UPPER)
for (x0, x1) in BAYS:
    w = x1 - x0
    A("UpperTop",  x0, Y_CARC_TOP - T, 0, w, T, D_UPPER)
    A("UpperBack", x0, Y_COUNT, 0, w, Y_CARC_TOP - Y_COUNT - T, 10, material="mdf", grain="none")
    # shelves sit in FRONT of the 4mm inset back (z=4), 16mm front setback
    for ytop in (Y_SHELF1, Y_HDR_T, Y_SHELF2):
        A("Shelf", x0 + 1, ytop - T, 10, w - 2, T, D_UPPER - 26)
# centre bay above the header — TWO dividers, so the upper band reads as one
# regular rhythm of 421..564 bays right across the 2900, no divider lands on the
# nook centreline, and no shelf above the header spans more than 421.
A("UpperTop", X_NOOK, Y_CARC_TOP - T, 0, NOOK, T, D_UPPER)
A("UpperBack", X_NOOK, Y_HDR_T, 0, NOOK, Y_CARC_TOP - Y_HDR_T - T, 10, material="mdf", grain="none")
# No dividers: the centre reads as one full-width opening top to bottom.
# A plain 18mm shelf at 1200 sags 21mm (32mm with creep). 36mm laminated is
# still 4.0mm. 36mm + a 40mm front nosing is an L-beam at 1.45mm — the same
# trick as the header, one tier lighter, and the two bands line up.
for k in (0, 1):
    A("ShelfWide", X_NOOK + 1, Y_SHELF2 - 2*T + k*T, 10, NOOK - 2, T, D_UPPER - 26,
      note=f"laminated leaf {k+1} of 2 -> 36mm")
    A("ShelfNosing", X_NOOK + 1, Y_SHELF2 - 2*T - 40, D_UPPER - 26 + 10 - 2*T + k*T,
      NOOK - 2, 40, T, note=f"40mm nosing, leaf {k+1} of 2; glue+screw to the shelf front")

# ============ CROWN  Y 2500..2600 ===========================================
# BUGFIX 3: a single 2900 fascia exceeds every sheet in the catalogue (max 2800).
# Split at the left pier centreline (1073) where a vertical shadow line already
# falls, so the scarf joint is invisible.
CROWN_JT = PIER_L + T   # 832 — left pier centreline, where a shadow line already falls
A("CrownFascia", 0, Y_CARC_TOP, D_UPPER - T, CROWN_JT, CEIL - Y_CARC_TOP, T, note="scribed to ceiling; scarf joint at pier CL")
A("CrownFascia", CROWN_JT, Y_CARC_TOP, D_UPPER - T, RUN - CROWN_JT, CEIL - Y_CARC_TOP, T, note="scribed to ceiling")

spec = c.spec()
print(f"positioned parts: {len(spec['parts'])}")
w = check_overlaps(spec)
print(f"\noverlap warnings: {len(w)}")
for s in w:
    print("  " + s)
json.dump(spec, open("/home/claude/nook/spec.json", "w"), indent=1)
print("\n--- cut list groups ---")
for p in sorted(cutlist_parts(spec), key=lambda r: -r["length"]):
    print(f"  {p['qty']:2}x {p['name']:18} {p['length']:>5} x {p['width']:>4}  {p['material']}")

# ---------------- emitters ----------------
from draw import draw
from render import render
draw(spec, "/home/claude/nook/elevation.svg",
     title="Horvitz nook unit — front elevation (mm) — PROVISIONAL, plan dims")
render(spec, "/home/claude/nook/preview.html",
       title="Horvitz nook unit — 2900 x 2600")
print("\nemitted elevation.svg + preview.html")
