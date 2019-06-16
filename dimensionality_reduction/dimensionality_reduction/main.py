#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import glob
import argparse
import cv2
import tqdm
import numpy as np
import pandas as pd
from ryoma_util.graph import graph
from ryoma_ml.dimensionality_reduction import tsne

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------

"""
  関数名: ArgParser
  説明：引数を解析して値を取得する
"""
def ArgParser():
	parser = argparse.ArgumentParser(description='指定されたディレクトリ内の画像群の次元削減を行うツール\n',
			formatter_class=argparse.RawTextHelpFormatter)
	
	# --- 引数を追加 ---
	parser.add_argument('--input_data_dir', dest='input_data_dir', type=str, default=None, required=True, \
			help='画像を格納しているディレクトリ')
	parser.add_argument('--input_data_type', dest='input_data_type', type=str, default=None, required=True, \
			help='入力する画像の拡張子(png, jpg)')
	parser.add_argument('--input_label', dest='input_label', type=str, default=None, required=True, \
			help='各画像のラベルデータ(コンマ(,)区切りのテキストデータ)')
	parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=True, \
			help='出力ディレクトリ')
	parser.add_argument('--output_suffix', dest='output_suffix', type=str, default=None, required=False, \
			help='出力ファイルに付与する接尾語')
	
	args = parser.parse_args()
	
	return args

#---------------------------------
# クラス
#---------------------------------
	
#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	# --- 引数処理 ---
	args = ArgParser()

	# --- 入力画像取得 ---
	input_imgs = glob.glob(os.path.join(args.input_data_dir, '**/*.{}'.format(args.input_data_type)), recursive=True)
	img = cv2.imread(input_imgs[0], cv2.IMREAD_GRAYSCALE)
	img_data = np.array([img.reshape(img.shape[0]*img.shape[1])])
	for input_img in input_imgs[1:]:
		img = cv2.imread(input_img, cv2.IMREAD_GRAYSCALE)
		img_data = np.vstack((img_data, img.reshape(img.shape[0]*img.shape[1])))
	img_data = img_data / 255.0
	print(img_data.shape)

	# --- 入力ラベル取得 ---
	input_labels = pd.read_csv(args.input_label, header=None).values[0]
	print(input_labels)

	# --- 出力ディレクトリ生成 ---
	os.makedirs(args.output_dir, exist_ok=True)

	# --- 次元削減(t-SNE) ---
	perplexities = [0.0, 1.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0, 40.0, 50.0]
	g = graph.Graph()
	for perplexity in tqdm.tqdm(perplexities):
		data_reduced = tsne.tsne(img_data, perplexity=perplexity)
		if (args.output_suffix is not None):
			g.scatter(data_reduced[:, 0], data_reduced[:, 1], label=input_labels, savefile=os.path.join(args.output_dir, 'tsne-perplexity{}-{}.png'.format(perplexity, args.output_suffix)))
		else:
			g.scatter(data_reduced[:, 0], data_reduced[:, 1], label=input_labels, savefile=os.path.join(args.output_dir, 'tsne-perplexity{}.png'.format(perplexity)))

