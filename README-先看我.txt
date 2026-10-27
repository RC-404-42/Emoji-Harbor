表情補給站 Emoji Harbor 1.2.4
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
Firefox 開發包：本次附帶的 Emoji-Harbor-Firefox-v1.2.4-unsigned.xpi 尚未簽署，請在 about:debugging#/runtime/this-firefox 暫時載入，完全退出再重開後須重載。

詳細說明請開啟 Start-Here.html。隱私聲明另附 PRIVACY.md、Privacy.html。
膚色選項控制選字盤與新插入的表情，不會修改網頁原本的膚色。
七套靜態字型和230個動畫均為本機素材；其他字型可自行匯入。

109 項功能邏輯檢查通過，包含根節點樣式重設與動態清單重建的模擬測試。
尚未完成本版 Chrome／Firefox／Win10 及 Discord 真實頁面的實機視覺驗證。
Chrome 資料夾及 XPI 內含執行原始碼；XPI 是 ZIP 格式，可解壓查看。
公開分享請保留授權：程式碼 MIT 不代表所有圖案與字型都屬 MIT，詳見 Chrome/licenses。


1.2.4（2026-10-27）：設定頁新增預設選字盤分頁（全部／最近使用），以及小、中、大、特大表情尺寸；不影響網頁字形尺寸。加入 Mona12 彩色像素風格（OFL 1.1），缺字由 Noto 後備，複合表情支援取決於字型。字型來源及版本見 Chrome/build-info.json。
選字盤偏好不廣播重套頁面字型，快取膚色結果，每批通知最多4個分頁；背景分頁暫停動畫，切回不再全頁重掃。
Telegram 動畫本版未加入。未完成真實瀏覽器效能與視覺驗證，未與 Emoji Swap 實測比較。

Firefox 1.2.4 採 OpenType SVG 字型；請先暫時載入確認 Windows Firefox 顯示，再重新送簽。此環境尚未完成實機驗證。
