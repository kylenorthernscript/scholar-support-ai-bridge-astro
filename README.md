# Theta Clinical Support

## 📋 プロジェクト概要

**サービス名**: Theta Clinical Support（シータ・クリニカル・サポート）  
**会社名**: 株式会社シータ・テクノロジーズ  
**サービス内容**: 臨床研究参加者リクルート・翻訳・事務代行サービス

臨床研究者の本業への集中を支援するため、AI技術を活用した効率的な研究サポートサービスを提供しています。

## 🚀 主な機能

- **参加者リクルート**: AIを活用した効率的な研究参加者の募集・スクリーニング
- **多言語翻訳**: 英語、中国語、スペイン語、フランス語など多数の言語に対応
- **事務代行**: 書類作成、データ入力、スケジュール管理などの研究事務全般

## 🏗️ 技術スタック

- **フレームワーク**: [Astro](https://astro.build/) 5.8.1
- **UI**: React 18.3.1（インタラクティブコンポーネント用）
- **スタイリング**: Tailwind CSS 3.4.11
- **言語**: TypeScript
- **デプロイ**: Netlify

## 📂 プロジェクト構成

```text
/
├── public/
│   ├── favicon.svg
│   └── logo.svg
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── HeroSection.astro
│   │   ├── FeaturesSection.astro
│   │   ├── ProcessSection.astro
│   │   ├── ContactSection.astro
│   │   ├── Footer.astro
│   │   └── chatbot/
│   ├── layouts/
│   │   └── Layout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── contact-success.astro
│   │   └── landing/
│   └── styles/
│       └── global.css
├── package.json
└── astro.config.mjs
```

## 🧞 開発コマンド

プロジェクトのルートディレクトリから以下のコマンドを実行：

| コマンド | 説明 |
| :--- | :--- |
| `npm install` | 依存関係のインストール |
| `npm run dev` | 開発サーバー起動（`localhost:4321`） |
| `npm run build` | 本番用ビルド（`./dist/`） |
| `npm run preview` | ビルドのプレビュー |

## 🎨 デザインシステム

### カラーパレット
- **Primary**: Blue系（hsl(235 89% 70%)）
- **Secondary**: Green系（hsl(142 76% 48%)）
- **Accent**: Orange（アイコンアクセント用）

### レスポンシブ対応
- Mobile: ~640px
- Tablet: 640px~1024px
- Desktop: 1024px~

### アクセシビリティ
- WCAG AA準拠
- キーボードナビゲーション対応
- スクリーンリーダー対応

## 🌐 多言語対応

以下の言語に対応：
- 英語
- 中国語
- スペイン語
- フランス語
- その他多数

## 📞 お問い合わせ

- **メール**: info@thetaclinical.com
- **会社**: 株式会社シータ・テクノロジーズ

## 📄 ライセンス

© 2025 シータ・テクノロジーズ. All rights reserved.