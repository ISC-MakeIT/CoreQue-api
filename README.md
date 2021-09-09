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

## pipenv
ライブラリを使うときとか
### 依存関係の追加  
```
pipenv install hoge
```
開発用の依存関係の場合
```
pipenv install --dev hoge
```
### 依存関係の削除
```
pipenv uninstall hoge
pipenv clean
```
### パッケージを読み込めないときとか
```
pipenv --venv
```
で環境が合っているか確認(Select Interpreter)

## terraform
環境をデプロイするときとか
### 現在の環境を適用する
```
terraform apply
```
### 現在の環境を破棄する
```
terraform destroy
```