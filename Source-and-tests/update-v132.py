from pathlib import Path
src=Path('emoji-harbor-src')
for p in src.iterdir():
 if p.suffix in ['.js','.json','.html','.md']:p.write_text(p.read_text().replace('1.3.1','1.3.2'))
# An empty center reveals the button color rather than tinting every theme pink.
(src/'icons/theme-drop.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 28"><path d="M12 2C10.7 6.2 3.6 12.1 3.6 18a8.4 8.4 0 0 0 16.8 0C20.4 12.1 13.3 6.2 12 2Z" fill="none" stroke="#f5cde2" stroke-opacity=".58" stroke-width="1.5" stroke-linejoin="round"/></svg>')
p=src/'themes.css';s=p.read_text().replace('background:url("icons/theme-drop.svg") center/contain no-repeat','background:var(--t-ink);opacity:.55;mask:url("icons/theme-drop.svg") center/contain no-repeat');p.write_text(s)
p=src/'picker.js';s=p.read_text().replace('const SIZE=80;',"let pageSize=0;const sizes={small:[8,28,4],medium:[6,36,3],large:[4,52,2],huge:[2,84,1]};\n // Only complete rows belong on a popup page. Settings uses the same compact defaults.\n function pageCapacity(){const size=sizes[EH.normalize(settings()).pickerSize];let rows=size[2];const grid=$('emojiGrid');if(document.body.classList.contains('popup-v110')&&grid.clientHeight>0){const css=getComputedStyle(grid),gap=parseFloat(css.rowGap)||0,padding=(parseFloat(css.paddingTop)||0)+(parseFloat(css.paddingBottom)||0),height=grid.clientHeight-padding;rows=Math.max(1,Math.min(4,Math.floor((height+gap)/(size[1]*1.6+20+gap))))}return size[0]*rows}")
s=s.replace("const sizes={small:[8,28],medium:[6,36],large:[4,52],huge:[2,84]},size=sizes[drawSize];", "const size=sizes[drawSize],first=page*pageSize;")
s=s.replace("syncMode();drawStyle=", "const capacity=pageCapacity();if(pageSize!==capacity){pageSize=capacity;page=Math.floor(first/pageSize)}page=Math.max(0,Math.min(page,Math.max(0,Math.ceil(filtered.length/pageSize)-1)));syncMode();drawStyle=")
s=s.replace('grid.replaceChildren();for', 'grid.replaceChildren();grid.scrollTop=0;for').replace('page*SIZE,(page+1)*SIZE', 'page*pageSize,(page+1)*pageSize').replace('filtered.length/SIZE','filtered.length/pageSize').replace('(page+1)*SIZE','(page+1)*pageSize')
s=s.replace(" filter();return {clearRecents", " if(document.body.classList.contains('popup-v110')&&globalThis.ResizeObserver)new ResizeObserver(()=>{if(pageCapacity()!==pageSize)draw()}).observe($('emojiGrid'));\n filter();return {clearRecents")
assert 'SIZE' not in s;p.write_text(s)
p=src/'help.html';s=p.read_text().replace('<h3>1.3.2 · 2026-10-28</h3>','<h3>1.3.2 · 2026-10-28</h3><ul><li>配色按鈕改為半透明空心水滴，線條跟隨配色，中央透出原本底色。</li><li>減少選字盤每頁數量；右上角依表情大小與可用高度顯示完整列，其餘改到下一頁。翻頁回到頂端，切換大小與視窗高度時保留附近位置。</li></ul><h3>1.3.1 · 2026-10-28</h3>',1);p.write_text(s)
# Adapt the existing regression test's initial count and add boundary/resize coverage.
t=Path('tooling/test-v131.cjs').read_text().replace('1.3.1','1.3.2').replace(".length===80,file+' immediately renders picker'", ".length===32,file+' immediately renders compact picker'")
t=t.replace("await themeTests();console.log", "await themeTests();await paginationTests();console.log")
Path('tooling/test-v132.cjs').write_text(t)
