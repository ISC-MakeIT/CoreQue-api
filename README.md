## 概要
MakeEATのAPIで主に食品データを扱う

## 開発の進め方
ブランチをmain(master?)から切り離す  
e.g.
```
git branch feature-hoge
git checkout feature-hoge
```
出来上がったら  
コミット、プッシュしてgithubからプルリクを出してください

## terraformで実際に動かして確認するとき
terraform applyする前に
```
build.sh
```
を実行してモジュールをpackageに含める
