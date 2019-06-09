# 1.指定されたcsvファイルをスペクトログラム画像に変換するツール

	 << csvファイル仕様 >>
	    time, value  <-- 要Header
	     xx, xx
	     ...


	optional arguments:
	  -h, --help            show this help message and exit
	  --input_csv INPUT_CSV
	                        csvファイル(--input_csv, --input_csv_listまたは--input_csv_dirのいずれかは必ず指定が必要)
	  --input_csv_list INPUT_CSV_LIST
	                        csvファイルリスト(--input_csv, --input_csv_listまたは--input_csv_dirのいずれかは必ず指定が必要)
	  --input_csv_dir INPUT_CSV_DIR
	                        csvファイルが保存されたディレクトリ(--input_csv, --input_csv_listまたは--input_csv_dirのいずれかは必ず指定が必要)
	  --output_dir OUTPUT_DIR
	                        スペクトログラムを出力するディレクトリ
	  --n_fft N_FFT         FFT長
	  --min_freq MIN_FREQ   スペクトログラム出力の最小周波数
	  --max_freq MAX_FREQ   スペクトログラム出力の最大周波数
	  --specgram_mode SPECGRAM_MODE
	                        スペクトログラムの表現形式(psd or magnitude)
	
## 1-1.実行形式ファイルの生成

	make

## 1-2.生成した実行形式ファイルをインストール

デフォルトはMakefileと同じディレクトリにbinディレクトリを生成してインストールする

	make install


