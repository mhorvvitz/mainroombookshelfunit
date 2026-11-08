#!/usr/bin/env python3
"""Three-page A3 drawing set, all geometry read from spec.json.
  1  Front elevation, keyed to a large dimension table
  2  Section A-A + plan
  3  Electrical: the service void, and why the socket moves
"""
import json
S = json.load(open("spec.json")); P = S["parts"]
MM = 3.7795
W, H = 420*MM, 297*MM

INK="#141414"; THIN="#565656"; DIM="#9c2b1b"; BLUE="#1d5f91"; GRN="#2f6b3f"
FILL="#e9e6df"; GHOST="#f2f0eb"; NOTE="#3d3d3d"; VOID="#fbe6c8"

class Sheet:
    def __init__(s, name): s.o=[]; s.name=name
    def rect(s,x,y,w,h,f=FILL,sw=.7,st=INK,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,.3):.1f}" height="{max(h,.3):.1f}" fill="{f}" stroke="{st}" stroke-width="{sw}"{d}/>')
    def line(s,x1,y1,x2,y2,c=THIN,sw=.6,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{sw}"{d}/>')
    def txt(s,x,y,t,sz=11,c=INK,a="start",w="400",mono=False):
        ff="'DejaVu Sans Mono',Consolas,monospace" if mono else "Helvetica,Arial,sans-serif"
        s.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" fill="{c}" text-anchor="{a}" font-weight="{w}" font-family="{ff}">{t}</text>')
    def circ(s,x,y,r,f="#fff",st=DIM,sw=1.1):
        s.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    def balloon(s,x,y,n):
        s.circ(x,y,9.5); s.txt(x,y+3.6,str(n),10,DIM,"middle","700")
    def hdim(s,y,x1,x2,lab,sz=9.5):
        s.line(x1,y,x2,y,DIM,.8)
        for x in (x1,x2): s.line(x,y-3.5,x,y+3.5,DIM,.8)
        s.txt((x1+x2)/2,y-4,lab,sz,DIM,"middle","600",True)
    def vdim(s,x,y1,y2,lab,sz=9.5):
        s.line(x,y1,x,y2,DIM,.8)
        for y in (y1,y2): s.line(x-3.5,y,x+3.5,y,DIM,.8)
        s.o.append(f'<text x="{x-4.5:.1f}" y="{(y1+y2)/2:.1f}" font-size="{sz}" fill="{DIM}" text-anchor="middle" font-weight="600" font-family="\'DejaVu Sans Mono\',monospace" transform="rotate(-90 {x-4.5:.1f} {(y1+y2)/2:.1f})">{lab}</text>')
    def title(s, sub, status="DRAFT — 13 decisions open · NOT site-measured"):
        s.line(40,H-56,W-40,H-56,INK,1.0)
        s.txt(40,H-38,"MAIN-ROOM NOOK UNIT",15,INK,"start","700")
        s.txt(40,H-22,sub,11,NOTE)
        s.txt(W-40,H-38,status,11,DIM,"end","700")
        s.txt(W-40,H-22,f"mm · A3 · sheet {s.name}",10,NOTE,"end","400",True)
    def svg(s):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
                f'viewBox="0 0 {W:.0f} {H:.0f}"><rect width="{W:.0f}" height="{H:.0f}" fill="#fff"/>'
                + "".join(s.o) + "</svg>")

FRONTS={"BaseDoor","BaseDrawerFront","BenchDrawerFront"}
BOXES={"BenchBoxSide","SkinnyBoxSide"}

# =========================================================== SHEET 1
s1=Sheet("1 of 3"); K=1/12.0
EX,EY=52,88
def fx(x): return EX+x*MM*K
def fy(y): return EY+(2600-y)*MM*K
s1.txt(EX,EY-16,"FRONT ELEVATION",15,INK,"start","700")
s1.txt(EX+168,EY-16,"1:13 — all dimensions keyed to the table on the right",10.5,NOTE)
s1.rect(fx(-60),fy(2600),60*MM*K,2600*MM*K,GHOST,.5)
s1.rect(fx(2900),fy(2600),60*MM*K,2600*MM*K,GHOST,.5)
s1.line(fx(-90),fy(2600),fx(2990),fy(2600),INK,1.3)
s1.line(fx(-90),fy(0),fx(2990),fy(0),INK,1.3)
for p in sorted(P,key=lambda q:q["z"]):
    if p["defn"] in BOXES: continue
    f="#fcfbf9" if p["defn"] in FRONTS else FILL
    s1.rect(fx(p["x"]),fy(p["y"]+p["sy"]),p["sx"]*MM*K,p["sy"]*MM*K,f,.5)
# balloons: vertical levels on the LEFT of the drawing, widths ACROSS the top
for n,y in [(1,50),(2,240),(3,990),(4,1640),(5,1706),(8,2500)]:
    s1.balloon(fx(-130),fy(y),n)
    s1.line(fx(-118),fy(y),fx(-8),fy(y),DIM,.5,"3 3")
s1.balloon(fx(205),fy(890),6); s1.balloon(fx(1450),fy(2099),7)
HPOS=[(9,9),(10,212),(11,416),(12,832),(13,1450)]
for n,x in HPOS: s1.balloon(fx(x),fy(0)+16,n)
s1.hdim(fy(0)+44,fx(0),fx(2900),"2900 OVERALL",11.5)
# ---- key table
TX,TY=fx(2900)+104,92
s1.txt(TX,TY-14,"DIMENSION KEY",13,INK,"start","700")
ROWS=[("H","HEIGHTS — from finished floor",None,None),
 (1,"Plinth","0 → 100","recessed 60, cap moulding on top"),
 (2,"Bench zone","100 → 380","two drawers; deck is 28mm"),
 (3,"Nook clear","380 → 1600","1220 high × 1200 wide, no divider"),
 (4,"Header fascia","1600 → 1680","80 downstand — the L-beam"),
 (5,"Header deck","1680 → 1716","36mm, 2×18 laminated"),
 (6,"Counter","881 → 900","19mm; the line runs right across"),
 (7,"Centre shelf","2081 → 2117","36mm + 40 nosing, full 1200 span"),
 (8,"Carcass top","2500","crown to 2600, scribed"),
 ("W","WIDTHS — left to right",None,None),
 (9,"End panel","18","exposed return beside the door"),
 (10,"Shelf column","389 × 4","15 shelves, all 386–389"),
 (11,"Inner divider","18 × 2",""),
 (12,"Nook pier","36 × 2","2×18 laminated, full height"),
 (13,"NOOK","1200","clear between piers"),
 ("D","DEPTHS — from the wall face",None,None),
 ("","Upper shelves","320","books read properly at this depth"),
 ("","Base + door","430","412 carcass + 19 shaker front"),
 ("","Bench deck","500","70 proud of the base run"),
 ("","Service void","30","behind the nook back — see sheet 3"),
]
y=TY+10
for a,b,c,d in ROWS:
    if c is None:
        y+=10
        s1.txt(TX,y,b,10.5,DIM,"start","700"); s1.line(TX,y+4,W-46,y+4,DIM,.7); y+=20; continue
    if a!="":
        s1.circ(TX+8,y-4,8.5); s1.txt(TX+8,y-0.6,str(a),9,DIM,"middle","700")
    s1.txt(TX+24,y,b,11,INK,"start","600")
    s1.txt(TX+168,y,str(c),11.5,DIM,"start","700",True)
    if d: s1.txt(TX+256,y,d,9.5,NOTE)
    y+=21
s1.txt(TX,y+14,"Build to the SMALLEST measured width and height, minus a 15–20 scribe",10.5,DIM,"start","700")
s1.txt(TX,y+29,"at the right-hand end. The 2900 and 2600 above are plan dimensions.",10.5,DIM,"start","700")
s1.title("Sheet 1 — front elevation + dimension key")

# =========================================================== SHEET 2
s2=Sheet("2 of 3"); K2=1/9.0
AX,AY=60,66
def sx2(z): return AX+z*MM*K2
def sy2(y): return AY+(2600-y)*MM*K2
s2.txt(AX,AY-16,"SECTION A–A",15,INK,"start","700")
s2.txt(AX+118,AY-16,"1:9 — cut through the centre of the nook, looking left",10.5,NOTE)
s2.rect(sx2(-200),sy2(2600),200*MM*K2,2600*MM*K2,GHOST,.6)
s2.txt(sx2(-196),sy2(2600)-6,"200 concrete external wall",9.5,NOTE)
s2.line(sx2(-260),sy2(0),sx2(640),sy2(0),INK,1.3)
s2.line(sx2(-260),sy2(2600),sx2(560),sy2(2600),INK,1.3)
for p in sorted(P,key=lambda q:-q["x"]):
    if not (p["x"] < 1450 < p["x"]+p["sx"]): continue
    f = VOID if p["defn"]=="NookFurring" else FILL
    s2.rect(sx2(p["z"]),sy2(p["y"]+p["sy"]),p["sz"]*MM*K2,p["sy"]*MM*K2,f,.55)
s2.rect(sx2(12),sy2(470),466*MM*K2,90*MM*K2,"#ded5c6",.55)
s2.txt(sx2(490),sy2(430),"90 cushion",10,NOTE)
for lab,z,off in [("320 upper shelf",320,26),("430 base + door",430,46),("500 bench deck",500,66)]:
    s2.hdim(sy2(0)+off,sx2(0),sx2(z),lab,10)
s2.vdim(sx2(-200)-18,sy2(0),sy2(2600),"2600",11)
for y,l in [(380,"380 deck"),(900,"900 counter"),(1600,"1600 fascia u/s"),(1716,"1716 header"),(2500,"2500 top")]:
    s2.line(sx2(500),sy2(y),sx2(640),sy2(y),THIN,.5,"3 3")
    s2.txt(sx2(646),sy2(y)+4,l,10,NOTE,"start","600",True)
# plan
PX,PY=760,80; K3=1/9.0
def px3(x): return PX+x*MM*K3
def pz3(z): return PY+z*MM*K3
s2.txt(PX,PY-16,"PLAN at +600",15,INK,"start","700")
s2.txt(PX+108,PY-16,"1:9 — base level; upper carcass face dashed",10.5,NOTE)
s2.rect(px3(600),pz3(-200),2320*MM*K3,200*MM*K3,GHOST,.6)
s2.txt(px3(610),pz3(-200)+13,"200 concrete — ends at x=600",9.5,NOTE)
s2.rect(px3(-20),pz3(-620),640*MM*K3,420*MM*K3,"#fbf9f5",.6,"#7d7d7d","4 3")
s2.txt(px3(300),pz3(-620)+16,"CLOSET (by others)",10,NOTE,"middle","600")
s2.txt(px3(300),pz3(-620)+30,"back-to-back, opens to the door",9,NOTE,"middle")
for p in P:
    if p["defn"] in ("BaseSide","BaseBottom","Pier","BenchBottom","BenchMullion") and p["y"]<=600<=p["y"]+p["sy"]:
        s2.rect(px3(p["x"]),pz3(p["z"]),p["sx"]*MM*K3,p["sz"]*MM*K3,FILL,.55)
s2.line(px3(0),pz3(430),px3(814),pz3(430),INK,1.0)
s2.line(px3(2086),pz3(430),px3(2900),pz3(430),INK,1.0)
s2.line(px3(850),pz3(500),px3(2050),pz3(500),INK,1.0)
s2.line(px3(0),pz3(320),px3(2900),pz3(320),BLUE,.8,"5 3")
s2.txt(px3(0),pz3(320)-6,"upper carcass face 320",9.5,BLUE)
s2.hdim(pz3(-760),px3(0),px3(600),"600 closet behind",10)
s2.hdim(pz3(-900),px3(0),px3(2900),"2900",11)
s2.title("Sheet 2 — section + plan")

# =========================================================== SHEET 3
s3=Sheet("3 of 3")
s3.txt(52,50,"ELECTRICAL — WHY THE SOCKET MOVES",15,INK,"start","700")
s3.txt(52,70,"Your existing outlet is low and central, so it lands directly behind the bench drawers. A live box may not be buried behind fixed joinery with no access.",11,NOTE)
s3.txt(52,86,"Instead of chasing three new boxes into 200mm concrete, the nook back is held 30mm off the wall. That gap is the chase. Everything wires inside it.",11,NOTE)

def panel(x,y,w,h,letter,ttl,scale):
    s3.rect(x,y,w,h,"#fff",.8,"#c9c5bd")
    s3.circ(x+16,y+16,11,"#fff",INK,1.1); s3.txt(x+16,y+20,letter,11,INK,"middle","700")
    s3.txt(x+34,y+21,ttl,12,INK,"start","700"); s3.txt(x+w-10,y+21,scale,10,NOTE,"end","400",True)

# ---------- A : nook back seen from the room, 1:12
AX,AY,AW,AH=52,112,430,582
panel(AX,AY,AW,AH,"A","NOOK BACK, seen from the room","1:12")
KA=1/12.0; ox,oy=AX+96,AY+72
def ax_(x): return ox+(x-850)*MM*KA
def ay_(y): return oy+(1680-y)*MM*KA
s3.rect(ax_(850),ay_(1680),1200*MM*KA,1300*MM*KA,FILL,.9)
for i in range(7):
    s3.rect(ax_(850+i*(1200-70)/6),ay_(1680),70*MM*KA,1300*MM*KA,"#e1ddd4",.4)
s3.rect(ax_(850),ay_(380),1200*MM*KA,7,"#d8cfc0",.8)
s3.txt(ax_(1450),ay_(380)+19,"bench deck  +380",9.5,NOTE,"middle","600")
s3.txt(ax_(1450),ay_(1680)-8,"header fascia u/s  +1600",9.5,NOTE,"middle","600")
def dev(x,y,w,h,lab,c):
    s3.rect(ax_(x),ay_(y+h),w*MM*KA,h*MM*KA,"#fff",1.4,c)
    s3.txt(ax_(x)+w*MM*KA/2,ay_(y+h)-6,lab,9,c,"middle","700")
dev(1140,960,86,86,"SOCKET",GRN)
dev(1060,1200,110,90,"SCONCE",BLUE); dev(1730,1200,110,90,"SCONCE",BLUE)
s3.vdim(ax_(850)-20,ay_(1000),ay_(380),"1000",10)
s3.vdim(ax_(850)-54,ay_(1250),ay_(380),"1250",10)
s3.hdim(ay_(380)+48,ax_(1115),ax_(1785),"670 between sconce centres",9.5)
s3.txt(AX+12,AY+AH-30,"Heights from finished floor. Final positions are the חשמלאי's call —",9.5,NOTE)
s3.txt(AX+12,AY+AH-16,"cut the boxes in the back panel AFTER he marks them on site.",9.5,NOTE)

# ---------- B : horizontal section through the back build-up, 1:1
BX,BY,BW,BH=504,112,540,250
panel(BX,BY,BW,BH,"B","HORIZONTAL SECTION through the nook back","1:2")
KB=0.5; bz=BX+150; bt,bb=BY+58,BY+168
def hz(z): return bz+z*MM*KB
s3.rect(hz(-50),bt,50*MM,bb-bt,GHOST,.9)
s3.rect(hz(0),bt,30*MM,bb-bt,VOID,1.3,DIM)
s3.rect(hz(30),bt,18*MM,bb-bt,FILL,.9)
s3.rect(hz(48),bt+22,12*MM,bb-bt-44,"#e1ddd4",.9)
s3.circ(hz(15),(bt+bb)/2,13,"#fff",DIM,1.4)
s3.txt(hz(15),(bt+bb)/2+4,"C",10,DIM,"middle","700")
for z,lab,c in [(-25,"concrete",NOTE),(15,"30 VOID",DIM),(39,"18 back",NOTE),(54,"12 batten",NOTE)]:
    s3.txt(hz(z),bb+16,lab,9.5,c,"middle","700" if c==DIM else "600")
s3.txt(hz(15),bb+30,"conduit runs here",9,DIM,"middle")
s3.txt(BX+290,BY+70,"A 45-wide furring strip every ~300 holds the",10,NOTE)
s3.txt(BX+290,BY+86,"back panel off the concrete. The gaps between",10,NOTE)
s3.txt(BX+290,BY+102,"them are the chase.",10,NOTE)
s3.txt(BX+290,BY+126,"Nothing is cut into the wall: no dust, no rebar,",10,NOTE)
s3.txt(BX+290,BY+142,"no risk to the 4\" drain stack.",10,NOTE)
s3.txt(BX+290,BY+170,"Cost of the whole change:",10,GRN,"start","700")
s3.txt(BX+290,BY+186,"five strips of 30mm MDF.",10,GRN,"start","700")

# ---------- C : vertical route, 1:12
CX,CY,CW,CH=504,386,540,568
panel(CX,CY,CW,CH,"C","VERTICAL ROUTE — existing box to the new outlets","1:14")
KC=1/14.0; cl=CX+92; cb=CY+CH-30
def cy_(y): return cb-y*MM*KC
s3.rect(cl-30,cy_(1750),30,1750*MM*KC,GHOST,.8)
s3.txt(cl-34,cy_(1790),"concrete",9,NOTE,"end","600")
s3.rect(cl,cy_(1680),30*MM*KC,(1680-380)*MM*KC,VOID,1.2,DIM)
s3.rect(cl,cy_(388),140,8,"#d8cfc0",.9)
s3.rect(cl,cy_(366),140,(366-118)*MM*KC,"#fff",.9)
s3.rect(cl-5,cy_(330),22,14,"#fff",1.5,"#8c3b2e")
s3.line(cl+5,cy_(316),cl+5,cy_(1260),DIM,2.2,"5 3")
for yy,lab,c in [(1000,"new socket",GRN),(1250,"sconce feed",BLUE)]:
    s3.rect(cl+1,cy_(yy+30),16,11,"#fff",1.4,c)
    s3.txt(cl+24,cy_(yy)+2,lab,9.5,c,"start","700")
s3.txt(cl+152,cy_(392)+4,"bench deck — ONE Ø30 hole at the rear",9.5,NOTE,"start","600")
s3.txt(cl+152,cy_(250)+4,"bench drawer — pull it out and the old",9.5,NOTE,"start","600")
s3.txt(cl+152,cy_(250)+17,"box is in reach. That is the access.",9.5,NOTE,"start","600")
s3.txt(cl+24,cy_(330)+4,"EXISTING BOX — stays where it is,",9.5,"#8c3b2e","start","700")
s3.txt(cl+24,cy_(330)+17,"live, as an accessible junction",9.5,"#8c3b2e","start","700")
s3.txt(cl+152,cy_(1100)+4,"30 service void",9.5,DIM,"start","700")

# ---------- notes column
NX2,NY2=1076,132
s3.txt(NX2,NY2,"WHAT THE ELECTRICIAN ACTUALLY DOES",12,INK,"start","700")
s3.line(NX2,NY2+7,W-46,NY2+7,INK,.8)
steps=[("1","Leaves the existing box exactly where it is, live, as a junction. It ends up behind the centre bench drawer, which pulls out — that satisfies the access requirement."),
 ("2","Drills one Ø30 hole through the rear of the bench deck, in line with the void."),
 ("3","Runs flexible conduit up inside the 30mm void to a new socket at 1000 and two sconce boxes at 1250."),
 ("4","Nothing is chased into the concrete. No core drilling, no rebar scanning, no risk to the 4\" drain stack in this wall."),
 ("5","Marks the three box positions on the back panel before it is sprayed. The נגר cuts them, not the electrician.")]
yy=NY2+28
for n,t in steps:
    s3.circ(NX2+9,yy-4,9.5,"#fff",BLUE,1.2); s3.txt(NX2+9,yy-0.5,n,9.5,BLUE,"middle","700")
    words=t.split(); line=""; ly=yy
    for wd in words:
        if len(line)+len(wd)+1 > 62: s3.txt(NX2+26,ly,line,10.5,NOTE); line=wd; ly+=15
        else: line = (line+" "+wd).strip()
    s3.txt(NX2+26,ly,line,10.5,NOTE); yy = ly+30
s3.txt(NX2,yy+8,"SEQUENCE MATTERS",12,INK,"start","700")
s3.line(NX2,yy+15,W-46,yy+15,INK,.8)
s3.txt(NX2,yy+36,"Conduit and boxes go in while the nook back is off. Once the",10.5,DIM)
s3.txt(NX2,yy+51,"battens are glued on and the unit is sprayed, changing a box",10.5,DIM)
s3.txt(NX2,yy+66,"position means taking the back panel out again.",10.5,DIM)
s3.txt(NX2,yy+92,"STILL UNKNOWN: the exact height and offset of your existing",10.5,"#8c3b2e","start","700")
s3.txt(NX2,yy+107,"outlet. Measure it and I will put it on the drawing properly.",10.5,"#8c3b2e","start","700")
s3.title("Sheet 3 — electrical")

for sh,fn in ((s1,"sheet1.svg"),(s2,"sheet2.svg"),(s3,"sheet3.svg")):
    open(fn,"w",encoding="utf-8").write(sh.svg())
pages="".join(f'<div class="pg">{open(f,encoding="utf-8").read()}</div>' for f in ("sheet1.svg","sheet2.svg","sheet3.svg"))
open("set_print.html","w",encoding="utf-8").write(
 '<!doctype html><html><head><meta charset="utf-8"><style>@page{size:420mm 297mm;margin:0}'
 'html,body{margin:0;padding:0}.pg{width:420mm;height:297mm;page-break-after:always;overflow:hidden}'
 '.pg:last-child{page-break-after:auto}svg{display:block;width:420mm;height:297mm}</style></head><body>'
 +pages+'</body></html>')
print("3 sheets written")
