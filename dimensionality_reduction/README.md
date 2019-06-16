# 1.指定されたディレクトリ内の画像群の次元削減を行うツール

	optional arguments:
	  -h, --help            show this help message and exit
	  --input_data_dir INPUT_DATA_DIR
	                        画像を格納しているディレクトリ
	  --input_data_type INPUT_DATA_TYPE
	                        入力する画像の拡張子(png, jpg)
	  --input_label INPUT_LABEL
	                        各画像のラベルデータ(コンマ(,)区切りのテキストデータ)
	  --output_dir OUTPUT_DIR
	                        出力ディレクトリ
	  --output_suffix OUTPUT_SUFFIX
	                        出力ファイルに付与する接尾語
	
## 1-1.実行形式ファイルの生成

	make

※Error発生，デバッグ中．Pythonコマンド経由なら実行可

	python dimensionality_reduction/main.py --help

## 1-2.生成した実行形式ファイルをインストール

デフォルトはMakefileと同じディレクトリにbinディレクトリを生成してインストールする

	make install


