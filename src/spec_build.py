#!/usr/bin/env python3
"""
Horvitz main-room bookshelf unit with recessed bench nook.
Positioned-part spec. ALL DIMENSIONS mm. Origin: X=0 left end of the run,
Y=0 finished floor, Z=0 back face (against the concrete), front face at +Z.

STATUS: DRAFT. Controlling dimensions (2900 run, 2600 ceiling) are from the
architect's plan, NOT site measurement. No part may be cut from this.

Decisions in force: paint greige · nook back horizontal shiplap · handles
knobs on doors + bar pulls on drawers, BRASS · no sconces · socket inside a
bench drawer · LED strip concealed behind the header fascia · no dividers
anywhere, so the two side bays and the nook each run full width.
"""
import sys, os, json
SKILL = "/root/.claude/skills/synced/50b1bd87-06ff-4b00-829c-fb046f957e69_776f7a00-b6d1-4357-825f-9f68130378de/furniture-design"
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from carcass import Carcass, cutlist_parts, check_overlaps

# 18mm MDF IS NOT STOCKED IN ISRAEL. Supplier lists run 17/19/24/28 and the
# skill catalogue 16/19/22/28/30. Everything is 19mm: carcass and fronts alike.
T       = 19
T_FRONT = 19
MAT = "mdf"

# ---------------- controlling dimensions ----------------
RUN      = 2900   # plan      total face length
CEIL     = 2600   # plan      finished floor to finished ceiling (CONFIRMED)
WALL_END = 600    # plan      concrete ends here; closet back-to-back behind 0..600

# ---------------- depth planes (Z, from the wall face) ----------------
D_UPPER  = 320
D_BASE   = 412    # + 19 shaker door = 431 face
D_COUNT  = 440
D_BENCH  = 482    # + 19 drawer front = 501 face
D_PIER   = 412
VOID     = 28     # service void behind the nook back — LED feed runs here (28mm rips)
PLINTH_SETBACK = 60

# ---------------- vertical stack (Y) ----------------
Y_PLINTH   = 100
T_DECK     = 28   # bench deck: TWO drawers = one mullion = 591 span.
                  # 22mm gives 2.63mm under 80kg; 28mm gives 1.28mm.
Y_BENCH    = 380  # deck top (+90 cushion ≈ 450 finished seat)
Y_BASE_TOP = 881
Y_COUNT    = 900  # counter surface (19mm)
HDR_DECK   = 2*T  # 38, two 19mm leaves laminated
HDR_DROP   = 62   # fascia below a 38 deck -> 100 visible band.
                  # At 92 kg/m over 1200 a 70 band is 4.48mm and 90 is 2.40mm
                  # (no margin). 100 is the first honest number. Hides the LED.
Y_HDR_T    = 1716                    # header deck top
Y_HDR_U    = Y_HDR_T - HDR_DECK      # 1680 deck underside
Y_FASCIA_U = Y_HDR_U - HDR_DROP      # 1616 fascia underside = nook clear height
Y_SHELF1   = 1308
Y_SHELF2   = 2117
Y_CARC_TOP = 2500                    # crown 2500..2600, scribed to the ceiling

NOSE_SIDE  = 51   # 19 deck + 51 nosing  = 70 band, 793 span -> 0.63mm
NOSE_MID   = 32   # 38 deck + 32 nosing  = 70 band, 1200 span -> 1.64mm

# ---------------- horizontal layout (X) ----------------
# No dividers anywhere. Two full-width side bays and the nook.
# 19 | 793 | 38 pier | 1200 nook | 38 pier | 793 | 19  = 2900
BAY, NOOK = 793, 1200
x = 0
V1     = x; x += T          # 0..18      left end panel (exposed, by the door)
BL     = x; x += BAY        # 18..814    (concrete starts at 600 inside this bay)
PIER_L = x; x += 2*T        # 814..850
X_NOOK = x; x += NOOK       # 850..2050
PIER_R = x; x += 2*T        # 2050..2086
BR     = x; x += BAY        # 2086..2882
V5     = x; x += T          # 2882..2900 right end, scribes to the wall
assert x == RUN, x
SINGLE_V = (V1, V5)
BAYS = [(V1 + T, PIER_L), (PIER_R + 2*T, V5)]

c = Carcass(RUN, CEIL, D_BENCH, t=T, material=MAT, name="NookUnit")
A = c.add

# ============ PLINTH ========================================================
A("PlinthBase",  0, 0, D_BASE - PLINTH_SETBACK - T, X_NOOK, Y_PLINTH, T, note="set back 60; cap moulding on top")
A("PlinthBench", X_NOOK, 0, D_BENCH - PLINTH_SETBACK - T, NOOK, Y_PLINTH, T, note="bench plinth, projects 70")
A("PlinthBase",  X_NOOK + NOOK, 0, D_BASE - PLINTH_SETBACK - T, RUN - (X_NOOK + NOOK), Y_PLINTH, T)

# ============ NOOK PIERS — full height, carry the header ====================
for px in (PIER_L, PIER_R):
    for k in (0, 1):
        A("Pier", px + k*T, Y_PLINTH, 0, T, Y_CARC_TOP - Y_PLINTH, D_PIER,
          note=f"laminated leaf {k+1} of 2 -> 36mm")

# ============ BASE ZONE  Y 100..881 =========================================
for xp in SINGLE_V:
    A("BaseSide", xp, Y_PLINTH, 0, T, Y_BASE_TOP - Y_PLINTH, D_BASE)
for (x0, x1) in BAYS:
    w = x1 - x0
    A("BaseBottom", x0, Y_PLINTH, 0, w, T, D_BASE)
    A("BaseTop",    x0, Y_BASE_TOP - T, 0, w, T, D_BASE)
    A("BaseBack",   x0, Y_PLINTH + T, 0, w, Y_BASE_TOP - Y_PLINTH - 2*T, 4,
      material="hardboard", grain="none")
    op0, op1 = Y_PLINTH + T, Y_BASE_TOP - T          # 118..863 = 745 clear
    g, DRW_H = 3, 150
    # two skinny drawers over two doors, so the vertical rhythm matches
    for i in range(2):
        fw = (w - 3*g) / 2
        A("BaseDrawerFront", x0 + g + i*(fw + g), op1 - DRW_H, D_BASE, fw, DRW_H - g, T_FRONT, kind="door")
        bw = fw - 26
        for off in (0, bw - 12):
            A("SkinnyBoxSide", x0 + g + i*(fw + g) + 13 + off, op1 - DRW_H + 10, 40,
              12, DRW_H - 35, D_BASE - 70, material="plywood_birch", grain="none")
    door_h = (op1 - DRW_H - g) - (op0 + g)
    for i in range(2):
        lw = (w - 3*g) / 2
        A("BaseDoor", x0 + g + i*(lw + g), op0 + g, D_BASE, lw, door_h, T_FRONT, kind="door")

# ============ COUNTER  Y 881..900 ===========================================
A("Counter", 0, Y_BASE_TOP, 0, PIER_L, Y_COUNT - Y_BASE_TOP, D_COUNT, note="19mm, 10 proud of the doors")
A("Counter", PIER_R + 2*T, Y_BASE_TOP, 0, RUN - (PIER_R + 2*T), Y_COUNT - Y_BASE_TOP, D_COUNT)

# ============ BENCH MODULE  Y 100..380 ======================================
A("BenchBottom",   X_NOOK, Y_PLINTH, 0, NOOK, T, D_BENCH)
A("BenchPlatform", X_NOOK, Y_BENCH - T_DECK, 0, NOOK, T_DECK, D_BENCH, note="28mm seat deck")
bo0, bo1 = Y_PLINTH + T, Y_BENCH - T_DECK
BW = (NOOK - T) / 2                                   # 591 clear per drawer
A("BenchMullion", X_NOOK + BW, bo0, 0, T, bo1 - bo0, D_BENCH)
for i in range(2):
    fw = (NOOK - 3*3) / 2
    A("BenchDrawerFront", X_NOOK + 3 + i*(fw + 3), bo0 + 3, D_BENCH, fw, (bo1 - bo0) - 6, T_FRONT, kind="door")
    bx = X_NOOK + i*(BW + T)
    for off in (0, BW - 26 - 12):
        A("BenchBoxSide", bx + 13 + off, bo0 + 8, 30, 12, (bo1 - bo0) - 30, 440,
          material="plywood_birch", grain="none")

# ============ NOOK BACK — horizontal shiplap on a 30mm SERVICE VOID =========
# The socket now lives inside a bench drawer, fed straight off the existing
# box. The void is kept for ONE job: the low-voltage run from the driver in
# the bench up to the LED strip behind the header fascia.
NB_H = Y_FASCIA_U - Y_BENCH
for i in range(5):
    A("NookFurring", X_NOOK + 6 + i*(NOOK - 57)/4, Y_BENCH, 0, 45, NB_H, VOID,
      note="vertical furring; leaves the 30mm service void against the concrete")
A("NookBack", X_NOOK, Y_BENCH, VOID, NOOK, NB_H, T, note="18 MDF ground behind the shiplap")
N_BOARD, BG = 9, 6
BH = (NB_H - (N_BOARD - 1)*BG) / N_BOARD
for i in range(N_BOARD):
    A("ShiplapBoard", X_NOOK, Y_BENCH + i*(BH + BG), VOID + T, NOOK, BH, 12,
      note=f"horizontal shiplap, {N_BOARD} boards, {BG}mm shadow gap")

# ============ HEADER — 36 deck + 64 fascia = 100 band, hides the LED ========
for k in (0, 1):
    A("Header", X_NOOK, Y_HDR_U + k*T, 0, NOOK, T, D_UPPER, note=f"laminated leaf {k+1} of 2")
    A("HeaderFascia", X_NOOK, Y_FASCIA_U, D_UPPER - 2*T + k*T, NOOK, HDR_DROP, T,
      note=f"64 downstand, leaf {k+1} of 2; L-beam + conceals the LED strip")

# ============ UPPER ZONE  Y 900..2500 =======================================
for xp in SINGLE_V:
    A("UpperSide", xp, Y_COUNT, 0, T, Y_CARC_TOP - Y_COUNT, D_UPPER)
for (x0, x1) in BAYS:
    w = x1 - x0
    A("UpperTop",  x0, Y_CARC_TOP - T, 0, w, T, D_UPPER)
    A("UpperBack", x0, Y_COUNT, 0, w, Y_CARC_TOP - Y_COUNT - T, 12, material="mdf", grain="none")
    # 18 deck + 52 nosing = 70 band. Plain 18mm at 796 sags 6.2mm with creep.
    for ytop in (Y_SHELF1, Y_HDR_T, Y_SHELF2):
        A("Shelf", x0 + 1, ytop - T, 12, w - 2, T, D_UPPER - 28)
        A("ShelfNosing", x0 + 1, ytop - T - NOSE_SIDE, D_UPPER - 28 + 12 - T,
          w - 2, NOSE_SIDE, T, note="52 below the deck -> 70 visible band")
# centre: one full-width shelf, 36 deck + 34 nosing = the same 70 band
A("UpperTop", X_NOOK, Y_CARC_TOP - T, 0, NOOK, T, D_UPPER)
A("UpperBack", X_NOOK, Y_HDR_T, 0, NOOK, Y_CARC_TOP - Y_HDR_T - T, 12, material="mdf", grain="none")
for k in (0, 1):
    A("ShelfWide", X_NOOK + 1, Y_SHELF2 - 2*T + k*T, 12, NOOK - 2, T, D_UPPER - 28,
      note=f"laminated leaf {k+1} of 2 -> 36mm")
A("ShelfWideNosing", X_NOOK + 1, Y_SHELF2 - 2*T - NOSE_MID, D_UPPER - 28 + 12 - T,
  NOOK - 2, NOSE_MID, T, note="34 below a 36 deck -> the same 70 visible band")

# ============ CROWN =========================================================
CROWN_JT = PIER_L + T
A("CrownFascia", 0, Y_CARC_TOP, D_UPPER - T, CROWN_JT, CEIL - Y_CARC_TOP, T,
  note="scribed to the ceiling; scarf joint on the pier centreline")
A("CrownFascia", CROWN_JT, Y_CARC_TOP, D_UPPER - T, RUN - CROWN_JT, CEIL - Y_CARC_TOP, T,
  note="scribed to the ceiling")

spec = c.spec()
print(f"positioned parts: {len(spec['parts'])}")
w = check_overlaps(spec)
print(f"overlap warnings: {len(w)}")
for s in w: print("  " + s)
json.dump(spec, open("/home/claude/nook/spec.json", "w"), indent=1)
print(f"\nnook clear: {NOOK} wide x {Y_FASCIA_U - Y_BENCH} high above the deck")
print(f"side bays: {BAY} clear, shelves 70mm band")
print("--- cut list groups ---")
for p in sorted(cutlist_parts(spec), key=lambda r: -r["length"]):
    print(f"  {p['qty']:2}x {p['name']:18} {p['length']:>5} x {p['width']:>4}  {p['material']}")
