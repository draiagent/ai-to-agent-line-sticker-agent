# ai-to-agent-line-sticker-agent

## LINE 貼圖製作與驗收上架

提供參考圖片與VAC任務圖卡，由Agent完成靜態或動態貼圖的樣板製作、批次生成、規格檢查與上架準備。

![VAD流程設計與VAC任務圖卡](assets/vac-line-sticker.png)

## 為什麼做這個專案？

有角色圖片，卻卡在去背、文字動畫、尺寸調整、逐張檢查與打包。AI Coach益力康陳董將這些痛點整理成能交給Agent執行的流程，讓創作者專心決定角色個性與粉絲想用的貼圖用語。

閱讀[完整社群文章](docs/article.md)。

## 開始使用

1. 將上方VAC與8張參考圖片交給具備讀圖、產圖及檔案處理能力的Agent。
2. 選擇「生成靜態貼圖」或「生成動態貼圖」。
3. Agent先做一張樣板；確認後再批次製作與檢查。
4. 收取貼圖ZIP、預覽、上架文案與驗收表；上傳、送審依圖卡授權流程進行。

可直接使用圖卡；文字版見[VAC](docs/vac.md)，可載入的技能位於[SKILL.md](skill/line-sticker-agent/SKILL.md)。技能可整個資料夾交給支援技能的Agent；不同平台依其安裝方式載入。

**文字是動畫重點：人物、寵物、物品保持靜止。** 先確認一張，再批次製作，避免整批返工。

## 輸入、輸出與適用範圍

適合IP創作者、社群版主及品牌內容團隊。輸入為參考圖片、用語與類型；完整任務輸出為8張貼圖、主要圖片、聊天室標籤圖、預覽、文案、驗收表及ZIP。

本Repo包含工作技能與輔助程式，需由有相應工具的Agent執行。Python程式只處理縮放、已有畫格的APNG編碼、單張技術檢查與PNG打包，不會自行繪圖或登入LINE。

## 已有實測

**以下為舊版動畫測試，外圍白邊已被指出需修正，不作為最終上架成品。**

![舊版文字動態預覽](examples/rest-break/preview.gif)

[休息一下案例](examples/VAC-rest-break.md)附靜態PNG、動態APNG與GIF預覽。新增[去白邊動畫測試](examples/rest-break/borderless-animated.png)與[原圖](examples/rest-break/borderless-source.png)。使用者仍指出畫質與殘影問題，因此所有測試樣板均未通過最終視覺驗收，作為問題分析案例；8張套組、主要圖片、標籤圖與平台上傳仍需在實際任務執行。詳見[驗收紀錄](docs/validation.md)。

## 輔助程式快速測試

Python 3.10以上，安裝Pillow：

```bash
python -m pip install -r requirements.txt
python scripts/sticker.py verify --input examples/rest-break/static.png --kind static
python scripts/sticker.py verify --input examples/rest-break/animated.png --kind animated
python scripts/sticker.py static --input examples/rest-break/static.png --output output/01.png
```

已有5–20張不同透明畫格時，可執行：

```bash
python scripts/sticker.py animated --frames-dir frames/01 --output output/01.png --duration-ms 2000
python scripts/sticker.py verify --input output/01.png --kind animated
python scripts/sticker.py package --input-dir output --output output/stickers.zip
```

package僅打包資料夾中的PNG，不代表套組數量、main/tab或審核內容已通過。上傳前由Agent逐項完成[驗收清單](docs/acceptance.md)。

## 專案內容

| 路徑 | 內容 |
|---|---|
| assets/vac-line-sticker.png | 最新銅曜霓境風格VAC圖卡 |
| docs/article.md | 完整署名社群文章 |
| docs/vac.md | 圖卡文字版 |
| docs/acceptance.md | 上架前驗收清單與官方來源 |
| docs/validation.md | 本版實際檢查紀錄 |
| skill/line-sticker-agent/SKILL.md | Agent工作技能 |
| scripts/sticker.py | 輔助製作及技術檢查 |
| examples/rest-break/ | 單張靜態、動態及預覽樣板 |
| RELEASE_NOTES.md | 版本發布說明 |

## 版本與後續

v0.3.0，2026-11-01。由既有v1檔名的初始套件整理而來；舊套件無SemVer版本宣告，本版仍屬樣板驗證階段。後續先依新版VAC完成清晰、無殘影的合格樣板，再進行完整8張套組與實際上傳驗收，不列為已完成功能。

## 授權

沿用既有[MIT授權](LICENSE)於程式與文字文件。Logo、人物肖像、角色與圖片不隨程式授權，見[素材聲明](ASSET_RIGHTS.md)。

AI Coach 益力康陳董 x CGM Coach 血糖教練  
2026 AI to Agent | 2027 AI to AGI Agent
