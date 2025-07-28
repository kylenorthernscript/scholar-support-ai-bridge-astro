# Theta Clinical Support - Claude Code プロジェクト

## 📋 プロジェクト概要

**サービス名**: Theta Clinical Support（シータ・クリニカル・サポート）
**会社名**: 株式会社シータ・テクノロジーズ
**サービス内容**: 臨床研究参加者リクルート・翻訳・事務代行サービス

## 🏗️ 技術スタック

- **フレームワーク**: Astro 5.8.1
- **UI**: React 18.3.1（インタラクティブコンポーネント用）
- **スタイリング**: Tailwind CSS 3.4.11
- **タイポグラフィ**: Inter フォント
- **言語**: TypeScript
- **デプロイ**: Netlify

## 🎨 デザインシステム

### カラーパレット
- **Primary**: Blue系（hsl(235 89% 70%)）
- **Secondary**: Green系（hsl(142 76% 48%)）
- **Accent**: Orange（アイコンアクセント用）
- **Background**: セクション別カラーコーディング

### コンポーネント構成
- **Header**: Reactアイランド（スクロール検知、ダークモードトグル）
- **Hero**: Astroコンポーネント（主要メッセージ）
- **Features**: カードグリッドレイアウト
- **Process**: インフォグラフィックス
- **Contact**: インタラクティブフォーム

## 📱 対応仕様

### レスポンシブブレークポイント
- **Mobile**: ~640px
- **Tablet**: 640px~1024px
- **Desktop**: 1024px~

### アクセシビリティ
- **WCAG AA準拠**
- **キーボードナビゲーション対応**
- **スクリーンリーダー対応**
- **高コントラスト対応**

## 🌐 多言語対応

### 対応言語
- 英語
- 中国語
- スペイン語
- フランス語
- その他多数

## 🚀 開発・デプロイ

### 開発コマンド
```bash
npm run dev          # 開発サーバー起動
npm run build        # 本番ビルド
npm run preview      # ビルド確認
```

### 自動デプロイ
- **GitHub**: https://github.com/kylenorthernscript/scholar-support-ai-bridge-astro
- **Netlify**: 自動デプロイ設定済み

## 📋 開発ガイドライン

### コード品質
1. **TypeScript**: 型安全性を重視
2. **Tailwind**: ユーティリティファーストCSS
3. **Astroパターン**: 静的優先、必要時のみReactアイランド
4. **パフォーマンス**: Core Web Vitals最適化

### ブランドガイドライン
1. **トーン**: プロフェッショナル、信頼性、革新性
2. **メッセージ**: 研究者の本業集中支援
3. **ビジュアル**: クリーン、モダン、アクセシブル

## 🔧 Claude Code利用時の注意事項

### 優先事項
1. **レスポンシブ対応必須**
2. **アクセシビリティ維持**
3. **パフォーマンス最適化**
4. **ブランド一貫性**
5. **SEO対応**

### 禁止事項
- ブランド色の大幅変更
- レスポンシブ対応の破綻
- アクセシビリティの劣化
- 不要な外部依存関係追加

### Git コミットルール
- **重要**: コミットメッセージにClaude Codeを使用していることを示すメッセージ（"🤖 Generated with Claude Code"、"Co-Authored-By: Claude"など）は含めない
- シンプルで明確なコミットメッセージを使用する
- 変更内容を簡潔に説明する

## 📞 コンタクト情報

- **メール**: info@theta-tech.co.jp
- **電話**: 03-1234-5678
- **会社**: 株式会社シータ・テクノロジーズ

## 🔐 GitHub認証設定

Claude Codeから直接GitHubにプッシュするための設定：

### 環境変数設定
```bash
# ~/.zshrcに以下を追加
export GITHUB_TOKEN="your-github-personal-access-token"
```

### セットアップ手順
1. GitHubで[Personal Access Token](https://github.com/settings/tokens)を生成
2. スコープ: `repo`（フルアクセス）を選択
3. トークンを`~/.zshrc`に追加
4. `source ~/.zshrc`で設定を反映

### プッシュ方法
```bash
git push  # 自動的にGITHUB_TOKENが使用されます
```

**注意**: 
- トークンは定期的に更新が必要な場合があります
- トークンは公開リポジトリにコミットしないでください
- 現在このプロジェクトの`~/.zshrc`には既にトークンが設定済みです