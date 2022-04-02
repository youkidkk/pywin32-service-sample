# pywin32-service-sample

pywin32 を使用した Windows サービスのサンプル。

## パッケージのインストール

```shell
pipenv install
pipenv install --dev
```

## ビルド

```shell
pipenv run pyinstaller src/pywin32_sample.py --onefile --clean --hiddenimport win32timezone --hiddenimport win32serviceutil
# -> dist 配下にexeファイルが作成される
```

## サービスのインストール、起動、停止

### フォルダ、ファイル構成

- pyinstaller_sample.exe
- configs
  - log_conf.yml
- logs

### サービスのインストール、起動、停止、アンインストール

管理者としてコマンドプロンプトを起動し、exe ファイルのディレクトリで以下を実行

```shell
# インストール
pywin32_sample install

# 起動
pywin32_sample start

# 停止
pywin32_sample stop

# アンインストール
pywin32_sample remove
```
