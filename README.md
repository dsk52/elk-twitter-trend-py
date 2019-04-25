# elk-twitter-trend-py

以下の記事を写経したやつ。コードはそのままだとうまく動かなかったのでちょっと変えてある。

[ElasticsearchとKibanaを使ってTwitterのトレンドワードを可視化してみた - Qiita](http://qiita.com/yoppe/items/3e61fd567ae1d4c40a96)

## Env

- Docker
    - Elasticsearch v5.5.1
    - Kibana v5.5.1
- Python3
    - flake8

## Setting Env
### Docker

```
$ docker pull nshou/elasticsearch-kibana
```

### Python

```
<<<<<<< HEAD
$ python3 -m venv venv
$ source venv/bin/activate.fish
=======
$ source ./bin/activate
>>>>>>> 19082c80c5387fc52740cf074dee17afd6eea03a
$ pip install -r requirements.txt
```

### Twitter Appの作成
[TwitterのDevelopper](https://apps.twitter.com/)ページでAppを作成し、アクセストークンなどを作成する必要があります。
取得したアクセストークンなどは、 ``.env.sample`` を参考に ``.env`` をルートディレクトリに作成してください。


### Start
Dockerを立ち上げた状態で、Pythonのスクリプトを走らせます。

```
$ docker run -d --name elk-twitter-trend -p 9200:9200 -p 5601:5601 nshou/elasticsearch-kibana
```

```
$ python trend_stream.py
```

<<<<<<< HEAD
Access http://localhost:5601
=======
>>>>>>> 19082c80c5387fc52740cf074dee17afd6eea03a
