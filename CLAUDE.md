# 專案交接
先讀 AGENTS.md 與 sessionnote.md，尤其最後的逐單元進度。使用者已接受生物3-1，要求品質優先、地科一單元再生物一單元，並持續留下session note。

已逐篇精修：生物3-1、地科4-1、生物3-2。其餘13篇新增單元只是舊批次草稿，不得當作已完成品質重做。下一組：地科4-2 → 生物3-3。每一單元先核對原PDF圖與文字，再自己逐段編寫，參考原Claude的biology/u1-5.html、u1-4.html及已接受的3-1。

## 檔案與重建
- _src/units/<科目-單元>.html：逐篇正文。
- 對應.questions.json：六組完整詳解；.json：裁圖座標、側欄、來源頁碼；.review.json：驗證。
- python _src/build_earth_4_1.py / python _src/build_biology_3_2.py 只重建指定單元。
- _src/individual_unit.py只共享原版型與裁圖流程，沒有代寫內容；individual-unit.css只做少量局部修正。
- build_biology_3_1.py是原本獨立實作，保持不動。
- rebuild_layout.py最後的三個逐篇覆寫必須保留。不能只改輸出HTML，或拿continuation.json的批次稿覆蓋精修內容。

## 來源與核對
地科：E:\家教備課\男生\地科\講義；生物：E:\家教備課\男生\生物\講義。網站：E:\家教備課\男生\總\Studyhighschool。
earth/4-1來源地科2 PDF2–5（印刷104–107）；biology/3-2來源生物1 PDF89下半–93（印刷91–95）。原小試1–8與經典演練1–12已解說；原頁與印刷頁不可混用。
已精修單元的易錯點與原題簡化限制見sessionnote，尤其同染色體遠距可近似獨立，不能又抄回過度簡化敘述。

## 驗證與發布
python _src/check_earth_4_1_biology_3_2.py；python _src/validate_handouts.py。必須實際看裁圖與桌面、390px手機畫面，檢查答案開合、書籤保存／篩選、放大、目錄。原題數與卡組數分開記錄。
開始、成稿、驗證、發布立即追加sessionnote；推送後確認GitHub Pages公開HTML與圖片確實更新。Pages目前從main根目錄自動發布，build_type=legacy。
不要夾帶其他對話的物理、化學、首頁未提交修改。
