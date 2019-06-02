#! -*- coding: utf-8 -*-

"""
  [Signal Generator]
    波形生成ツール
"""

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import sys
import argparse

from ryoma_util.signal_generator import signal_generator

#---------------------------------
# 定数定義
#---------------------------------
FREQ_DEFAULT = 1.0	# 周波数のデフォルト値
FS_DEFAULT = 8000	# サンプリング周波数のデフォルト値
DURATION_DEFAULT = 1.0		# 波形の時間長のデフォルト値

#---------------------------------
# 関数
#---------------------------------

"""
  関数名: ArgParser
  説明：引数を解析して値を取得する
"""
def ArgParser():
	parser = argparse.ArgumentParser(description='引数に応じた波形を生成する', formatter_class=argparse.RawTextHelpFormatter)
	
	# --- 引数を追加 ---
	parser.add_argument('--type', dest='type', type=str, default='random', \
			help='波形の種類 \n'
			'  * 乱数 : random (default) \n'
			'  * 正弦波 : sin \n'
			'  * 余弦波 : cos \n', required=False)
	parser.add_argument('--csv', dest='csv', type=str, default=None, help='出力csvファイル', required=False)
	parser.add_argument('--png', dest='png', type=str, default=None, help='出力pngファイル', required=False)
	parser.add_argument('--freq', dest='freq', type=float, default=FREQ_DEFAULT, \
			help='生成する波形の周波数[Hz](default={}Hz)'.format(FREQ_DEFAULT), required=False)
	parser.add_argument('--fs', dest='fs', type=int, default=FS_DEFAULT, \
			help='生成する波形のサンプリング周波数[Hz](default={}Hz)'.format(FS_DEFAULT), required=False)
	parser.add_argument('--duration', dest='duration', type=float, default=DURATION_DEFAULT, \
			help='生成する波形の長さ[sec](default={}sec)'.format(DURATION_DEFAULT), required=False)
	
	args = parser.parse_args()
	
	return args

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	# --- 引数処理 ---
	args = ArgParser()

	# --- 波形生成 ---
	sg = signal_generator.SignalGenerator(args.csv, args.png, args.freq, args.fs, args.duration)
	if (args.type == 'random'):
		sg.random()
	elif (args.type == 'sin'):
		sg.sin()
	elif (args.type == 'cos'):
		sg.cos()
	elif (args.type == 'triangle'):
		sg.triangle()
	elif (args.type == 'sawtooth'):
		sg.sawtooth()
	elif (args.type == 'square'):
		sg.square()
	else:
		print('[ERROR] unknown type: {}', args.type)


