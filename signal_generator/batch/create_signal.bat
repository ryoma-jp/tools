@echo off

rem バッチファイル参考URL
rem   https://jj-blues.com/cms/wantto-changevalueinfor/
rem   https://jj-blues.com/cms/wantto-usearray/

rem パラメータ設定
set fs=8000
set duration=1
set phase[0]=0
set phase[1]=0.196349540849362
set phase[2]=0.392699081698724
set phase[3]=0.589048622548086
set phase[4]=0.785398163397448
set phase[5]=0.98174770424681
set phase[6]=1.17809724509617
set phase[7]=1.37444678594553
set phase[8]=1.5707963267949
set phase[9]=1.76714586764426
set phase[10]=1.96349540849362
set phase[11]=2.15984494934298
set phase[12]=2.35619449019234
set phase[13]=2.55254403104171
set phase[14]=2.74889357189107
set phase[15]=2.94524311274043

rem 出力フォルダ作成
set csv_dir=.\csv
set png_dir=.\png
mkdir %csv_dir%
mkdir %png_dir%

rem 波形生成
setlocal enabledelayedexpansion
set fl=5
:FreqLoop
if !fl! gtr 300 goto EndFreqLoop
echo ----------------
echo !fl!
echo ----------------

set ph=0
set freq=!fl!
:PhaseLoop
call set Phase=%%phase[!ph!]%%
if defined Phase (
	rem 正弦波
	echo [processing] sin, !freq!Hz, !Phase!rad
	set out_csv=%csv_dir%\sin-freq_!freq!Hz-phase_!Phase!.csv
	set out_png=%png_dir%\sin-freq_!freq!Hz-phase_!Phase!.png
	python signal_generator\main.py --type sin --csv !out_csv! --png !out_png! --freq !freq! --fs !fs! --duration !duration! --phase !Phase!

	rem 余弦波
	echo [processing] cos, !freq!Hz, !Phase!rad
	set out_csv=%csv_dir%\cos-freq_!freq!Hz-phase_!Phase!.csv
	set out_png=%png_dir%\cos-freq_!freq!Hz-phase_!Phase!.png
	python signal_generator\main.py --type cos --csv !out_csv! --png !out_png! --freq !freq! --fs !fs! --duration !duration! --phase !Phase!

	rem 三角波
	echo [processing] triangle, !freq!Hz, !Phase!rad
	set out_csv=%csv_dir%\triangle-freq_!freq!Hz-phase_!Phase!.csv
	set out_png=%png_dir%\triangle-freq_!freq!Hz-phase_!Phase!.png
	python signal_generator\main.py --type triangle --csv !out_csv! --png !out_png! --freq !freq! --fs !fs! --duration !duration! --phase !Phase!

	rem 矩形波
	echo [processing] square, !freq!Hz, !Phase!rad
	set out_csv=%csv_dir%\square-freq_!freq!Hz-phase_!Phase!.csv
	set out_png=%png_dir%\square-freq_!freq!Hz-phase_!Phase!.png
	python signal_generator\main.py --type square --csv !out_csv! --png !out_png! --freq !freq! --fs !fs! --duration !duration! --phase !Phase!

	rem 鋸波
	echo [processing] sawtooth, !freq!Hz, !Phase!rad
	set out_csv=%csv_dir%\sawtooth-freq_!freq!Hz-phase_!Phase!.csv
	set out_png=%png_dir%\sawtooth-freq_!freq!Hz-phase_!Phase!.png
	python signal_generator\main.py --type sawtooth --csv !out_csv! --png !out_png! --freq !freq! --fs !fs! --duration !duration! --phase !Phase!

	set /a ph=!ph!+1
	goto PhaseLoop
)

set /a fl = !fl!+5
goto FreqLoop

:EndFreqLoop

endlocal


:End

