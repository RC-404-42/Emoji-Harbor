from pathlib import Path
src=Path('emoji-harbor-src')
for p in src.iterdir():
 if p.suffix in ['.js','.json','.html','.md']:
  p.write_text(p.read_text().replace('1.3.0','1.3.1').replace('伯爵拿鐵','灰岩拿鐵'))
p=src/'themes.css';s=p.read_text().replace('--teal:var(--t-accent);--orange:var(--t-accent);','--teal:var(--t-accent-ink,var(--t-accent));--orange:var(--t-accent-ink,var(--t-accent));')
lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith('body.popup-v110[data-popup-theme="sakura"]'):
  lines[i]='body.popup-v110[data-popup-theme="sakura"]{--t-scheme:light;--t-bg:#fff0f7;--t-card:#ffe0ef;--t-control:#fff7fb;--t-button:#ffd0e7;--t-hover:#ffbddd;--t-line:#cb638e;--t-ink:#57263f;--t-muted:#82405f;--t-accent:#ff0da6;--t-accent-ink:#a60069;--t-selected:#ffc4e3;--t-on-accent:#4d1238;--t-error:#a32c2c}'
 if line.startswith('body.popup-v110[data-popup-theme="earl"]'):
  lines[i]='body.popup-v110[data-popup-theme="earl"]{--t-scheme:dark;--t-bg:#454545;--t-card:#555555;--t-control:#3c3c3c;--t-button:#606060;--t-hover:#686868;--t-line:#989898;--t-ink:#f5f5f5;--t-muted:#d2d2d2;--t-accent:#dedede;--t-selected:#666666;--t-on-accent:#333333;--t-error:#ffb4b4}'
s='\n'.join(lines)+'\n'
s=s.replace('.eh-select-option[aria-selected=true]{color:var(--t-accent)}','.eh-select-option[aria-selected=true]{color:var(--t-accent-ink,var(--t-accent))}')
a=s.index('.popup-v110 .theme-control{');b=s.index('.popup-v110 .theme-menu',a)
s=s[:a]+'''/* Shared geometry keeps the theme and settings controls identical. */
.popup-v110 header #options,.popup-v110 .theme-control .eh-select-trigger{width:40px;height:40px;min-height:40px;flex-shrink:0;padding:0;border-radius:11px;display:flex;align-items:center;justify-content:center;gap:0}
.popup-v110 .theme-control{width:40px;flex:0 0 40px}
.popup-v110 .theme-control .eh-select-trigger>span{display:none}
.popup-v110 .theme-control .eh-select-trigger::before{content:"";display:block;width:22px;height:25px;background:url("icons/theme-drop.svg") center/contain no-repeat}
body.popup-v110[data-popup-theme] .theme-control .eh-select-trigger{background:var(--t-button)}
body.popup-v110[data-popup-theme] .theme-control .eh-select-trigger:hover{background:var(--t-hover)}
'''+s[b:]
p.write_text(s)
(src/'icons/theme-drop.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 28"><defs><linearGradient id="pink" x1="4" y1="4" x2="19" y2="26" gradientUnits="userSpaceOnUse"><stop stop-color="#ffe6f6" stop-opacity=".84"/><stop offset=".5" stop-color="#ffa6d4" stop-opacity=".64"/><stop offset="1" stop-color="#f478c0" stop-opacity=".44"/></linearGradient></defs><path d="M12 2C10.7 6.2 3.6 12.1 3.6 18a8.4 8.4 0 0 0 16.8 0C20.4 12.1 13.3 6.2 12 2Z" fill="url(#pink)" stroke="#ffd4ec" stroke-opacity=".7" stroke-width="1.1" stroke-linejoin="round"/><path d="M8.7 12.8C7 15 6.6 16.2 6.6 18" fill="none" stroke="#fff6fc" stroke-opacity=".8" stroke-width="1.8" stroke-linecap="round"/></svg>''')
# Historical release notes keep their original version and name; new note explains the rename.
p=src/'help.html';s=p.read_text();needle='<h3>1.3.1 · 2026-10-28</h3>'
assert needle in s
s=s.replace(needle, '<h3>1.3.1 · 2026-10-28</h3><ul><li>配色按鈕與齒輪統一為圓角方形，使用半透明粉色水滴。</li><li>灰色款改名「灰岩拿鐵」，以深灰為底、淺灰為輔；保留既有選擇。</li><li>櫻花歐蕾增加粉紅底色與 #FF0DA6 強調色，小字使用較深莓粉色。</li></ul><h3>1.3.0 · 2026-10-28</h3>',1)
p.write_text(s)
# Update the existing regression suite for the new release/name. No new tests for styling-only changes.
t=Path('tooling/test-v130.cjs').read_text().replace('1.3.0','1.3.1').replace('伯爵拿鐵','灰岩拿鐵');Path('tooling/test-v131.cjs').write_text(t)
