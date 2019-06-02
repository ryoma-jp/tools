# 1.波形を生成するツール

	optional arguments:
	  -h, --help           show this help message and exit
	  --type TYPE          波形の種類
	                         * 乱数 : random (default)
	                         * 正弦波 : sin
	                         * 余弦波 : cos
	  --csv CSV            出力csvファイル
	  --png PNG            出力pngファイル
	  --freq FREQ          生成する波形の周波数[Hz](default=1.0Hz)
	  --fs FS              生成する波形のサンプリング周波数[Hz](default=8000Hz)
	  --duration DURATION  生成する波形の長さ[sec](default=1.0sec)

## 1-1.実行形式ファイルの生成

	make

## 1-2.生成した実行形式ファイルをインストール

デフォルトはMakefileと同じディレクトリにbinディレクトリを生成してインストールする

	make install


