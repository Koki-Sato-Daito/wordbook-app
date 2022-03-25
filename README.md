## 概要

『ITエンジニアのための英単語テスト』がテーマのアプリケーションです。Python, Javaそれぞれの公式ドキュメントで高い頻度で出現する英単語を出題することで実践的な英単語の習得を目的としています。


## ホスト先のURL

- https://it-engineer-english.com/


## 使用した技術と機能一覧

### 技術スタック

- Django REST frameworkでAPIサーバを構築
- Nuxt.jsでWEBクライアントを構築
- Digital OceanのUbuntu Server Droplet(サーバインスタンス)にNginxを導入し、APIサーバはリバースプロキシ、WEBクライアントは静的ファイルとして配信
- データベースはPostgreSQL
- 開発環境はDockerのPythonイメージ、PostgreSQLイメージ、Node.jsイメージから簡単に構築可能
- 単語データの取得には[こちら(自分で作りました！)](https://github.com/Koki-Sato-Daito/wordbook_generator)のアプリケーションを使用


### 機能一覧

#### APIサーバ

- Django REST Framework標準のトークン認証とdjoserライブラリでエンドポイント生成
- Django Adminで単語の登録をするための管理ページ、django-import-exportライブラリでcsvファイルから一括でデータをインポート
- マスターデータ(単語、進捗データ、間違った問題リスト)用のエンドポイント
- 学習進捗の保存用のエンドポイント
- 間違った問題を記録するエンドポイント


#### WEBクライアント

- 認証トークン、ユーザ情報はvuex-persistedstateでlocalStorageに格納
- トップページ
- ログイン、ログアウト、ユーザ登録ページ
- テスト(試験)ページ
- コンポーネントは、要素とスタイリングを記述したPresentationalsコンポーネントと、共通のビジネスロジックを記述したContainersコンポーネントに分割した。原則としてPage->Containers->Presentationalsの順に親コンポーネントから利用するように設計
- コンポーネント間はProps、$emitで連携


## ポートフォリオ作成背景、目的

- 大学のゼミで簡単な自然言語処理を行っていたため、その知見を活かしたアプリケーションを作れないかと思い作成しました。
- 英語学習をテーマに扱っていますが、これは、自分がプログラミングや新しい技術を学習しているときに、英語のドキュメントを曲がりなりにも解釈したり、正しい英単語を使って識別子をつけたりという行為を何度も繰り返していることに気づいて、英語学習の優先順位の高さや汎用性を実感したためです。
- それから、ITという文脈ではどんな英単語の出現頻度が高いのかが気になって単語の分析をしてみたいという知的好奇心も大きく自分をモチベートしました。


## ポートフォリオ作成で役に立ったこと

- 実装することで完成形に近づいているという直感とは裏腹に、考慮するべき点が同時に指数関数的に増加しているという感覚が新鮮でした。例えば、一つだけ機能を追加しようと考えて手を動かした結果、『その過程でこの機能が必要だ』とか『とりあえず動くものができたけど、ここで例外が出たらどうするか、データを検証しなくては』など、プラスで考慮しなくてはいけないことがいくつも出てきました。ここからシステムを事前に網羅的に設計することの難しさを学びました。
- 初めて触る技術が多い中、実装中のデグレーションにそこまで絶望せずに済んだのはユニットテストによる恩恵でした。また、初めて触る技術に対して『使い方を学んで、どのように導入するのか』という自分流のフローの輪郭は見えてき多様に思います。
- やみくもにコードを書き始めるのではなく『どうやったら機能を実現できるか』『どのようにやるのか』というような段取りを言語化したメモを先に書くと捗ることを学んだ。


## 使い方

- クローン

```
$ https://github.com/Koki-Sato-Daito/wordbook-app.git
$ cd wordbook-app
```

- 環境変数の設定。シークレットキーには[こちら](https://miniwebtool.com/ja/django-secret-key-generator/)がおすすめです。

```
$ vi.env
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGIN_WHITELIST=http://localhost:3000
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_HOST=db
DB_PORT=5432

$ vi frontend/.env
BASE_URL=http://localhost:8000
```

- dockerコンテナ構築と起動

```
$ docker-compose up --build -d
```

- マイグレーション、管理アカウント作成

```
$ docker-compose exec web python3 manage.py migrate --settings=config.settings.development
$ docker-compose exec web python3 manage.py createsuperuser --settings=config.settings.development
```

- http://localhost:3000にアクセス可能できます。
- 単語データはhttp://localhost:8000/adminで追加します。
