@echo off

rem バッチファイル参考URL
rem   https://jj-blues.com/cms/wantto-changevalueinfor/
rem   https://jj-blues.com/cms/wantto-usearray/

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
for /l %%f in (5, 5, 300) do (
	echo %%f
	
	rem 正弦波
	echo [processing] sin, %%fHz
	set out_csv=%csv_dir%\sin-freq_%%fHz.csv
	set out_png=%png_dir%\sin-freq_%%fHz.png
	python signal_generator\main.py --type sin --csv !out_csv! --png !out_png! --freq %%f --fs !fs! --duration !duration!

	rem 余弦波
	echo [processing] cos, %%fHz
	set out_csv=%csv_dir%\cos-freq_%%fHz.csv
	set out_png=%png_dir%\cos-freq_%%fHz.png
	python signal_generator\main.py --type cos --csv !out_csv! --png !out_png! --freq %%f --fs !fs! --duration !duration!

	rem 三角波
	echo [processing] triangle, %%fHz
	set out_csv=%csv_dir%\triangle-freq_%%fHz.csv
	set out_png=%png_dir%\triangle-freq_%%fHz.png
	python signal_generator\main.py --type triangle --csv !out_csv! --png !out_png! --freq %%f --fs !fs! --duration !duration!

	rem 矩形波
	echo [processing] square, %%fHz
	set out_csv=%csv_dir%\square-freq_%%fHz.csv
	set out_png=%png_dir%\square-freq_%%fHz.png
	python signal_generator\main.py --type square --csv !out_csv! --png !out_png! --freq %%f --fs !fs! --duration !duration!

	rem 鋸波
	echo [processing] sawtooth, %%fHz
	set out_csv=%csv_dir%\sawtooth-freq_%%fHz.csv
	set out_png=%png_dir%\sawtooth-freq_%%fHz.png
	python signal_generator\main.py --type sawtooth --csv !out_csv! --png !out_png! --freq %%f --fs !fs! --duration !duration!
	
	set /a n=n+1
)



endlocal

