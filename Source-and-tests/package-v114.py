import pathlib,shutil,json,zipfile,hashlib,re
src=pathlib.Path('emoji-harbor-src');root=pathlib.Path('dist/Emoji-Harbor-v1.1.4');root.mkdir(exist_ok=True)
assert 'ALL 86 CHECKS PASSED' in pathlib.Path('tooling/validation-v114.log').read_text()
dest=root/'Chrome';shutil.copytree(src,dest,dirs_exist_ok=True)
m=json.loads((dest/'manifest.json').read_text());m.pop('browser_specific_settings',None);(dest/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
firefox=pathlib.Path('tooling/firefox-v114');shutil.copytree(src,firefox,dirs_exist_ok=True)
m=json.loads((firefox/'manifest.json').read_text());m['background']={'scripts':['core.js','background.js']};(firefox/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
for folder in [dest,firefox]:
 m=json.loads((folder/'manifest.json').read_text());assert m['version']=='1.1.4'
 refs=m['content_scripts'][0]['js']+[m['action']['default_popup'],m['options_ui']['page']]+list(m['icons'].values())
 for r in refs:assert (folder/r).is_file(),r
 for page in folder.glob('*.html'):
  for r in re.findall(r'(?:src|href)="([^"#]+)"',page.read_text()):
   if ':'not in r:assert (page.parent/r).is_file(),(page,r)
 for name in ['content.js','core.js','background.js','dropdown.js','picker.js','popup.js','options.js']:
  assert (folder/name).read_bytes()==(src/name).read_bytes(),name
xpi=pathlib.Path('dist/Emoji-Harbor-Firefox-v1.1.4-unsigned.xpi')
with zipfile.ZipFile(xpi,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(firefox.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(firefox))
with zipfile.ZipFile(xpi)as z:
 assert z.testzip()is None
 manifest=json.loads(z.read('manifest.json'));assert manifest['version']=='1.1.4'
 assert manifest['browser_specific_settings']['gecko']['id']=='emoji-harbor@local.invalid'
 assert 'scripts'in manifest['background']and'service_worker'not in manifest['background']
 assert len([n for n in z.namelist()if n.startswith('fonts/')and n.endswith('.woff2')])==6
 assert len([n for n in z.namelist()if n.startswith('anim/')and n.endswith('.webp')])==230
 assert z.read('PRIVACY.md')==(src/'PRIVACY.md').read_bytes()
 assert not any(n.startswith('META-INF/')for n in z.namelist())
shutil.copyfile(xpi,root/xpi.name)
for source,target in [('help.html','Start-Here.html'),('privacy.html','Privacy.html')]:
 text=(src/source).read_text().replace('href="ui.css"','href="Chrome/ui.css"').replace('src="icons/128.png"','src="Chrome/icons/128.png"');(root/target).write_text(text)
shutil.copyfile(src/'PRIVACY.md',root/'PRIVACY.md');shutil.copyfile(src/'LICENSE',root/'LICENSE')
(root/'README-先看我.txt').write_text("""表情補給站 Emoji Harbor 1.1.4
GPT 協助開發、編寫程式與使用說明。

這版改善：
- 效能修正：不相關的樣式變更不再重掃子樹，新增內容分批掃描，取消定時全頁重掃。
- 眨眼喝奶茶圖示改為平面插畫風格。
- 說明移除 Firefox 簽署教學，只保留安裝方式。
- Chrome／Edge／Vivaldi／Brave 安裝說明。
- 字型使用固定本機名稱，避免網站重設根節點樣式後失效。
- 網頁重建文字、覆寫字型或降級樣式優先權時，自動重新套用。

Chrome／Edge／Vivaldi／Brave：解壓後在擴充管理頁開啟開發人員模式，載入 Chrome 資料夾。
Chrome 更新：把新版 Chrome 資料夾內容覆蓋到原安裝位置，再到 chrome://extensions 按重新載入。已開的網站首次重整一次。
Firefox 正式包：about:addons → 齒輪 → 從檔案安裝附加元件，選發布者提供的已簽署 XPI。
Firefox 開發包：本次附帶的 Emoji-Harbor-Firefox-v1.1.4-unsigned.xpi 尚未簽署，請在 about:debugging#/runtime/this-firefox 暫時載入，完全退出再重開後須重載。

詳細說明請開啟 Start-Here.html。隱私聲明另附 PRIVACY.md、Privacy.html。
膚色選項控制選字盤與新插入的表情，不會修改網頁原本的膚色。
六套靜態字型和230個動畫均為本機素材；其他字型可自行匯入。

86 項功能邏輯檢查通過，包含根節點樣式重設與動態清單重建的模擬測試。
尚未完成本版 Chrome／Firefox／Win10 及 Discord 真實頁面的實機視覺驗證。
Chrome 資料夾及 XPI 內含執行原始碼；XPI 是 ZIP 格式，可解壓查看。
公開分享請保留授權：程式碼 MIT 不代表所有圖案與字型都屬 MIT，詳見 Chrome/licenses。
""")
(root/'README.md').write_text('''# 表情補給站 · Emoji Harbor

使用者提出想法、測試與回饋，GPT 協助開發編寫。

離線 Emoji 顯示與選字擴充，支援 Chrome 與 Firefox。可切換六種靜態風格、Noto 動畫、調整大小及選定膚色；可自行匯入彩色字型。

## 安裝與更新

- Chrome／Edge／Vivaldi／Brave：在各瀏覽器擴充管理頁啟用開發人員模式，載入 `Chrome` 資料夾。更新時覆蓋原安裝位置再重新載入。
- Firefox 正式包：`about:addons` → 齒輪 → 從檔案安裝附加元件，選發布者提供的已簽署 XPI。
- Firefox 開發包：本次附帶的 `unsigned.xpi` 尚未簽署，請在 `about:debugging#/runtime/this-firefox` 暫時載入，重開瀏覽器後須重載。
- 下載後開啟 `Start-Here.html` 閱讀完整中文說明。

## 隱私

詳見 [隱私聲明](PRIVACY.md)。本版本沒有伺服器、帳號、追蹤或外部字型請求。偏好、最近使用與匯入字型只存在本機。

## 原始碼與驗證

`Chrome` 資料夾與 XPI 內均為完整可讀原始碼，正常使用無需建置。86 項功能邏輯檢查通過；本版未完成 Win10、雙瀏覽器及 Discord 真實頁面的實機安裝與視覺驗證。

## 授權

原創程式碼採 MIT。第三方字型及圖案各依其條款；Apple 圖案不在程式碼 MIT 授權範圍。請保留 `Chrome/licenses`，確認素材條款後再散布對應素材。隱私聲明不會變更素材授權。
''')
old=pathlib.Path('dist/Emoji-Harbor-v1.1.0')
for name in ['Webpage-Test.html','webpage-test.js','Style-Preview.png']:
 shutil.copyfile(old/name,root/name)
dev=root/'Source-and-tests';dev.mkdir(exist_ok=True)
for name in ['build-fonts.py','render-assets.cjs','render-extra.cjs','download-animations.py','test-v114.cjs','package-v114.py']:
 shutil.copyfile(pathlib.Path('tooling')/name,dev/name)
shutil.copyfile('emoji-atelier-work/assets/catalog.json',dev/'font-catalog.json');shutil.copyfile('tooling/validation-v114.log',dev/'VALIDATION.txt')
with(dev/'VALIDATION.txt').open('a')as f:f.write('\nPackaging: XPI manifest at archive root, stable Gecko ID, Firefox background scripts, 6 WOFF2 fonts, 230 animated WebPs, included privacy text, archive CRC and resource references verified.\nBrowser integration NOT verified. Logic tests mock browser/FontFace/geometry APIs. Existing static fonts and artwork were not changed in 1.1.4.\n')
(dev/'README.txt').write_text('''Chrome/ and the XPI contain ready-to-load source. No build is required for normal use.
For logic tests: npm install jsdom@26 in this folder, then node test-v114.cjs.
Font pipeline utilities document previous asset generation. They require upstream images and build dependencies; font bitmaps and final animations are included in the extension.
''')
assert re.findall(r'<h2>(.*?)</h2>',(root/'Start-Here.html').read_text())==['表情補給站','初次安裝','版本與更新說明','動畫如何運作','套用範圍與排除','權限與資料','驗證狀態','隱私聲明']
archive=pathlib.Path('dist/Emoji-Harbor-v1.1.4.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root.parent))
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None
 assert z.read(root.name+'/'+xpi.name)==xpi.read_bytes()
for p in [archive,xpi]:print(p.resolve(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
