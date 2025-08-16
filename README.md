# 🤖 FAQ Bot

LINEとOpenAIを連携したFAQ自動応答Botです。
社内FAQや顧客サポートに利用可能で、FAQデータベースと大規模言語モデルを組み合わせて、自然で的確な回答を返します。

---

# 📦 セットアップ方法

### 1. 必要環境

* Python 3.10 以上
* pip（Pythonパッケージ管理ツール）
* SQLite3

### 2. リポジトリのクローン

```bash
git clone https://github.com/yourname/faq-bot.git
cd faq-bot
```

### 3. ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env` ファイルをプロジェクト直下に作成し、以下を記入してください：

```env
LINE_CHANNEL_SECRET=xxxxxxxxxxxxxxxxx
LINE_CHANNEL_ACCESS_TOKEN=xxxxxxxxxxxxxxxxx
OPENAI_API_KEY=xxxxxxxxxxxxxxxxx
```

### 5. DB初期化

```bash
python init_db.py
```

### 6. アプリ起動

```bash
python app.py
```

---

# ▶️ 使い方

1. LINE公式アカウントを友だち追加
2. 任意のメッセージを送信
3. FAQ Bot が過去のFAQデータやOpenAIを活用して応答

---

## 📱 動作イメージ

以下のスクリーンショット例をREADMEに追加してください👇

* **起動画面**
  ![screenshot1](docs/images/screenshot1.png) ← ここに `ea596e9e-5d78-458e-8d07-6ae5e1c11ed8.png` を差し込む

* **FAQ応答例1**
  ![screenshot2](docs/images/screenshot2.png) ← ここに `e70f53d5-5990-45e5-ba1a-0c0ad9c8ddb3.png` を差し込む

* **FAQ応答例2**
  ![screenshot3](docs/images/screenshot3.png) ← ここに `02cba021-dfca-45aa-8800-e3eb1997bb17.png` を差し込む

---

# 📂 プロジェクト構成

```
faq-bot/
├── app.py              # メインアプリ
├── init_db.py          # DB初期化スクリプト
├── requirements.txt    # 必要ライブラリ
├── db/                 # SQLite DB
├── static/             # 静的ファイル
├── templates/          # HTMLテンプレート
├── docs/
│   └── images/         # スクリーンショット保存場所
└── README.md
```

---

# 👥 貢献方法

1. Fork & Clone してください
2. 新しいブランチを作成

   ```bash
   git checkout -b feature/my-feature
   ```
3. 修正をコミット

   ```bash
   git commit -m "Add my feature"
   ```
4. Pull Request を送信

---

# 📜 ライセンス

MIT License

---

💡 これをベースにすれば、 **環境構築〜利用方法〜動作イメージ** がすべて一目で分かるREADMEになります。

👉 ご希望なら、この内容を **`README.md` ファイルとして生成** して差し上げましょうか？
