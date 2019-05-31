# 1.Pythonツールのサンプル

Pythonプログラムを単一の実行形式ファイルにする(ツール化する)サンプル

## 1-1.ファイル構成

	sample/
	  ├─ README.md
	  ├─ Makefile
	  └─ sample/
	      ├─ sample.py
	      └─ submodule.py

### README.md

本ファイル

### Makefile

Pythonコードをコンパイルして実行形式ファイルを生成するスクリプト

#### sample/

実行形式にするコード

## 1-2.実行形式ファイルの生成

	make

## 1-3.生成した実行形式ファイルをインストール

デフォルトはMakefileと同じディレクトリにbinディレクトリを生成してインストールする

	make install


