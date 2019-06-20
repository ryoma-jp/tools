@echo off

rem バッチファイル参考URL
rem   https://jj-blues.com/cms/wantto-changevalueinfor/
rem   https://jj-blues.com/cms/wantto-usearray/

rem 生成パターン定義
set freq[0]=10
set freq[1]=30
set freq[2]=50
set freq[3]=70
set freq[4]=100
set freq[5]=150
set freq[6]=200
set freq[7]=250
set n_freq=7

rem パラメータ設定
set fs=8000
set duration=20

rem 出力フォルダ作成
set csv_dir=.\csv
set png_dir=.\png
mkdir %csv_dir%
mkdir %png_dir%

rem 波形生成
setlocal enabledelayedexpansion
set /a n=0
for /l %%f in (1, 1, %n_freq%) do (
	echo !freq[%%f]!
	
	rem 正弦波
	echo [processing] sin, !freq[%%f]!Hz
	set out_csv=%csv_dir%\sin-freq_!freq[%%f]!Hz.csv
	set out_png=%png_dir%\sin-freq_!freq[%%f]!Hz.png
	python signal_generator\main.py --type sin --csv !out_csv! --png !out_png! --freq !freq[%%f]! --fs !fs! --duration !duration!

	rem 余弦波
	echo [processing] cos, !freq[%%f]!Hz
	set out_csv=%csv_dir%\cos-freq_!freq[%%f]!Hz.csv
	set out_png=%png_dir%\cos-freq_!freq[%%f]!Hz.png
	python signal_generator\main.py --type cos --csv !out_csv! --png !out_png! --freq !freq[%%f]! --fs !fs! --duration !duration!

	rem 三角波
	echo [processing] triangle, !freq[%%f]!Hz
	set out_csv=%csv_dir%\triangle-freq_!freq[%%f]!Hz.csv
	set out_png=%png_dir%\triangle-freq_!freq[%%f]!Hz.png
	python signal_generator\main.py --type triangle --csv !out_csv! --png !out_png! --freq !freq[%%f]! --fs !fs! --duration !duration!

	rem 矩形波
	echo [processing] square, !freq[%%f]!Hz
	set out_csv=%csv_dir%\square-freq_!freq[%%f]!Hz.csv
	set out_png=%png_dir%\square-freq_!freq[%%f]!Hz.png
	python signal_generator\main.py --type square --csv !out_csv! --png !out_png! --freq !freq[%%f]! --fs !fs! --duration !duration!

	rem 鋸波
	echo [processing] sawtooth, !freq[%%f]!Hz
	set out_csv=%csv_dir%\sawtooth-freq_!freq[%%f]!Hz.csv
	set out_png=%png_dir%\sawtooth-freq_!freq[%%f]!Hz.png
	python signal_generator\main.py --type sawtooth --csv !out_csv! --png !out_png! --freq !freq[%%f]! --fs !fs! --duration !duration!
	
	set /a n=n+1
)



endlocal

