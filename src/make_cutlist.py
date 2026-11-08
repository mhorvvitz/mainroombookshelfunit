#!/usr/bin/env python3
"""Convert the positioned spec into cutlist.py's schema, with real Israeli
sheet stock, bilingual part names, and per-part notes."""
import json, sys, os, subprocess
SKILL = "/root/.claude/skills/synced/50b1bd87-06ff-4b00-829c-fb046f957e69_776f7a00-b6d1-4357-825f-9f68130378de/furniture-design"
sys.path.insert(0, os.path.join(SKILL, "scripts"))

BIG = [2800, 2070]; SML = [2440, 1220]
MATERIALS = [
  {"id":"mdf18","name":"MDF 18mm / MDF 18 מ\"מ — גוף","thickness":18,"sheet":BIG,"kerf":4,"trim":10},
  {"id":"mdf19","name":"MDF 19mm / MDF 19 — חזיתות שייקר + משטח","thickness":19,"sheet":BIG,"kerf":4,"trim":10},
  {"id":"mdf30","name":"MDF 30mm / MDF 30 — סרגלי פילוס לחלל שירות","thickness":30,"sheet":BIG,"kerf":4,"trim":10},
  {"id":"mdf22","name":"MDF 22mm / MDF 22 — משטח ישיבה","thickness":22,"sheet":BIG,"kerf":4,"trim":10},
  {"id":"mdf12","name":"MDF 12mm / MDF 12 — סרגלי גומחה","thickness":12,"sheet":SML,"kerf":3,"trim":10},
  {"id":"mdf10","name":"MDF 10mm / MDF 10 — גבים גלויים","thickness":10,"sheet":BIG,"kerf":3,"trim":10},
  {"id":"hb4",  "name":"Hardboard 4mm / מזונית 4 — גבים נסתרים","thickness":4,"sheet":SML,"kerf":3,"trim":10},
  {"id":"ply15","name":"Birch ply 15mm / דיקט בירץ' 15 — ארגזי מגירה","thickness":15,"sheet":SML,"kerf":3,"trim":10},
  {"id":"ply12","name":"Birch ply 12mm / דיקט בירץ' 12 — ארגזי מגירה דקה","thickness":12,"sheet":SML,"kerf":3,"trim":10},
]
MATFOR = {("mdf",30):"mdf30",("mdf",18):"mdf18",("mdf",19):"mdf19",("mdf",22):"mdf22",("mdf",12):"mdf12",
          ("mdf",10):"mdf10",("mdf",20):"mdf19",("hardboard",4):"hb4",
          ("plywood_birch",15):"ply15",("plywood_birch",12):"ply12"}
# the counter is 19mm MDF
MATFOR[("mdf",19)] = "mdf19"

HE = {
 "Pier":"עמוד גומחה / Nook pier","BaseSide":"צד ארון תחתון / Base side",
 "BaseBottom":"תחתית ארון תחתון / Base bottom","BaseTop":"עליונית ארון תחתון / Base top",
 "BaseBack":"גב ארון תחתון / Base back","BaseDoor":"דלת שייקר / Shaker door",
 "BaseDrawerFront":"חזית מגירה דקה / Skinny drawer front","Counter":"משטח / Counter",
 "BenchBottom":"תחתית ספסל / Bench bottom","BenchPlatform":"משטח ישיבה / Bench deck",
 "BenchMullion":"מחיצת ספסל / Bench mullion","BenchDrawerFront":"חזית מגירת ספסל / Bench drawer front",
 "BenchBoxSide":"צד ארגז מגירה / Drawer box side","SkinnyBoxSide":"צד ארגז מגירה דקה / Skinny box side",
 "NookBack":"גב הגומחה / Nook back","NookBatten":"סרגל גומחה / Nook batten","NookFurring":"סרגל פילוס / Furring strip",
 "Header":"קורת ראש / Header leaf","HeaderFascia":"חזית הקורה / Header fascia",
 "UpperSide":"צד ארון עליון / Upper side","UpperTop":"עליונית ארון עליון / Upper top",
 "UpperBack":"גב ארון עליון / Upper back","UpperDivider":"מחיצה עליונה / Upper divider",
 "Shelf":"מדף / Shelf","PlinthBase":"סוקל / Plinth","PlinthBench":"סוקל ספסל / Bench plinth",
 "CrownFascia":"כרכוב / Crown fascia",
}
NOTE = {
 "Pier":"2 leaves laminated to 36mm per pier; full height 100-2500; carries the header",
 "Header":"2 leaves laminated to 36mm; glue+screw the fascia on to form the L-beam",
 "HeaderFascia":"2 leaves laminated to 36mm; 80 downstand — this is what stops the header sagging",
 "BenchPlatform":"22mm over two mullions; do NOT substitute 18mm",
 "UpperSide":"System 32: two rows of 5mm holes, front row 37 from the front edge",
 "Pier_":"",
 "Shelf":"adjustable on 5mm pins; 298 deep leaves a 22 front setback",
 "UpperBack":"VISIBLE inside open shelving — sprayed both faces",
 "BaseBack":"hidden behind doors — one face only",
 "CrownFascia":"two lengths, scarf joint on the left pier centreline (x=832); scribe to ceiling",
 "NookBatten":"7 off at 189 centres; glue to the nook back before spraying",
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

out = {"project": "Horvitz main-room nook unit — PROVISIONAL (plan dims, not site-measured)",
       "units": "mm", "materials": MATERIALS, "parts": parts,
       "checks": {"overall": {"width": 2900, "height": 2600, "depth": 500}}}
json.dump(out, open("cutlist_spec.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(parts)} line items, {sum(p['qty'] for p in parts)} pieces")
