# Alice Server
 
## プロジェクト開始手順

## プロジェクトのビルド
Dockerのディレクトリで実行
$ docker compose build 


## Djangoプロジェクトの作成
$ docker compose run app django-admin.py startproject Djangoプロジェクト名 .
runコマンドで作成されたコンテナ（UUIDが付帯しているコンテナ名）は削除してもよい。

docker compose run app django-admin.py startproject AliceApp .

docker compose run api django-admin.py startproject AliceAPI .


## プロジェクトの構築
$ docker compose up -d


## MySQL設定
root user: root
root password: a1icer00t%

user: alice
user password: a1icedb% 



## コンテナの中に入る
$ docker compose exec コンテナ名 bash