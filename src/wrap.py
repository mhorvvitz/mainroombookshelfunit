svg = open("shopdrawing.svg", encoding="utf-8").read()
open("sheet_print.html","w",encoding="utf-8").write(
 '<!doctype html><html><head><meta charset="utf-8"><style>'
 '@page{size:420mm 297mm;margin:0}html,body{margin:0;padding:0}'
 'svg{display:block;width:420mm;height:297mm}</style></head><body>'+svg+'</body></html>')
