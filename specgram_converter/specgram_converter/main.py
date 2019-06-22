#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import io
import os
import sys
import argparse
import csv
import glob
import struct
import tqdm
import cv2
import numpy as np
import pandas as pd
from scipy import fftpack as sp_fftpack

#---------------------------------
# 定数定義
#---------------------------------
RELATION_CSV_NAME = 'relation.csv'
LABEL_TXT_NAME = 'label.txt'

#---------------------------------
# 関数
#---------------------------------

"""
  関数名: ArgParser
  説明：引数を解析して値を取得する
"""
def ArgParser():
	parser = argparse.ArgumentParser(description='指定されたcsvファイルをスペクトログラム画像に変換するツール\n'
			' << csvファイル仕様 >>\n'
			'    time, value  <-- 要Header\n'
			'     xx, xx\n'
			'     ...', \
			formatter_class=argparse.RawTextHelpFormatter)
	
	# --- 引数を追加 ---
	parser.add_argument('--input_csv', dest='input_csv', type=str, default=None, required=False, \
			help='csvファイル(--input_csv, --input_csv_listまたは--input_csv_dirのいずれかは必ず指定が必要)')
	parser.add_argument('--input_csv_list', dest='input_csv_list', type=str, default=None, required=False, \
			help='csvファイルリスト(--input_csv, --input_csv_listまたは--input_csv_dirのいずれかは必ず指定が必要)')
	parser.add_argument('--input_csv_dir', dest='input_csv_dir', type=str, default=None, required=False, \
			help='csvファイルが保存されたディレクトリ(--input_csv, --input_csv_listまたは--input_csv_dirのいずれかは必ず指定が必要)')
	parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=True, \
			help='スペクトログラムを出力するディレクトリ')
	parser.add_argument('--n_fft', dest='n_fft', type=int, default=1024, required=False, \
			help='FFT長')
	parser.add_argument('--min_freq', dest='min_freq', type=float, default=-1, required=False, \
			help='スペクトログラム出力の最小周波数')
	parser.add_argument('--max_freq', dest='max_freq', type=float, default=-1, required=False, \
			help='スペクトログラム出力の最大周波数')
	parser.add_argument('--specgram_mode', dest='specgram_mode', type=str, default='psd', required=False, \
			help='スペクトログラムの表現形式(psd or magnitude)')
	parser.add_argument('--label_kwd', dest='label_kwd', type=str, default=None, required=False, \
			help='キーワードをもとにラベル付けを行う\n'
				 '入力csvファイル名からキーワードを抽出する為，入力csvにあらかじめ付与しておくこと\n'
				 'ラベル付けされたファイルは{}として出力ディレクトリ以下に格納される'.format(LABEL_TXT_NAME))
	
	args = parser.parse_args()
	
	return args

#---------------------------------
# クラス
#---------------------------------
class CSVtoSpectrogram():
	"""
	コンストラクタ
	"""
	def __init__(self, args):
		# --- パラメータ取り込み ---
		if (args.input_csv is not None):
			# --- csvファイル指定を優先して処理する ---
			self.input_csv = [args.input_csv]
		elif (args.input_csv_list is not None):
			# --- csvファイルリスト ---
			with open(args.input_csv_list, "r") as f:
				self.input_csv = [s.strip() for s in f.readlines()]
		elif (args.input_csv_dir is not None):
			# --- csvディレクトリ指定 ---
			self.input_csv = glob.glob(os.path.join(args.input_csv_dir, '**/*.csv'), recursive=True)
		else:
			# --- 入力csvファイルまたはcsvファイルリストはどちらか指定が必要 ---
			print('[ERROR] --input_csv, --input_csv_listまたは--input_csv_dirのいずれかは必ず指定が必要')
			quit()

		# --- ラベル付けキーワードを抽出 ---
		if (args.label_kwd is None):
			self.label_kwd = None
		else:
			self.label_kwd = pd.read_csv(io.StringIO(args.label_kwd), header=None, skipinitialspace=True).values[0]
		
		# --- 変数値を設定 ---
		self.n_fft = args.n_fft
		self.min_freq = args.min_freq
		self.max_freq = args.max_freq
		self.specgram_mode = args.specgram_mode
		self.output_dir = args.output_dir
		
		# --- 出力ディレクトリを生成 ---
		os.makedirs(self.output_dir, exist_ok=True)
		
		# --- 取り込み情報を表示
		print('[INFO] input_csv')
		print(self.input_csv)
		print('[INFO] output_dir')
		print(self.output_dir)
		
		return
		
	"""
	csvファイルをスペクトログラムに変換
	"""
	def csv_to_specgram(self):
		### csvファイル読み込み ###
		def _load_csv(csv_file):
			df = pd.read_csv(csv_file)
#			print(df.keys())
			time = df[df.keys()[0]].values.astype(float)
			data = df[df.keys()[1]].values.astype(float)
			
			fs = round(1./(time[1]-time[0]), -1)
			duration = time[-1]
			
			return time, data, fs, duration
			
		relation_csv = pd.DataFrame()
		label_txt = []
		for csv_idx, input_csv in enumerate(tqdm.tqdm(self.input_csv)):
			# --- csvファイル読み込み ---
			time, data, fs, duration = _load_csv(input_csv)
			
			# --- 周波数算出 ---
			freq_list = np.array([_f / self.n_fft * fs for _f in range(self.n_fft+1)])
			freq_list[freq_list < 0] += fs
			if (self.min_freq < 0):
				min_freq = 0
			else:
				min_freq = self.min_freq
			if (self.max_freq < 0):
				max_freq = fs / 2
			else:
				max_freq = self.max_freq
			
			# --- 窓関数：ハミング窓 ---
			wnd_vals = 0.54 - 0.46 * np.cos(2.0 * np.pi * np.arange(self.n_fft) / (self.n_fft - 1))
			
			# --- スペクトログラムのFFT bin数算出 ---
			n_bins = len(data) // self.n_fft
			
			# --- FFT bin数分FFTを繰り返す ---
			for n_bin in range(n_bins):
				# --- 入力データ位置を算出 ---
				pos = self.n_fft * n_bin
				_data = data[pos:pos+self.n_fft]
				_data = _data * wnd_vals
				
				# --- FFTを実行 ---
				fft_y = sp_fftpack.fft(_data)
				if (self.specgram_mode == 'magnitude'):
					# magnitude
					fft_y = np.abs(fft_y) / np.abs(wnd_vals).sum()
				else:		# self.specgram_mode == 'psd'
					# psd
					fft_y = (np.conj(fft_y) * fft_y) / fs / (np.abs(wnd_vals)**2).sum()
					slc = slice(1, -1, None)
					fft_y[slc] *= 2.
				fft_ampspectrum = fft_y.real
				
				# --- スペクトログラム作成(FFT結果の積み上げ) ---
				if (n_bin == 0):
					csv_data = freq_list[np.newaxis, 0:self.n_fft//2+1].copy()
					csv_data = np.vstack((csv_data, fft_ampspectrum[0:self.n_fft//2+1].copy())).T
				else:
					csv_data = np.hstack((csv_data, fft_ampspectrum[0:self.n_fft//2+1, np.newaxis].copy()))
			
			# スペクトログラム対象の周波数帯を抽出
			csv_data = np.flipud(csv_data[((freq_list >= min_freq) & (freq_list <= max_freq))[0:self.n_fft//2+1]])
			
			# --- csv出力 ---
			df = pd.DataFrame(csv_data)
			df.to_csv(os.path.join(self.output_dir, 'specgram_{:06d}.csv'.format(csv_idx)))
			
			# --- 画像化(png出力) ---
			bin_data = np.array(((np.clip(10 * np.log(csv_data[:, 1:]), -400, None) / 400) + 1) * 255, dtype=np.uint8)
			cv2.imwrite(os.path.join(self.output_dir, 'specgram_{:06d}.png'.format(csv_idx)), bin_data)
			
			# --- バイナリ出力 ---
			bin_data = bin_data.reshape(bin_data.shape[0] * bin_data.shape[1])
			with open(os.path.join(self.output_dir, 'specgram_{:06d}.bin'.format(csv_idx)), "wb") as fout:
				fout.write(struct.pack(b'B' * len(bin_data), *bin_data))

			# --- 入出力の関連付けを追加 ---
			relation_csv = relation_csv.append([[input_csv, 'specgram_{:06d}'.format(csv_idx)]])

			# --- ラベル抽出 ---
			if (self.label_kwd is not None):
				for label, kwd in enumerate(self.label_kwd):
					if (input_csv.find(kwd) >= 0):
						label_txt.append(label)
						break

		# --- 入出力関連付けファイルを保存 ---
		relation_csv.to_csv(os.path.join(self.output_dir, RELATION_CSV_NAME), index=None, header=['input csv', 'output prefix'])

		# --- ラベル付けファイルを保存 ---
		if (self.label_kwd is not None):
			header = [self.label_kwd[_kwd] for _kwd in label_txt]
			pd.DataFrame([label_txt]).to_csv(os.path.join(self.output_dir, LABEL_TXT_NAME), index=None, header=header)
			
		return
	
	
#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	# --- 引数処理 ---
	args = ArgParser()

	# --- 入力csvをスペクトログラムに変換 ---
	csv2specgram = CSVtoSpectrogram(args)
	csv2specgram.csv_to_specgram()

