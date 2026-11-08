#!/usr/bin/env python3
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CL = json.load(open("cutlist_spec.json"))
F  = "Arial"
H  = Font(name=F, size=10, bold=True, color="FFFFFF")
B  = Font(name=F, size=10, bold=True)
N  = Font(name=F, size=10)
SM = Font(name=F, size=9, color="555555")
RED= Font(name=F, size=10, bold=True, color="C00000")
HD = PatternFill("solid", fgColor="3F3A33")
ALT= PatternFill("solid", fgColor="F2F0EC")
WRN= PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="D0CCC4")
BOX  = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook(); wb.remove(wb.active)

# ----------------------------------------------------------------- CUT LIST
ws = wb.create_sheet("Cut list  רשימת חיתוך")
ws.sheet_view.rightToLeft = False
ws["A1"] = "MAIN-ROOM NOOK UNIT  —  CUT LIST / רשימת חיתוך"; ws["A1"].font = Font(name=F, size=14, bold=True)
ws["A2"] = "PROVISIONAL — 2900 × 2600 are architect's plan dimensions, NOT site-measured. Do not cut until the wall is measured."
ws["A2"].font = RED
ws.merge_cells("A1:I1"); ws.merge_cells("A2:I2")
ws["A3"] = "All dimensions mm. Grain: none (MDF) — parts may be rotated freely for nesting. Banding: none — all MDF edges sealed, filled and sprayed."
ws["A3"].font = SM; ws.merge_cells("A3:I3")

cols = ["#", "Part / חלק", "Qty", "Length", "Width", "Thk", "Material", "Area m² (calc)", "Notes"]
for c, h in enumerate(cols, 1):
    cell = ws.cell(5, c, h); cell.font = H; cell.fill = HD; cell.border = BOX
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

mat_name = {m["id"]: m["name"] for m in CL["materials"]}
r = 6
first = r
for i, p in enumerate(CL["parts"], 1):
    th = next(m["thickness"] for m in CL["materials"] if m["id"] == p["material"])
    vals = [i, p["name"], p["qty"], p["length"], p["width"], th, mat_name[p["material"]], None, p["notes"]]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(r, c, v); cell.font = N; cell.border = BOX
        if c in (1, 3, 4, 5, 6): cell.alignment = Alignment(horizontal="center")
        if c in (2, 7, 9): cell.alignment = Alignment(vertical="center", wrap_text=True)
        if i % 2 == 0: cell.fill = ALT
    ws.cell(r, 8, f"=C{r}*D{r}*E{r}/1000000").number_format = "0.000"
    ws.cell(r, 8).font = N; ws.cell(r, 8).border = BOX
    if i % 2 == 0: ws.cell(r, 8).fill = ALT
    r += 1
last = r - 1
ws.cell(r, 2, "TOTAL").font = B
ws.cell(r, 3, f"=SUM(C{first}:C{last})").font = B
ws.cell(r, 8, f"=SUM(H{first}:H{last})").font = B
ws.cell(r, 8).number_format = "0.000"
ws.cell(r, 9, "pieces / m² of sheet face").font = SM
for col, w in zip("ABCDEFGHI", [5, 34, 6, 9, 8, 6, 34, 13, 62]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "A6"
ws.auto_filter.ref = f"A5:I{last}"

# ---------------------------------------------------------------- MATERIALS
ms = wb.create_sheet("Sheets  לוחות")
ms["A1"] = "SHEET TAKE-OFF / כמות לוחות"; ms["A1"].font = Font(name=F, size=14, bold=True)
ms["A2"] = ("Estimate only — a heuristic area total plus waste, NOT an optimised nesting plan. "
            "For the real cut plan run OpenCutList on the model or use CutList Optimizer.")
ms["A2"].font = RED; ms.merge_cells("A2:G2")
hdr = ["Material", "Sheet size", "Sheet m²", "Parts m² (from cut list)", "Waste factor", "Sheets needed", "Buy"]
for c, h in enumerate(hdr, 1):
    cell = ms.cell(4, c, h); cell.font = H; cell.fill = HD; cell.border = BOX
    cell.alignment = Alignment(horizontal="center", wrap_text=True)
rr = 5
cut_tab = "'Cut list  רשימת חיתוך'"
for m in CL["materials"]:
    used = any(p["material"] == m["id"] for p in CL["parts"])
    if not used: continue
    sh = m["sheet"]
    ms.cell(rr, 1, m["name"]).font = N
    ms.cell(rr, 2, f"{sh[0]} × {sh[1]}").font = N
    ms.cell(rr, 3, f"={sh[0]}*{sh[1]}/1000000").number_format = "0.000"
    ms.cell(rr, 4, f'=SUMIF({cut_tab}!$G${first}:$G${last},A{rr},{cut_tab}!$H${first}:$H${last})').number_format = "0.000"
    ms.cell(rr, 5, 1.30).number_format = "0%"
    ms.cell(rr, 6, f"=D{rr}*E{rr}/C{rr}").number_format = "0.00"
    ms.cell(rr, 7, f"=ROUNDUP(F{rr},0)").font = B
    for c in range(1, 8):
        ms.cell(rr, c).border = BOX
        if ms.cell(rr, c).font.name is None: ms.cell(rr, c).font = N
    rr += 1
ms.cell(rr, 1, "Waste factor is a 30% allowance on area. Confirm against the supplier's own nesting before ordering.").font = SM
for col, w in zip("ABCDEFG", [40, 14, 10, 22, 13, 14, 8]): ms.column_dimensions[col].width = w

# ---------------------------------------------------------------- HARDWARE
hs = wb.create_sheet("Hardware  פרזול")
hs["A1"] = "HARDWARE SCHEDULE / רשימת פרזול"; hs["A1"].font = Font(name=F, size=14, bold=True)
hs["A2"] = "Quantities derived from the spec. Confirm every clearance against the actual product datasheet before machining."
hs["A2"].font = SM; hs.merge_cells("A2:E2")
for c, h in enumerate(["Item / פריט", "Qty", "Spec", "Where", "Confidence"], 1):
    cell = hs.cell(4, c, h); cell.font = H; cell.fill = HD; cell.border = BOX
    cell.alignment = Alignment(horizontal="center", wrap_text=True)
HW = [
 ("ציר סמוי סגירה שקטה / Concealed soft-close hinge", 8, "35mm cup, full overlay, 2 per leaf (doors 589 high)", "4 base shaker doors", "high"),
 ("מסילות כדוריות סגירה שקטה 350 / Ball-bearing runner 350", 4, "side-mount, full extension, pair; box width = opening − 26", "4 skinny top drawers", "moderate — confirm clearance on the datasheet"),
 ("מסילות כדוריות סגירה שקטה 450 / Ball-bearing runner 450", 3, "side-mount, full extension, pair; box width = opening − 26", "3 bench drawers", "moderate — confirm clearance on the datasheet"),
 ("פין מדף Ø5 / Shelf pin Ø5", 80, "Ø5 × 10 deep, System 32 grid, front row 37 from front edge", "15 adjustable shelves + spares", "high"),
 ("מיניפיקס Ø15 + בורג Ø8×24 + פקק / Minifix cam + bolt + cap", 59, "Ø15 × 13.5 housing; Ø8 × 24 bolt", "carcass joints (from assembly plan)", "high"),
 ("דיבל עץ Ø8×30 / Fluted dowel Ø8×30", 30, "with PVA glue", "carcass alignment", "high"),
 ("רגל ארון מתכווננת 100 / Adjustable leg 100mm", 20, "100mm, levelling; clip-on plinth", "under every base + bench module", "high"),
 ("עוגן לבטון M8 / M8 concrete anchor", 14, "sleeve or chemical, into 200mm concrete", "wall fixing + anti-tip — MANDATORY", "high"),
 ("ידיות / Handles or knobs", 11, "client's choice — affects front machining", "4 doors + 4 skinny + 3 bench drawers", "OPEN — not yet chosen"),
 ("גופי תאורה בגומחה / Nook sconces", 2, "wall-mounted on the nook back, switched", "by חשמלאי — conduit before plaster", "OPEN — position to set on site"),
 ("שקע / Socket", 1, "in the nook or on the counter", "by חשמלאי — conduit before plaster", "OPEN — position to set on site"),
 ("סרט LED (אופציונלי) / LED strip (optional)", 1, "concealed behind the 80mm header fascia", "washes the nook back; needs a driver location", "OPTIONAL"),
]
for i, row in enumerate(HW):
    rw = 5 + i
    for c, v in enumerate(row, 1):
        cell = hs.cell(rw, c, v); cell.font = N; cell.border = BOX
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if i % 2 == 0: cell.fill = ALT
        if c == 2: cell.alignment = Alignment(horizontal="center")
        if c == 5 and ("OPEN" in str(v) or "OPTIONAL" in str(v)):
            cell.fill = WRN; cell.font = B
for col, w in zip("ABCDE", [46, 7, 50, 40, 36]): hs.column_dimensions[col].width = w

# ------------------------------------------------------- MEASUREMENT + NOTES
ns = wb.create_sheet("Measure first  מדידה")
ns["A1"] = "SITE MEASUREMENT — DO THIS BEFORE ANY CUTTING"; ns["A1"].font = Font(name=F, size=14, bold=True, color="C00000")
ns["A2"] = "Every number in this workbook came from the architect's plan. A plan dimension is an intention; a wall is a fact. Fill the yellow cells on site, then I will regenerate the whole package."
ns["A2"].font = N; ns.merge_cells("A2:E2"); ns.row_dimensions[2].height = 30
ns["A2"].alignment = Alignment(wrap_text=True, vertical="top")
for c, h in enumerate(["Measurement", "Plan value", "Measured", "Controlling", "Why it matters"], 1):
    cell = ns.cell(4, c, h); cell.font = H; cell.fill = HD; cell.border = BOX
    cell.alignment = Alignment(horizontal="center", wrap_text=True)
MEAS = [
 ("Width at floor", 2900, None, None, ""),
 ("Width at 900", 2900, None, None, ""),
 ("Width at ceiling", 2900, None, None, "Smallest of the three governs. Surplus goes into the right-hand scribe."),
 ("Height at left end", 2600, None, None, ""),
 ("Height at centre", 2600, None, None, ""),
 ("Height at right end", 2600, None, None, "Smallest governs. Crown absorbs the difference."),
 ("Diagonal 1", None, None, None, ""),
 ("Diagonal 2", None, None, None, "Unequal diagonals = out of square; grow the scribe allowance."),
 ("Floor slope across the run", None, None, None, "Decides whether the plinth is tapered."),
 ("Wall x=600: is it really where the concrete ends?", 600, None, None, "Sets where the closet carcass starts behind the run."),
 ("Depth available behind the left 600 for the closet", None, None, None, "Bookcase takes 430; the closet gets what is left. Needs ~600 to hang coats."),
 ("4\" drain stack — distance from the right-hand wall", None, None, None, "One anchor into it ruins the day. Have the plumber mark it."),
 ("Is 2600 finished floor to finished ceiling?", None, None, None, "A bulkhead, fan-coil or curtain pelmet changes the whole upper stack."),
 ("Does the right-hand end meet a wall, or is it open?", None, None, None, "Decides scribe vs finished return panel."),
]
for i, (a, b, c_, d, e) in enumerate(MEAS):
    rw = 5 + i
    ns.cell(rw, 1, a).font = N
    ns.cell(rw, 2, b).font = N
    ns.cell(rw, 3, c_).fill = WRN
    ns.cell(rw, 4, d).fill = WRN
    ns.cell(rw, 5, e).font = SM
    for cc in range(1, 6):
        ns.cell(rw, cc).border = BOX
        ns.cell(rw, cc).alignment = Alignment(wrap_text=True, vertical="center")
        if ns.cell(rw, cc).font.name is None: ns.cell(rw, cc).font = N
ns.cell(5 + len(MEAS) + 1, 1, "Yellow = fill these in on site.").font = B
for col, w in zip("ABCDE", [50, 12, 12, 13, 56]): ns.column_dimensions[col].width = w


# ------------------------------------------------------------------- COST
cs = wb.create_sheet("Cost  עלות")
cs["A1"] = "BUILD COST ESTIMATE / אומדן עלות"; cs["A1"].font = Font(name=F, size=14, bold=True)
cs["A2"] = ("Two independent methods. Sheet prices are real quotes; hardware is my estimate and must be priced; "
            "labour comes from a published Israeli benchmark. Every figure includes VAT.")
cs["A2"].font = SM; cs.merge_cells("A2:G2")

def hdr(row, cols, widths=None):
    for c, h in enumerate(cols, 1):
        cell = cs.cell(row, c, h); cell.font = H; cell.fill = HD; cell.border = BOX
        cell.alignment = Alignment(horizontal="center", wrap_text=True)

# --- A. sheet materials
cs["A4"] = "A · SHEET MATERIALS — confidence HIGH (quoted price list, 2440×1220 sheets)"
cs["A4"].font = B; cs.merge_cells("A4:G4")
hdr(5, ["Material", "Parts m²", "Sheet m²", "Waste", "Sheets", "₪/sheet", "₪ total"])
MATROWS = [("MDF 19mm — carcass, fronts, shelves", 15.994, 2.977, 1.30, 155),
           ("MDF 12mm — visible backs + shiplap",    4.851, 2.977, 1.30, 119),
           ("MDF 28mm — bench deck + furring",       0.857, 2.977, 1.30, 195),
           ("Hardboard 4mm — hidden backs",          1.178, 2.977, 1.15,  85),
           ("Birch ply 12mm — drawer boxes",         0.672, 2.977, 1.25, 178)]
r = 6
for nm, pm, sm, wf, pr in MATROWS:
    cs.cell(r,1,nm).font=N; cs.cell(r,2,pm).number_format="0.000"; cs.cell(r,3,sm).number_format="0.000"
    cs.cell(r,4,wf-1).number_format="0%"; cs.cell(r,5,f"=ROUNDUP(B{r}*(1+D{r})/C{r},0)")
    cs.cell(r,6,pr).number_format='₪#,##0'; cs.cell(r,7,f"=E{r}*F{r}").number_format='₪#,##0'
    for c in range(1,8): cs.cell(r,c).border=BOX
    for c in (2,3,4,5,6,7): cs.cell(r,c).font=N
    r += 1
MAT_FIRST, MAT_LAST = 6, r-1
cs.cell(r,1,"Sheet materials subtotal").font=B
cs.cell(r,7,f"=SUM(G{MAT_FIRST}:G{MAT_LAST})").font=B; cs.cell(r,7).number_format='₪#,##0'
MAT_TOT = r; r += 2

# --- B. hardware
cs.cell(r,1,"B · HARDWARE — confidence LOW. These are my estimates. Price them before you commit.").font=B
cs.cell(r,1).fill = WRN; cs.merge_cells(f"A{r}:G{r}"); r += 1
hdr(r, ["Item", "Qty", "", "", "", "₪ each", "₪ total"]); r += 1
HW_FIRST = r
for nm, q, pr in [("Concealed soft-close hinge, 35 cup", 8, 25),
                  ("Ball-bearing runner 350, pair (skinny drawers)", 4, 60),
                  ("Ball-bearing runner 450, pair (bench drawers)", 2, 85),
                  ("Brass knobs (doors) + bar pulls (drawers)", 11, 60),
                  ("Shelf pins Ø5 + spares", 40, 1.5),
                  ("Minifix cam + bolt + cap", 60, 2.5),
                  ("Fluted dowels Ø8×30", 40, 0.6),
                  ("Adjustable legs 100mm", 20, 8),
                  ("M8 concrete anchors + anti-tip", 14, 7),
                  ("LED strip, driver, aluminium profile", 1, 400),
                  ("Crown cove + plinth cap moulding (lin. m)", 7, 35)]:
    cs.cell(r,1,nm).font=N; cs.cell(r,2,q).alignment=Alignment(horizontal="center")
    cs.cell(r,6,pr).number_format='₪#,##0.00'; cs.cell(r,7,f"=B{r}*F{r}").number_format='₪#,##0'
    for c in range(1,8): cs.cell(r,c).border=BOX
    r += 1
HW_LAST = r-1
cs.cell(r,1,"Hardware subtotal").font=B
cs.cell(r,7,f"=SUM(G{HW_FIRST}:G{HW_LAST})").font=B; cs.cell(r,7).number_format='₪#,##0'
HW_TOT = r; r += 2

# --- C. the two methods
cs.cell(r,1,"C · THE TWO METHODS").font=B; cs.merge_cells(f"A{r}:G{r}"); r += 1
hdr(r, ["", "", "", "", "", "LOW", "HIGH"]); r += 1
cs.cell(r,1,"Method 1 — all-in benchmark: face area × ₪/m² for a custom MDF unit").font=N
cs.cell(r,2,7.54).number_format="0.00"; cs.cell(r,6,1500); cs.cell(r,7,2000)
M1R = r; r += 1
cs.cell(r,1,"   = face 7.54 m² × rate (this ALREADY includes materials, hardware, finish)").font=SM
cs.cell(r,6,f"=B{M1R}*F{M1R}").number_format='₪#,##0'
cs.cell(r,7,f"=B{M1R}*G{M1R}").number_format='₪#,##0'
M1 = r; r += 1
cs.cell(r,1,"   + complexity loading: laminated piers and header, 7 nosings, shiplap,").font=SM
cs.cell(r,6,0.15).number_format="0%"; cs.cell(r,7,0.25).number_format="0%"
LOADR = r; r += 1
cs.cell(r,1,"     mouldings, three depth planes, a sprayed finish. Not a plain wardrobe.").font=SM
cs.cell(r,6,f"=F{M1}*(1+F{LOADR})").number_format='₪#,##0'
cs.cell(r,7,f"=G{M1}*(1+G{LOADR})").number_format='₪#,##0'
for c in (6,7): cs.cell(r,c).font=B
M1TOT = r; r += 1
cs.cell(r,1,"Method 2 — bottom-up floor: materials + hardware only, no labour, no finish").font=N
cs.cell(r,6,f"=G{MAT_TOT}+G{HW_TOT}").number_format='₪#,##0'
cs.cell(r,7,f"=G{MAT_TOT}+G{HW_TOT}").number_format='₪#,##0'
M2 = r; r += 1
cs.cell(r,1,"   implied labour + spraying (method 1 minus method 2)").font=SM
cs.cell(r,6,f"=F{M1TOT}-F{M2}").number_format='₪#,##0'
cs.cell(r,7,f"=G{M1TOT}-G{M2}").number_format='₪#,##0'
r += 1
cs.cell(r,1,"   labour as a share of the total — sanity check, should be 60–75%").font=SM
cs.cell(r,6,f"=(F{M1TOT}-F{M2})/F{M1TOT}").number_format="0%"
cs.cell(r,7,f"=(G{M1TOT}-G{M2})/G{M1TOT}").number_format="0%"
r += 2

# --- D. outside the carpenter
cs.cell(r,1,"D · NOT IN THE נגר'S QUOTE").font=B; cs.merge_cells(f"A{r}:G{r}"); r += 1
D_FIRST = r
for nm, lo, hi in [("Electrician — drawer socket, LED feed, driver", 800, 1500),
                   ("Cushion — 90mm HR foam, washable cover, made up", 600, 1200),
                   ("Delivery and installation, if quoted separately", 0, 1500)]:
    cs.cell(r,1,nm).font=N
    cs.cell(r,6,lo).number_format='₪#,##0'; cs.cell(r,7,hi).number_format='₪#,##0'
    for c in range(1,8): cs.cell(r,c).border=BOX
    r += 1
D_LAST = r-1; r += 1
cs.cell(r,1,"ALL-IN RANGE").font=Font(name=F, size=13, bold=True)
cs.cell(r,6,f"=F{M1TOT}+SUM(F{D_FIRST}:F{D_LAST})").font=Font(name=F,size=13,bold=True,color="C00000")
cs.cell(r,7,f"=G{M1TOT}+SUM(G{D_FIRST}:G{D_LAST})").font=Font(name=F,size=13,bold=True,color="C00000")
for c in (6,7): cs.cell(r,c).number_format='₪#,##0'; cs.cell(r,c).fill=WRN
r += 2
for note in ["Sheet prices: woodcut.co.il materials list, 122×244 sheets, read 2026-11-08. Confidence HIGH for the price, MODERATE that your yard matches it.",
             "Labour benchmark: pro.co.il carpenter price list — custom MDF wall unit ₪1,500–2,000/m², incl. VAT. Confidence MODERATE.",
             "Hardware: my own estimates, not quoted. Confidence LOW. The brass handles alone swing ₪300–₪1,100 depending on what you buy.",
             "No Israeli per-m² price for MDF spray finishing was findable, so finishing sits inside the method-1 benchmark rather than as its own line.",
             "This is an estimate for budgeting, not a quote. Get three נגרים to price the actual cut list and compare against this."]:
    cs.cell(r,1,note).font=SM; cs.merge_cells(f"A{r}:G{r}"); r += 1
for col, w in zip("ABCDEFG", [62, 10, 10, 9, 9, 14, 14]): cs.column_dimensions[col].width = w

wb.save("Nook_unit_cutlist.xlsx")
print("workbook written")
