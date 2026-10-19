# Studyhighschool

高中自然科電子講義。直接開啟 index.html，或透過 GitHub Pages 閱讀；無需安裝套件即可使用網站。

## 地科與生物
- 地科：原有歷史、天文、地質，加上大氣、海洋、天然災害、氣候資源與進階探究。
- 生物：原有細胞與能量，加上孟德爾、血型、染色體、性聯及連鎖互換。
- 保留585題既有題目與詳解；新增16篇概念講義、96題檢核、25篇閱讀引導。
- sources.html：4份參考講義共366頁完整原頁，可依冊別、單元、PDF頁碼閱讀及搜尋。新增原題採完整原頁呈現，與另編96題檢核分開。
- 原頁圖表、選項、附答及手寫註記保留；OCR只作搜尋輔助，請以原頁為準。

## 編輯與重建
`_src/continuation.json` 是新增章節內容，`_src/reading-guides.json` 是既有章節導讀。

```powershell
python _src/build_handouts.py
python _src/validate_handouts.py
```

重新匯入原資料：`python _src/build_sources.py`，需本機來源PDF、Markdown、PyMuPDF及Pillow。既有原章節的上游生成器仍在各科「講義電子化/_src」；使用上游重新匯出後，須再次執行本repo的 build_handouts.py。

來源位置與範圍見 sessionnote.md，逐頁對照見 _src/source-coverage.csv。
