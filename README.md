# Studyhighschool

高中自然科電子講義。直接開啟 index.html，或透過 GitHub Pages 閱讀；無需安裝套件即可使用網站。

## 地科與生物
- 地科：原有歷史、天文、地質，加上大氣、海洋、天然災害、氣候資源與進階探究。
- 生物：原有細胞與能量，加上孟德爾、血型、染色體、性聯及連鎖互換。
- 保留585題既有題目與詳解；新增16篇原圖配文字講義、96題檢核。
- sources.html：4份參考講義共366頁完整原頁，可依冊別、單元、PDF頁碼閱讀及搜尋。新增原題採完整原頁呈現，與另編96題檢核分開。
- 原頁圖表、選項、附答及手寫註記保留；OCR只作搜尋輔助，請以原頁為準。

## 編輯與重建
`_src/continuation.json` 是新增章節內容，`_src/reading-guides.json` 保留舊版導讀稿；新版不再插入大型導讀卡。

```powershell
python _src/build_handouts.py
python _src/validate_handouts.py
```

重新匯入原資料：`python _src/build_sources.py`，需本機來源PDF、Markdown、PyMuPDF及Pillow。既有原章節的上游生成器仍在各科「講義電子化/_src」；使用上游重新匯出後，須再次執行本repo的 build_handouts.py。

來源位置與範圍見 sessionnote.md，逐頁對照見 _src/source-coverage.csv。

## 2026-10-19 排版修正
- 新增16篇沿用前面單元的排版：原講義截圖→逐段文字講解→隨堂練習。48張對應原頁裁圖附PDF頁碼；後續180頁完整原稿直接納入各單元。
- 新章節已融合在首頁原有科目卡片、各科chgrid目錄及側欄，移除獨立追加區。
- 裁圖規格：_src/layout-figures.json；版型：_src/rebuild_layout.py；導覽：_src/integrate_navigation.py。build_handouts.py會依序呼叫重建。

## 逐單元品質重做
目前逐篇精修完成的是生物3-1，其他新增單元待逐篇重寫。3-1直接沿用既有生物單元的原始版型，先建立概念與比較表，再配原圖、推導與完整詳解。正文位於 _src/units/biology-3-1.html，重建使用 python _src/build_biology_3_1.py。
