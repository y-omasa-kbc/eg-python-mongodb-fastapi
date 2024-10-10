# 住所録API

このプロジェクトは、FastAPIとMongoDBを使用して、住所録エントリーのCRUD操作（作成、読み取り、更新、削除）を行うAPIです。

## 機能

- 新しい住所録エントリーの作成
- 住所録エントリー全件の取得
- 特定の住所録エントリーの取得
- 特定の住所録エントリーの更新
- 特定の住所録エントリーの削除

## 必要条件

- Python 3.8以上
- MongoDB
- FastAPI
- PyMongo
- Uvicorn (ASGIサーバ)
- dotenv (環境変数管理用)

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/address-book-api.git
cd address-book-api
```

### 2. 仮想環境の作成と有効化（任意）

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windowsの場合
venv\Scripts\activate
# MacOS/Linuxの場合
source venv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
プロジェクトのルートディレクトリにある`.env-sample`をコピーして`.env`を作成します。

`.env` ファイルの内容を、環境に合わせて編集します。
プロジェクトに含まれるdocker-compose.ymlを使用しコンテナ環境でMongoDBを起動する場合、.envファイルの編集は不要です。

### 5. MongoDBの起動

MongoDBがローカルまたはリモートで稼働していることを確認してください。.envファイルは、後述のコンテナ環境用に記述しております。必要に応じて変更してください

MongoDBをコンテナ環境で動かすためのdocker-compose.ymlファイルを含んでいます。.envファイルは、こちらを利用する前提で用意してあります。


### 6. APIの起動

Uvicornを使ってFastAPIサーバを起動します。

```bash
uvicorn main:app --reload
```

- `--reload` オプションを付けることで、コードの変更があった際に自動で再読み込みされます（開発時に便利です）。

### 7. APIへのアクセス

サーバが正常に起動している場合、以下のURLでAPIにアクセスできます。

- ベースURL: `http://localhost:8000`

## APIエンドポイント

APIの詳細な仕様は `doc/addressbook-api.yaml` に記載されています。このファイルを参照して各エンドポイントの詳細な定義を確認してください。

### 主要なエンドポイント

- **POST** `/address/`: 新しい住所録エントリーを作成します。
- **GET** `/address/`: 全ての住所録エントリーを取得します。
- **GET** `/address/{entry_id}`: 特定のIDを持つ住所録エントリーを取得します。
- **PUT** `/address/{entry_id}`: 特定のIDを持つ住所録エントリーを更新します。
- **DELETE** `/address/{entry_id}`: 特定のIDを持つ住所録エントリーを削除します。

## プロジェクト構成

```bash
.
├── main.py                     # FastAPIアプリケーション
├── requirements.txt            # Python依存関係
├── .env                        # 環境変数
├── docker-compose.yml          # MongoDBコンテナ起動用
└── client
    └── webroot                 # テストクライアントを公開するWebサーバコンテナ
        └── index.html          # テストクライアント
├── README.md                   # プロジェクトのドキュメント
└── doc
    └── addressbook-api.yaml    # API仕様のOpenAPIドキュメント
```

## 使用技術

このプロジェクトでは以下のライブラリを使用しています。

- [FastAPI](https://fastapi.tiangolo.com/) - Pythonで高速なAPIを構築するためのWebフレームワーク。
- [PyMongo](https://pymongo.readthedocs.io/en/stable/) - MongoDB用のPythonドライバ。
- [Uvicorn](https://www.uvicorn.org/) - FastAPIに最適なASGIサーバ。
- [dotenv](https://pypi.org/project/python-dotenv/) - `.env` ファイルから環境変数を読み込むライブラリ。

## テストの実行

テストクライアント
docker composeでコンテナを起動後、ブラウザで
[http://localhost:8080](http://localhost:8080)
にアクセスすることで、テスト用クライアントが利用できる。

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。
