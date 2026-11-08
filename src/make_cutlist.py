#!/usr/bin/env python3
"""Convert the positioned spec into cutlist.py's schema, with real Israeli
sheet stock, bilingual part names, and per-part notes."""
import json, sys, os, subprocess
SKILL = "/root/.claude/skills/synced/50b1bd87-06ff-4b00-829c-fb046f957e69_776f7a00-b6d1-4357-825f-9f68130378de/furniture-design"
sys.path.insert(0, os.path.join(SKILL, "scripts"))

BIG = [2800, 2070]; SML = [2440, 1220]
MATERIALS = [
  {"id":"mdf19","name":"MDF 19mm / MDF 19 — גוף, חזיתות שייקר, מדפים","thickness":19,"sheet":SML,"kerf":4,"trim":10},
  {"id":"mdf28","name":"MDF 28mm / MDF 28 — משטח ישיבה + סרגלי פילוס","thickness":28,"sheet":SML,"kerf":4,"trim":10},
  {"id":"mdf12","name":"MDF 12mm / MDF 12 — גבים גלויים + שיפלאפ","thickness":12,"sheet":SML,"kerf":3,"trim":10},
  {"id":"hb4",  "name":"Hardboard 4mm / מזונית 4 — גבים נסתרים","thickness":4,"sheet":SML,"kerf":3,"trim":10},
  {"id":"ply12","name":"Birch ply 12mm / דיקט בירץ' 12 — ארגזי מגירה","thickness":12,"sheet":SML,"kerf":3,"trim":10},
]
MATFOR = {("mdf",19):"mdf19",("mdf",28):"mdf28",("mdf",12):"mdf12",
          ("hardboard",4):"hb4",("plywood_birch",12):"ply12"}
# the counter is 19mm MDF
pass  # every panel is now a stocked thickness

HE = {
 "Pier":"עמוד גומחה / Nook pier","BaseSide":"צד ארון תחתון / Base side",
 "BaseBottom":"תחתית ארון תחתון / Base bottom","BaseTop":"עליונית ארון תחתון / Base top",
 "BaseBack":"גב ארון תחתון / Base back","BaseDoor":"דלת שייקר / Shaker door",
 "BaseDrawerFront":"חזית מגירה דקה / Skinny drawer front","Counter":"משטח / Counter",
 "BenchBottom":"תחתית ספסל / Bench bottom","BenchPlatform":"משטח ישיבה / Bench deck",
 "BenchMullion":"מחיצת ספסל / Bench mullion","BenchDrawerFront":"חזית מגירת ספסל / Bench drawer front",
 "BenchBoxSide":"צד ארגז מגירה / Drawer box side","SkinnyBoxSide":"צד ארגז מגירה דקה / Skinny box side",
 "NookBack":"גב הגומחה / Nook back","ShiplapBoard":"לוח שיפלאפ / Shiplap board","NookFurring":"סרגל פילוס / Furring strip",
 "Header":"קורת ראש / Header leaf","HeaderFascia":"חזית הקורה / Header fascia",
 "UpperSide":"צד ארון עליון / Upper side","UpperTop":"עליונית ארון עליון / Upper top",
 "UpperBack":"גב ארון עליון / Upper back","UpperDivider":"מחיצה עליונה / Upper divider",
 "Shelf":"מדף / Shelf","ShelfWide":"מדף מרכזי רחב / Wide centre shelf","ShelfNosing":"חזית מדף / Shelf nosing","ShelfWideNosing":"חזית מדף מרכזי / Centre shelf nosing","PlinthBase":"סוקל / Plinth","PlinthBench":"סוקל ספסל / Bench plinth",
 "CrownFascia":"כרכוב / Crown fascia",
}
NOTE = {
 "Pier":"2 leaves laminated to 36mm per pier; full height 100-2500; carries the header",
 "Header":"2 leaves laminated to 36mm; glue+screw the fascia on to form the L-beam",
 "HeaderFascia":"2 leaves laminated to 36mm; 80 downstand — this is what stops the header sagging",
 "BenchPlatform":"28mm over ONE mullion (two drawers). 22mm gives 2.63mm under 80kg — do not substitute",
 "NookBack":"ground panel for the shiplap; no socket cutout — the socket is in a bench drawer",
 "ShelfWide":"2 leaves laminated to 36mm; spans the full 1200, no divider",
 "ShelfNosing":"52 deep, glued+screwed under the shelf front edge -> 70mm visible band. WITHOUT it an 18mm shelf at 796 sags 6.2mm",
 "ShelfWideNosing":"34 deep under the 36mm centre deck -> the same 70mm band",
 "ShelfWide":"2 leaves laminated to 36mm; spans the full 1200 with no divider",
 "HeaderFascia":"64 below a 36 deck = 100mm band. Carries the opening AND hides the LED strip",
 "UpperSide":"System 32: two rows of 5mm holes, front row 37 from the front edge",
 "Pier_":"",
 "Shelf":"adjustable on 5mm pins; 298 deep leaves a 22 front setback",
 "UpperBack":"VISIBLE inside open shelving — sprayed both faces",
 "BaseBack":"hidden behind doors — one face only",
 "CrownFascia":"two lengths, scarf joint on the left pier centreline (x=832); scribe to ceiling",
 "ShiplapBoard":"9 boards, 6mm shadow gap; glue to the ground panel before spraying",
 "BaseDoor":"routed shaker, 19mm; 2 concealed soft-close hinges per leaf",
 "BaseSide":"System 32 both rows",
 "NookFurring":"5 off; creates the 30mm SERVICE VOID — socket + sconce wiring runs here, no chasing the concrete",
 "NookBack":"cut the socket box and 2 sconce boxes on site AFTER the electrician sets positions",
}

spec = json.load(open("spec.json"))
groups = {}
for p in spec["parts"]:
    if p.get("kind") == "rod": continue
    dims = sorted([p["sx"], p["sy"], p["sz"]])
    th, w, L = round(dims[0]), round(dims[1]), round(dims[2])
    mid = MATFOR.get((p["material"], th))
    if mid is None:
        print(f"!! no stock material for {p['defn']} {p['material']} {th}mm"); sys.exit(1)
    key = (p["defn"], L, w, mid)
    groups[key] = groups.get(key, 0) + 1

parts = []
for (defn, L, w, mid), qty in sorted(groups.items(), key=lambda kv: (-kv[0][1], kv[0][0])):
    parts.append({"name": HE.get(defn, defn), "qty": qty, "length": L, "width": w,
                  "material": mid, "grain": "none", "banding": [],
                  "notes": NOTE.get(defn, "")})

out = {"project": "Horvitz main-room nook unit v1.0 — design locked, NOT site-measured",
       "units": "mm", "materials": MATERIALS, "parts": parts,
       "checks": {"overall": {"width": 2900, "height": 2600, "depth": 501}}}
json.dump(out, open("cutlist_spec.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(parts)} line items, {sum(p['qty'] for p in parts)} pieces")
