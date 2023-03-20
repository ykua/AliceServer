# Alice Server
 
## プロジェクト開始手順
コンテナ作成時に初回のみ実行

## プロジェクトのビルド
Dockerのディレクトリで実行
$ docker compose build 

## コンテナの起動
$ docker compose up -d

## MySQL設定
root user: root
root password: a1icer00t%

user: alice
user password: a1icedb% 

## コンテナの中に入る
$ docker compose exec コンテナ名 bash