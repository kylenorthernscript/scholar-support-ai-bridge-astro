# International Research Study Scraper

外国人被験者が関わる臨床研究を自動的に収集・分析するシステム

## 🚀 機能

- **自動スクレイピング**: AMED、JST、JSPS等の研究公募情報を定期収集
- **国際研究識別**: ML + ルールベースのハイブリッド分析
- **多言語対応**: 日本語・英語のキーワードマッチング
- **スコアリング**: 国際性の度合いを数値化
- **データ出力**: JSON/CSV/Excel形式でエクスポート
- **自動化**: Docker + Cronによる定期実行

## 📋 必要条件

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (Dockerで提供)
- Redis (Dockerで提供)

## 🛠️ セットアップ

### 1. リポジトリのクローン

```bash
cd scraper
```

### 2. 環境変数の設定

```bash
cp .env.example .env
# .envファイルを編集して必要な設定を追加
```

### 3. Dockerでの起動

```bash
# 全サービスを起動
docker-compose up -d

# ログを確認
docker-compose logs -f scraper
```

### 4. ローカル開発環境

```bash
# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# スクレイピング実行
python main.py --sources AMED --output excel
```

## 📊 使用方法

### コマンドラインオプション

```bash
python main.py [OPTIONS]

Options:
  --sources    : スクレイピング対象 (AMED, JST, JSPS, ALL)
  --output     : 出力形式 (json, csv, excel)
  --output-dir : 出力ディレクトリ
  --verbose    : 詳細ログ表示
```

### 例

```bash
# AMEDのみをスクレイピングしてExcel出力
python main.py --sources AMED --output excel

# 全サイトをスクレイピングしてJSON出力
python main.py --sources ALL --output json --verbose
```

## 🔍 国際研究の判定基準

### スコアリングシステム

| カテゴリ | ポイント | 説明 |
|---------|---------|------|
| 明示的記載 | 10 | "外国人被験者"等の直接的な記載 |
| 国際プログラム | 8 | ASPIRE、e-ASIA等の国際プログラム |
| 複数国関与 | 7 | 複数国での実施が明記 |
| 多言語対応 | 5 | 複数言語のサポート記載 |
| 翻訳サービス | 5 | 翻訳・通訳の提供記載 |
| 複数規制当局 | 4 | FDA、EMA等の複数当局関与 |
| 暗黙的指標 | 3 | その他の国際性を示唆する要素 |

**閾値**: 8ポイント以上で国際研究として分類

## 📁 出力データ形式

### Excel出力例

- **研究一覧シート**: 
  - 研究ID、タイトル、国際タイプ、スコア、対象国、言語等
- **サマリーシート**: 
  - 総研究数、国際研究数、国際研究率等の統計情報

### JSON出力例

```json
{
  "study_id": "AMED_001",
  "title": "国際共同臨床研究",
  "international_type": "international_collaboration",
  "international_score": 25.0,
  "countries": ["Japan", "USA", "Germany"],
  "languages_supported": ["Japanese", "English", "German"]
}
```

## 🐛 トラブルシューティング

### よくある問題

1. **MeCabエラー**
   ```bash
   # Dockerを使用するか、MeCabをインストール
   sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8
   ```

2. **接続エラー**
   - robots.txtの確認
   - レート制限の調整（config.pyで設定）

3. **メモリ不足**
   - Docker Composeでメモリ制限を調整
   - バッチサイズを小さくする

## 📈 パフォーマンス

- **処理速度**: 約100件/分（レート制限込み）
- **精度**: 国際研究識別精度 約85%
- **メモリ使用**: 最大2GB（ML モデル込み）

## 🔒 セキュリティ

- User-Agentの適切な設定
- robots.txt遵守
- レート制限実装
- 個人情報の非保存

## 📝 ライセンス

本プロジェクトは株式会社シータ・テクノロジーズの内部ツールです。