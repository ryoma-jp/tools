#! /bin/bash

# optional arguments for signal generator:
#   -h, --help           show this help message and exit
#   --type TYPE          波形の種類
#                          * 乱数 : random (default)
#                          * 正弦波 : sin
#                          * 余弦波 : cos
#                          * 三角波 : triangle
#                          * 矩形波 : square
#                          * 鋸波   : sawtooth
#   --csv CSV            出力csvファイル
#   --png PNG            出力pngファイル
#   --freq FREQ          生成する波形の周波数[Hz](default=1.0Hz)
#   --fs FS              生成する波形のサンプリング周波数[Hz](default=8000Hz)
#   --duration DURATION  生成する波形の長さ[sec](default=1.0sec)

# パス定義
exe="bin/signal_generator"

# 生成パターン定義
freq=(10 30 50 70 100 150 200 250)
fs=8000
duration=5

# 出力ディレクトリ作成
csv_dir='./csv'
png_dir='./png'
mkdir -p ${csv_dir}
mkdir -p ${png_dir}

# 波形生成
for _freq in ${freq[@]}
do
	# 正弦波
	echo "[processing] sin, ${_freq}Hz"
	out_csv="${csv_dir}/sin-freq_${_freq}Hz.csv"
	out_png="${png_dir}/sin-freq_${_freq}Hz.png"
	${exe} --type sin --csv ${out_csv} --png ${out_png} --freq ${_freq} --fs ${fs} --duration ${duration}

	# 余弦波
	echo "[processing] cos, ${_freq}Hz"
	out_csv="${csv_dir}/cos-freq_${_freq}Hz.csv"
	out_png="${png_dir}/cos-freq_${_freq}Hz.png"
	${exe} --type cos --csv ${out_csv} --png ${out_png} --freq ${_freq} --fs ${fs} --duration ${duration}

	# 三角波
	echo "[processing] triangle, ${_freq}Hz"
	out_csv="${csv_dir}/triangle-freq_${_freq}Hz.csv"
	out_png="${png_dir}/triangle-freq_${_freq}Hz.png"
	${exe} --type triangle --csv ${out_csv} --png ${out_png} --freq ${_freq} --fs ${fs} --duration ${duration}

	# 矩形波
	echo "[processing] square, ${_freq}Hz"
	out_csv="${csv_dir}/square-freq_${_freq}Hz.csv"
	out_png="${png_dir}/square-freq_${_freq}Hz.png"
	${exe} --type square --csv ${out_csv} --png ${out_png} --freq ${_freq} --fs ${fs} --duration ${duration}

	# 鋸波
	echo "[processing] sawtooth, ${_freq}Hz"
	out_csv="${csv_dir}/sawtooth-freq_${_freq}Hz.csv"
	out_png="${png_dir}/sawtooth-freq_${_freq}Hz.png"
	${exe} --type sawtooth --csv ${out_csv} --png ${out_png} --freq ${_freq} --fs ${fs} --duration ${duration}

done



