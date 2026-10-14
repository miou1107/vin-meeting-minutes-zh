# 會議紀錄 skill（vin-meeting-minutes-zh）

這個會議記錄 skill 是由某位不願具名、常被各種會議蹂躪、且對寫會議記錄十分苦惱的會議達人精心特調過，特別適合台灣一般中小企業，無論用在內部會議、跨單位/跨公司會議都適合。讓 AI 把會議逐字稿整理成正式的繁體中文會議紀錄，用詞照台灣的習慣寫。Claude 整理完會產出 Google 文件或 Word 檔。
只要你手上有逐字稿，即使內容零碎、錯字連連，同樣都能整理出有條有理的會議記錄，且還原的程度非常高。

完成的會議紀錄，可參考 [範例](references/example-minutes.md)。

## 亮點特色

- **錯字再多、沒標講者的逐字稿也能整理**：Claude 會先讀專案的提案、前幾次的紀錄和人員名單，再修正語音辨識的錯字，判斷每段話是誰講的。
- **沒把握的地方不硬猜**：分不出是誰講的就先寫單位，聽不清楚的字和數字照原文保留，交件時一起列出來請你確認。
- **越用越準**：你更正過的錯字和講者會存進專案的對照表，下一場會議就不會再錯。
- **對內、對外分開寫**：公司內部會議直接寫人名；有客戶或廠商參加的會議只寫單位，客戶離線後的內部討論會刪除。
- **台灣用語、正式語氣**：政府案用公文體，公司內部和企業客戶用正式商務語氣，不寫中國大陸用語，也不寫 AI 常用的套話。
- **格式邏輯一致**：所有專案會議記錄格式邏輯高度一致、結構清晰，方便不同場次會議內容追蹤與分析。
- **直接產出 Google 文件**：完成 Google 設定後，Claude 會在你的 Google 雲端硬碟建好文件，並開放給公司同仁加註。之後改版網址不變；有人在文件上改過或留言，Claude 會先停下來問你。
- **接上 Gmail、行事曆和公司通訊錄，整理完直接寄信**：錄音 App 把逐字稿寄到你的 Gmail 之後，你把那封信的連結交給 Claude，或直接說「整理今天下午那場」即可。Claude 會從行事曆帶入會議時間、地點和與會人員，再從公司通訊錄查出每個人的信箱。紀錄整理好之後，Claude 會先讓你看要寄出的信。你回「發信」，Claude 才會從你的 Gmail 寄出。下次會議還沒排進行事曆的話，Claude 也會準備好會議邀請，同樣等你同意才寄出。

「直接產出 Google 文件」和「接上 Gmail、行事曆和公司通訊錄」這兩項，第一次使用前要先完成 Google 設定，設定方式見「要用 Google 文件和 Gmail，第一次要先設定」。

## 內容架構

| 章節 | 寫什麼 |
|---|---|
| 一、會議基本資訊 | 主題、日期時間、地點、主持人、與會人員、會議資料連結 |
| 二、會議目的 | 這場會議承接什麼、要確認什麼 |
| 三、討論摘要 | 依主題整理，每一條寫清楚是誰的說法 |
| 四、初步共識 | 會中已經同意的事 |
| 五、待確認事項 | 還沒定案的事，以及要向誰確認 |
| 六、行動方案 | 誰負責做什麼、什麼時候完成 |
| 七、其他建議 | 下次會議可以聚焦的事、可以延後的議題 |
| 八、補充資訊 | 會後提供的統計、參考網站、截圖；有額外補充資料才會有此段 |

## 安裝方法

請將 Prompt 貼給 AI，讓他完成安裝：

```
幫我安裝這個會議記錄 skill：https://github.com/miou1107/vin-meeting-minutes-zh
```

## 要用 Google 文件和 Gmail，第一次要先設定

只把逐字稿整理成 Word 檔，裝好就能用。要讓 Claude 建 Google 文件、讀 Gmail 和行事曆、幫你寄信，第一次使用前要先完成 Google 設定。設定的內容是在 Google Cloud 建一組你自己的授權，授權只存在你自己的電腦上。

跟你的 AI 說「幫我設定會議紀錄的 Google 連線」，AI 會一步一步帶你做，每一步都會附上可以直接點的網址。如果公司的 Google 帳號不能自己建 Google Cloud 專案，要請公司 IT 幫忙。

## 初次使用建議

先告訴 Claude 這個專案有哪些人、各自負責什麼。Claude 會把這些存成人員對照，之後每一場都會拿來判斷是誰在講話。沒有這份名單，很多段落 Claude 分不出是誰講的，只能先寫單位，再請你逐段確認。

## 安裝指令（本段是給 AI 的指令，一般人可忽略）

- Claude Code 安裝：`git clone https://github.com/miou1107/vin-meeting-minutes-zh ~/.claude/skills/vin-meeting-minutes-zh`
- Claude Code 更新：`git -C ~/.claude/skills/vin-meeting-minutes-zh pull`
- 使用者自己的設定、詞彙、偏好和 Google 登入都放在 `~/.config/vin-meeting-minutes-zh/`，不放在 skill 資料夾。更新、重裝 skill 都不會動到這些檔案，分享 skill 時也不會帶出去。
- 如果之前裝過舊名稱 meeting-minutes-zh，或更新時出現 unrelated histories 的錯誤，刪掉舊的資料夾再重新安裝。刪之前，先把自己在 `references/glossary.md` 加過的詞搬到 `~/.config/vin-meeting-minutes-zh/glossary.md`：`rm -rf ~/.claude/skills/meeting-minutes-zh ~/.claude/skills/vin-meeting-minutes-zh && git clone https://github.com/miou1107/vin-meeting-minutes-zh ~/.claude/skills/vin-meeting-minutes-zh`
- claude.ai 網頁版：下載這個 repo 的 zip 檔，到設定裡的 Skills 頁面上傳。
