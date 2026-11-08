#!/usr/bin/env python3
"""A3 landscape shop-drawing sheet: front elevation, section A-A, plan, title
block. Geometry read from spec.json so it can never disagree with the cut list."""
import json

S = json.load(open("spec.json"))
P = S["parts"]
MM = 3.7795           # px per mm at 96dpi
W, H = 420*MM, 297*MM # A3 landscape
KE = 1/15.0   # elevation + section
KP = 1/20.0   # plan
_K = [KE]
def k(v): return v*MM*_K[0]

INK="#1a1a1a"; THIN="#5a5a5a"; DIM="#9c2b1b"; FILL="#e8e5de"; GHOST="#f3f1ec"; NOTE="#4a4a4a"
o=[]
def rect(x,y,w,h,f=FILL,sw=0.7,st=INK):
    o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{max(w,0.2):.2f}" height="{max(h,0.2):.2f}" fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
def line(x1,y1,x2,y2,c=THIN,sw=0.5,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{sw}"{d}/>')
def txt(x,y,s,sz=6.5,c=INK,a="start",w="400",ff="Helvetica,Arial,sans-serif"):
    o.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{sz}" fill="{c}" text-anchor="{a}" font-weight="{w}" font-family="{ff}">{s}</text>')
def hdim(y,x1,x2,lab,tick=3):
    line(x1,y,x2,y,DIM,0.6)
    for x in (x1,x2): line(x,y-tick,x,y+tick,DIM,0.6)
    txt((x1+x2)/2,y-2.4,lab,5.4,DIM,"middle","500","'Courier New',monospace")
def vdim(x,y1,y2,lab,tick=3):
    line(x,y1,x,y2,DIM,0.6)
    for y in (y1,y2): line(x-tick,y,x+tick,y,DIM,0.6)
    o.append(f'<text x="{x-3.4:.2f}" y="{(y1+y2)/2:.2f}" font-size="5.4" fill="{DIM}" text-anchor="middle" font-weight="500" font-family="\'Courier New\',monospace" transform="rotate(-90 {x-3.4:.2f} {(y1+y2)/2:.2f})">{lab}</text>')

# ============================== FRONT ELEVATION ==============================
EX, EY = 52, 56                      # origin px: left edge, FLOOR line
def fx(x): return EX + k(x)
def fy(y): return EY + k(2600) - k(y)

txt(EX, EY-10, "FRONT ELEVATION", 8, INK, "start", "700")
txt(EX+124, EY+2, "scale 1:15", 6, NOTE)
# ceiling
line(fx(-40), fy(2600), fx(2960), fy(2600), INK, 1.1)
txt(fx(2965), fy(2600)+2, "CEILING 2600 (plan)", 5, NOTE)
# walls either side
rect(fx(-40), fy(2600), k(40), k(2600), GHOST, .6)
rect(fx(2900), fy(2600), k(40), k(2600), GHOST, .6)
# floor
line(fx(-60), fy(0), fx(2980), fy(0), INK, 1.1)

FRONTS = {"BaseDoor","BaseDrawerFront","BenchDrawerFront"}
BOXES  = {"BenchBoxSide","SkinnyBoxSide"}
for p in sorted(P, key=lambda q: q["z"]):
    if p["defn"] in BOXES: continue
    f = "#fbfaf7" if p["defn"] in FRONTS else FILL
    rect(fx(p["x"]), fy(p["y"]+p["sy"]), k(p["sx"]), k(p["sy"]), f, .55)

# horizontal dimension chain
CH = fy(2600) - 9
for a,b,l in [(0,18,"18"),(18,407,"389"),(407,425,"18"),(425,814,"389"),(814,850,"36"),
              (850,2050,"1200"),(2050,2086,"36"),(2086,2475,"389"),(2475,2493,"18"),
              (2493,2882,"389"),(2882,2900,"18")]:
    hdim(CH, fx(a), fx(b), l)
hdim(fy(0)+16, fx(0), fx(2900), "2900  OVERALL  (plan dim — site-measure before cutting)")
hdim(fy(0)+8, fx(814), fx(2086), "1272 nook opening incl. piers")

# vertical dimension chain
CV = fx(0) - 11
for a,b,l in [(0,100,"100"),(100,380,"280"),(380,1600,"1220 nook clear"),(1600,1680,"80"),
              (1680,1716,"36"),(1716,2117,"401"),(2117,2500,"383"),(2500,2600,"100")]:
    vdim(CV, fy(a), fy(b), l)
vdim(CV-13, fy(0), fy(2600), "2600")
# right-side level marks
for y,l in [(100,"+100 plinth"),(380,"+380 seat deck (+90 cushion = 470)"),(900,"+900 counter"),
            (1600,"+1600 fascia u/s"),(1716,"+1716 header top"),(2500,"+2500 carcass top")]:
    line(fx(2900), fy(y), fx(2952), fy(y), THIN, .4, "2 2")
    txt(fx(2956), fy(y)+1.8, l, 5, NOTE)
# section mark
for x in (fx(1450),):
    line(x, fy(2600)-16, x, fy(0)+6, "#2b6ca3", .6, "6 3")
    txt(x, fy(2600)-18, "A", 6.5, "#2b6ca3", "middle", "700")
    txt(x, fy(0)+13, "A", 6.5, "#2b6ca3", "middle", "700")

# ============================== SECTION A-A ==================================
SX, SY = 1180, 56
def sx_(z): return SX + k(z)
def sy_(y): return SY + k(2600) - k(y)
txt(SX, SY-10, "SECTION A–A", 8, INK, "start", "700")
txt(SX+76, SY-10, "through the nook · 1:15", 6, NOTE)
rect(sx_(-200), sy_(2600), k(200), k(2600), GHOST, .6)
txt(sx_(-200), sy_(2600)-3, "200 concrete external wall", 4.8, NOTE)
line(sx_(-260), sy_(0), sx_(620), sy_(0), INK, 1.1)
line(sx_(-260), sy_(2600), sx_(560), sy_(2600), INK, 1.1)
for p in sorted(P, key=lambda q: -q["x"]):
    if not (p["x"] < 1450 < p["x"]+p["sx"]): continue
    rect(sx_(p["z"]), sy_(p["y"]+p["sy"]), k(p["sz"]), k(p["sy"]), FILL, .55)
# cushion
rect(sx_(12), sy_(470), k(466), k(90), "#d8d0c2", .55)
txt(sx_(250), sy_(430), "90 cushion", 4.8, NOTE, "middle")
for a,b,l in [(0,320,"320 shelf"),(320,430,"110"),(0,430,"430 base face"),(0,500,"500 bench")]:
    pass
hdim(sy_(0)+9,  sx_(0), sx_(320), "320 upper")
hdim(sy_(0)+17, sx_(0), sx_(430), "430 base + door")
hdim(sy_(0)+25, sx_(0), sx_(500), "500 bench — 70 proud")
vdim(sx_(-200)-9, sy_(0), sy_(2600), "2600")

# ============================== PLAN =========================================
_K[0] = KP
PX, PY = 52, 858
txt(PX, PY-10, "PLAN at +600", 8, INK, "start", "700")
txt(PX+72, PY-10, "scale 1:20 · upper carcass face dashed", 6, NOTE)
def px_(x): return PX + k(x)
def pz_(z): return PY + k(z)
rect(px_(-40), pz_(-200), k(2980), k(200), GHOST, .6)
txt(px_(-36), pz_(-200)+9, "200 concrete external wall  —  ends at x=600; closet carcass behind x 0–600", 5, NOTE)
rect(px_(0), pz_(-620), k(600), k(420), "#faf8f4", .5, "#8a8a8a")
txt(px_(300), pz_(-620)+11, "CLOSET (by others)", 5, NOTE, "middle")
txt(px_(300), pz_(-620)+20, "back-to-back, opens to door", 4.6, NOTE, "middle")
# base-level plan
for p in P:
    if p["defn"] in ("BaseSide","BaseBottom","Pier","BenchBottom","BenchMullion"):
        if p["y"] <= 600 <= p["y"]+p["sy"]:
            rect(px_(p["x"]), pz_(p["z"]), k(p["sx"]), k(p["sz"]), FILL, .55)
line(px_(0), pz_(430), px_(814), pz_(430), INK, .9)
line(px_(2086), pz_(430), px_(2900), pz_(430), INK, .9)
line(px_(850), pz_(500), px_(2050), pz_(500), INK, .9)
# upper footprint dashed
line(px_(0), pz_(320), px_(2900), pz_(320), "#2b6ca3", .6, "4 3")
txt(px_(2910), pz_(320)+2, "upper carcass face 320", 5, "#2b6ca3")
hdim(pz_(-640), px_(0), px_(600), "600 closet behind")
hdim(pz_(-740), px_(0), px_(2900), "2900")
vdim(px_(0)-10, pz_(0), pz_(500), "500")

# ============================== NOTES + TITLE BLOCK ==========================
NX, NY = 950, 800
txt(NX, NY-10, "CRITICAL NOTES", 8, INK, "start", "700")
notes = [
 "1.  ALL DIMENSIONS IN MILLIMETRES. Drawing is PROVISIONAL — 2900 and 2600 are",
 "     architect's plan dimensions, NOT site-measured. Before any cutting: measure the",
 "     opening width at floor / 900 / ceiling and the height at left / centre / right, take",
 "     both diagonals, and build to the SMALLEST reading. Surplus goes into the scribe.",
 "2.  HEADER. The 1200 span is the one part of this design that fails slowly and",
 "     permanently. 36mm flat (2×18 laminated) sags 9.8mm over time under a book load.",
 "     The 80mm fascia glued AND screwed to the front edge makes it an L-beam — 1.2mm.",
 "     Do not omit the fascia. Do not substitute a single 18mm deck.",
 "3.  BENCH DECK is 22mm over TWO mullions. 18mm over one mullion deflects 4.8mm",
 "     under an 80kg adult. Do not substitute 18mm.",
 "4.  PIERS are 2×18 laminated to 36mm, full height 100–2500, and carry the header",
 "     and the whole upper centre. Glue the full face, not just the edges.",
 "5.  No vertical panel lands on the wall/closet junction at x=600 — it falls inside",
 "     bay 2. The bookcase carcass is self-supporting; the closet is a separate box behind.",
 "6.  FIXING is into 200mm concrete: M8 sleeve or chemical anchors. Have the plumber",
 "     mark the 4\" drain stack on the wall before drilling. Anti-tip fixing is mandatory.",
 "7.  BACKS sit in a 4mm dado, not on cam fittings. Upper backs are VISIBLE inside the",
 "     open shelving — 10mm MDF, sprayed both faces.",
 "8.  NO EDGE BANDING. All MDF edges are sealed, filled and sprayed.",
 "9.  SCRIBE 15mm at the right-hand end against the wall. Left end is an exposed",
 "     finished return beside the door.",
 "10. Electrical: two sconces on the nook back and one socket — conduit MUST be run",
 "     before plaster. Positions to be set with the חשמלאי on site.",
]
for i,n in enumerate(notes):
    txt(NX, NY + 2 + i*8.4, n, 5.6, NOTE if not n[:3].strip().rstrip('.').isdigit() else NOTE)

TBX, TBY, TBW, TBH = W-50-330, H-34-62, 330, 62
rect(TBX, TBY, TBW, TBH, "none", 1.0)
line(TBX, TBY+17, TBX+TBW, TBY+17, INK, .7)
line(TBX+200, TBY, TBX+200, TBY+TBH, INK, .7)
txt(TBX+6, TBY+12, "MAIN-ROOM NOOK UNIT — יחידת ספרים עם גומחת ישיבה", 8, INK, "start", "700")
rows = [("UNITS","mm"),("SCALE","1:15 elev+sect, 1:20 plan @ A3"),("MATERIAL","MDF, sprayed — routed shaker fronts"),
        ("STATUS","PROVISIONAL — not site-measured"),("PARTS","99 pieces / 30 line items")]
for i,(a,b) in enumerate(rows):
    txt(TBX+6, TBY+29+i*8, a, 5.2, NOTE, "start", "600")
    txt(TBX+58, TBY+29+i*8, b, 5.2, INK)
txt(TBX+206, TBY+29, "DO NOT CUT FROM", 6.5, DIM, "start", "700")
txt(TBX+206, TBY+39, "THIS DRAWING UNTIL", 6.5, DIM, "start", "700")
txt(TBX+206, TBY+49, "THE WALL IS MEASURED", 6.5, DIM, "start", "700")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
       f'viewBox="0 0 {W:.0f} {H:.0f}"><rect width="{W:.0f}" height="{H:.0f}" fill="#fff"/>'
       + "".join(o) + "</svg>")
open("shopdrawing.svg","w",encoding="utf-8").write(svg)
print("sheet written", len(svg), "bytes")
