# 參與方式

請附輸入條件、重現步驟、預期與實際結果。角色素材僅提交已取得權利的內容，不提交登入資料或金鑰。

修改規格時附官方來源及查核日期；同步更新VAC文字、技能與README。圖卡改版需保留Logo與完整署名。

程式修改後執行：

```bash
python -m unittest discover -s tests -v
python scripts/sticker.py verify --input examples/rest-break/static.png --kind static
python scripts/sticker.py verify --input examples/rest-break/animated.png --kind animated
```

視覺效果另以實際尺寸及播放覆核。請透過Pull Request描述問題、修改與驗證。
