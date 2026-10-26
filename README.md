# 表情補給站 · Emoji Harbor

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
