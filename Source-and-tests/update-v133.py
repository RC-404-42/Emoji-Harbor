from pathlib import Path
src=Path('emoji-harbor-src')
for p in src.iterdir():
 if p.suffix in ['.js','.json','.html','.md']:p.write_text(p.read_text().replace('1.3.2','1.3.3'))
p=src/'picker.js';s=p.read_text().replace('medium:[6,36,3],large:[4,52,2],huge:[2,84,1]', 'medium:[6,36,4],large:[4,52,3],huge:[2,84,2]')
s=s.replace('// Only complete rows belong on a popup page. Settings uses the same compact defaults.', '// Allow one extra row for a short scroll instead of leaving a partial-row gap.')
s=s.replace('Math.min(4,Math.floor((height+gap)/(size[1]*1.6+20+gap)))', 'Math.min(5,Math.floor((height+gap)/(size[1]*1.6+20+gap))+1)')
s=s.replace('let pageSize=0;', 'let pageSize=0,pageAnchor=0;').replace('function filter(){page=0;', 'function filter(){page=0;pageAnchor=0;').replace('first=page*pageSize;', 'first=pageAnchor;').replace("()=>{page--;draw()}", "()=>{page--;pageAnchor=page*pageSize;draw()}").replace("()=>{page++;draw()}", "()=>{page++;pageAnchor=page*pageSize;draw()}")
assert 'Math.min(5,' in s;p.write_text(s)
p=src/'themes.css';s=p.read_text();lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith('body.popup-v110[data-popup-theme="sakura"]'):
  lines[i]='body.popup-v110[data-popup-theme="sakura"]{--t-scheme:light;--t-bg:#f7eaf0;--t-card:#fceff5;--t-control:#fff8fb;--t-button:#ecd3df;--t-hover:#e9c6d8;--t-line:#b48b9e;--t-ink:#513846;--t-muted:#795b6b;--t-accent:#bb7b9a;--t-accent-ink:#8d4f70;--t-selected:#e9c9da;--t-on-accent:#4b2639;--t-error:#a32c2c}'
p.write_text('\n'.join(lines)+'\n')
p=src/'help.html';s=p.read_text().replace('<h3>1.3.3 · 2026-10-28</h3>', '<h3>1.3.3 · 2026-10-28</h3><ul><li>右上角選字盤在可容納的完整列之外多放一列，填補底下空白，只需短距離捲動；其餘仍分頁。</li><li>櫻花歐蕾改為低飽和的櫻花奶粉底、柔和玫瑰色按鈕與莓灰文字，降低亮桃紅的刺激感。</li></ul><h3>1.3.2 · 2026-10-28</h3>',1);p.write_text(s)
s=Path('tooling/test-v132.cjs').read_text().replace('1.3.2','1.3.3')
s=s.replace("items().length===32&&prev.disabled&&d.getElementById('pageInfo').textContent==='1 / 61'", "items().length===40&&prev.disabled&&d.getElementById('pageInfo').textContent==='1 / 49'")
s=s.replace('compact small page has four full rows and correct page count', 'small page fills the viewport and adds one short-scroll row')
s=s.replace('items().length===32&&g.scrollTop===0', 'items().length===40&&g.scrollTop===0')
s=s.replace("[['huge',2],['large',8],['medium',18],['small',32]]", "[['huge',4],['large',12],['medium',24],['small',40]]")
s=s.replace("items().length===16&&titles().includes(anchor)", "items().length===24&&titles().includes(anchor)").replace('smaller popup fits two complete rows while retaining the visible anchor','smaller popup keeps two full rows plus one extra, retaining the anchor')
s=s.replace('items().length===32&&titles().includes(anchor)', 'items().length===40&&titles().includes(anchor)')
# Check every size with the height shown in the user screenshots: total content
# exceeds the viewport by at most one row and gap, without a vacant lower block.
s=s.replace("// Reset and then resize while away from the first page: keep the anchor nearby.", """// Check the requested short-scroll compromise against a 265px grid.
 height=265;
 for(const [size,cols,px,expected]of [['small',8,28,32],['medium',6,36,24],['large',4,52,12],['huge',2,84,4]]){
  e.store.settings.pickerSize=size;d.getElementById('search').dispatchEvent(new e.w.Event('input'));const rows=items().length/cols,content=rows*(px*1.6+20)+(rows-1)*3+6;
  check(items().length===expected&&content>height&&content-height<=px*1.6+23,size+' fills the lower gap with at most one row of scrolling');
 }
 e.store.settings.pickerSize='small';height=290;
 // Reset and then resize while away from the first page: keep the anchor nearby.""")
Path('tooling/test-v133.cjs').write_text(s)
