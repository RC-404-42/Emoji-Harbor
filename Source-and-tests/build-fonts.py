import json, pathlib, copy, io, sys
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import newTable, TTFont
from fontTools.ttLib.tables import C_B_D_T_, E_B_L_C_
from fontTools.ttLib.tables.BitmapGlyphMetrics import SmallGlyphMetrics

ROOT=pathlib.Path('emoji-atelier-work/assets')
OUT=pathlib.Path('emoji-harbor-src'); (OUT/'fonts').mkdir(exist_ok=True)
data=json.loads((ROOT/'catalog.json').read_text()); records=data['records']; aliases=data['aliases']
allcp=sorted({ord(c) for s in aliases for c in s})
single={ord(r['emoji']):i for i,r in enumerate(records) if len(r['emoji'])==1}
cpnames={cp:(f'e{single[cp]:04d}' if cp in single else f'u{cp:X}') for cp in allcp}
order=['.notdef']+list(dict.fromkeys(cpnames.values()))+[f'e{i:04d}' for i in range(len(records)) if i not in single.values()]
ids={r['key']:f'e{i:04d}' for i,r in enumerate(records)}
fb=FontBuilder(1024,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(cpnames)
empty=TTGlyphPen(None).glyph();fb.setupGlyf({n:empty for n in order})
fb.setupHorizontalMetrics({n:(1024 if n.startswith('e') or n=='.notdef' else 0,0) for n in order})
fb.setupHorizontalHeader(ascent=880,descent=-144,lineGap=0)
fb.setupNameTable({'familyName':'Harbor Color','styleName':'Regular','uniqueFontIdentifier':'Harbor Color 1.0','fullName':'Harbor Color','psName':'HarborColor','version':'Version 1.000'})
fb.setupOS2(sTypoAscender=880,sTypoDescender=-144,sTypoLineGap=0,usWinAscent=880,usWinDescent=144)
fb.setupPost();fb.setupMaxp()
rules=[]
for text,key in sorted(aliases.items(), key=lambda kv:-len(kv[0])):
 if len(text)>1 or cpnames[ord(text)]!=ids[key]: rules.append('sub '+' '.join(cpnames[ord(c)] for c in text)+' by '+ids[key]+';')
fea='languagesystem DFLT dflt;\nfeature rlig {\n'+'\n'.join(rules)+'\n} rlig;'
addOpenTypeFeaturesFromString(fb.font,fea)
for style in (sys.argv[1:] or ['noto','apple','twemoji']):
 font=copy.deepcopy(fb.font)
 for name_id,value in [(1,'Harbor '+style.title()),(3,'Harbor '+style.title()+' 1.0'),(4,'Harbor '+style.title()),(6,'Harbor'+style.title())]:
  for platform,encoding,lang in [(1,0,0),(3,1,0x409)]:font['name'].setName(value,name_id,platform,encoding,lang)
 cbdt=newTable('CBDT');cbdt.version=3.0;cbdt.strikeData=[]
 cblc=newTable('CBLC');cblc.version=3.0;cblc.strikes=[]
 strike=E_B_L_C_.Strike();bst=strike.bitmapSizeTable
 bst.colorRef=0;bst.ppemX=64;bst.ppemY=64;bst.bitDepth=32;bst.flags=1
 for axis in ['hori','vert']:
  lm=E_B_L_C_.SbitLineMetrics()
  for k in ['ascender','descender','widthMax','caretSlopeNumerator','caretSlopeDenominator','caretOffset','minOriginSB','minAdvanceSB','maxBeforeBL','minAfterBL','pad1','pad2']:setattr(lm,k,0)
  lm.ascender=55;lm.descender=-9;lm.widthMax=64;lm.caretSlopeNumerator=1
  setattr(bst,axis,lm)
 bitmaps={}
 for i,r in enumerate(records):
  glyph=C_B_D_T_.cbdt_bitmap_format_17(None,None)
  metrics=SmallGlyphMetrics();metrics.height=64;metrics.width=64;metrics.BearingX=0;metrics.BearingY=55;metrics.Advance=64
  glyph.metrics=metrics;glyph.imageData=(ROOT/(style+'-ready')/(r['key']+'.png')).read_bytes();bitmaps[f'e{i:04d}']=glyph
 sub=E_B_L_C_.eblc_index_sub_table_1(None,None);sub.indexFormat=1;sub.imageFormat=17;sub.imageDataOffset=0
 sub.names=sorted(bitmaps,key=font.getGlyphID);sub.firstGlyphIndex=font.getGlyphID(sub.names[0]);sub.lastGlyphIndex=font.getGlyphID(sub.names[-1])
 strike.indexSubTables=[sub];cblc.strikes=[strike];cbdt.strikeData=[bitmaps]
 font['CBDT']=cbdt;font['CBLC']=cblc
 # Bitmap-only sfnt, matching the structure used by CBDT emoji web fonts.
 del font['glyf'];del font['loca'];font['maxp'].tableVersion=0x00005000
 font.flavor='woff2';font.save(OUT/'fonts'/(style+'.woff2'))
 print(style,(OUT/'fonts'/(style+'.woff2')).stat().st_size,flush=True)
 # Every official qualification must shape to precisely one bitmap glyph.
 import uharfbuzz as hb
 font.flavor=None;buf=io.BytesIO();font.save(buf)
 hf=hb.Font(hb.Face(buf.getvalue()))
 for text,key in aliases.items():
  b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(hf,b,{'rlig':True})
  visible=[g.codepoint for g in b.glyph_infos if g.codepoint!=font.getGlyphID(cpnames.get(0xFE0F,'.notdef'))]
  expected=font.getGlyphID(ids[key])
  assert visible==[expected],(style,text,visible,expected)
 print('shape PASS',len(aliases),flush=True)
