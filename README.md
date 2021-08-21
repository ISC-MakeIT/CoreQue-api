## 概要
MakeEATのAPIで主に食品データを扱う

## 基本的な開発の進め方
ブランチ命名規則  
https://qiita.com/c6tower/items/fe2aa4ecb78bef69928f  
基本的には `develop` のブランチで  
新しく機能を作りたいときに `feature-hoge` の形でブランチを切る  
機能を実装し終えたら `develop` にマージする  
公開できるようになったら `master` にマージする  

## ブランチ操作コマンド
```bash
# 今あるブランチをすべて表示させる
git branch -a

# ブランチを切るとき
git branch hoge

# ブランチを移動するとき
git checkout hoge
```

マージの時はGitHubからプルリクエストを出す方がやりやすいかも