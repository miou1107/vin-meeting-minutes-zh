# 檔案清單

| 檔案 | 用途 |
|---|---|
| `SKILL.md` | 給 AI 讀的整理規則：流程、章節格式、語氣、設定引導 |
| `README.md` | 給人讀的介紹與安裝方法 |
| `CHANGELOG.md` | 每個版本改了什麼 |
| `FILELIST.md` | 這份檔案清單 |
| `references/example-minutes.md` | 虛構的完整會議紀錄範例，八節都有 |
| `references/glossary.md` | 通用的語音辨識錯字對照（SEO、KOL、Threads 這類） |
| `scripts/google_setup.py` | 檢查與完成 Google 設定，讀使用者的 `settings.json` |
| `scripts/md_to_docx.py` | 把 Markdown 紀錄排成標準版面的 Word 檔 |
| `scripts/md_to_gdoc.py` | 把紀錄發成 Google 文件，改版時覆蓋同一份 |
| `scripts/gdoc_to_md.py` | 把 Google 文件拉回成 Markdown |
| `scripts/workspace.py` | 讀 Gmail 逐字稿、查行事曆與通訊錄、寄信、建會議邀請 |
| `scripts/notify.py` | Gmail 不能用時，改用 Google 文件的分享通知寄連結 |
| `scripts/check_update.py` | 整理完會議紀錄後檢查 GitHub 上有沒有新版，一天最多查一次 |

使用者自己的檔案不在這裡，放在 `~/.config/vin-meeting-minutes-zh/`：

| 檔案 | 用途 |
|---|---|
| `settings.json` | 信箱、寄件署名、我方公司簡稱、分享網域、逐字稿搜尋條件、字型與顏色 |
| `notes.md` | 自己的規則、偏好與語氣、判斷時參考的實例 |
| `glossary.md` | 自己公司的詞彙表 |
| `oauth-client.json`、`google-token.json` | Google 登入 |
| `update-check.json` | 上次檢查新版的時間，和已經問過的版本 |
