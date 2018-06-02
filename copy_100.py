import csv
import librosa
import os

from concurrent.futures import ProcessPoolExecutor
from left1728 import get_vocal
# from shutil import copy

import shutil


# song informations
class Song:

    def __init__(self, song_id, music_name, music_id, bg_path, song_path, lyric_path):
        self.song_id, self.music_name, self.music_id, self.bg_path, self.song_path, self.lyric_path = \
            song_id, music_name, music_id, bg_path, song_path, lyric_path


# data loader
class Loader:
    def __init__(self, csv_path, song_path, music_path):
        self.csv_path = csv_path
        self.song_path = song_path
        self.music_path = music_path

        self.data = []
        with open(csv_path, 'r', encoding='utf8') as f:
            rows = csv.reader(f)

            for row in rows:
                self.data.append(row)

        self.header = self.data[0]
        self.data = self.data[1:]  # skip header

    def __getitem__(self, idx):
        song_id = self.data[idx][0]
        music_name = self.data[idx][1]
        music_id = self.data[idx][12]
        bg_path = os.path.join(self.music_path, music_id + "-" + music_name, music_name + ".mp3")
        song_path = os.path.join(self.song_path, music_id + "-" + music_name, song_id + ".mp3")
        lyric_path = os.path.join(self.music_path, music_id + "-" + music_name, music_name + ".lyrc")

        return Song(song_id, music_name, music_id, bg_path, song_path, lyric_path)


# load data to numpy array
def get_data(s: Song):
    try:
        bg, sr = librosa.load(s.bg_path)
        mix, sr = librosa.load(s.song_path)
        f = open(s.lyric_path, 'r', encoding="utf-8")
        lyric = f.readlines()  # TODO: <-------這個你要自己用lyric Parser讀 如果你要算前奏時間的話

    # incase file is missing
    except FileNotFoundError as e:
        print(e)
        return None, None, None, None

    return bg, mix, sr, lyric


if __name__ == "__main__":

    finish = 0

    print("\nstart Loader")
    l = Loader("male_ios.csv", "/Users/LEE/nas/music_grp/17sing/song", "/Users/LEE/nas/music_grp/17sing/final_music")
    print("---Start ProcessPoolExecutor and check missing songs---")

    with ProcessPoolExecutor(max_workers=4) as executor:
        i = 0
        print("start for-loop and get_data")
        for bg, mix, sr, lyric in executor.map(get_data, l):
            # TODO: do something here
            print("\nfor", i + 1, "times")

            if finish >= 100:
                break

            lp = l[i].lyric_path

            mp = l.music_path
            mn = l[i].music_name
            mi = l[i].music_id

            sp = l.song_path
            sn = l[i].music_name
            si = l[i].song_id

            d_mix_file = os.path.join(sp, mi + "-" + sn, si + ".mp3")
            d_bg_file = os.path.join(mp, mi + "-" + mn, mn + ".mp3")
            d_lyric_file = lp

            src_mix_folder = os.path.join(sp, mi + "-" + sn)
            src_bg_folder = os.path.join(mp, mi + "-" + mn)
            src_lyric_folder = src_bg_folder

            src_mix_file = d_mix_file
            src_bg_file = d_bg_file
            src_lyric_file = d_lyric_file

            dst_mix_folder = "." + src_mix_folder.split("/Users/LEE/nas/music_grp")[1]
            dst_bg_folder = "." + src_bg_folder.split("/Users/LEE/nas/music_grp")[1]
            dst_lyric_folder = "." + src_lyric_folder.split("/Users/LEE/nas/music_grp")[1]

            dst_mix_file = os.path.join(dst_mix_folder, si + ".mp3")
            dst_bg_file = os.path.join(dst_bg_folder, mn + ".mp3")
            dst_lyric_file = os.path.join(dst_bg_folder, mn + ".lyrc")

            print("path done & start devocal")
            try:
                print(".")
                os.makedirs(dst_mix_folder, mode=0o777, exist_ok=True)
                os.makedirs(dst_bg_folder, mode=0o777, exist_ok=True)
                # same as bg
                # os.makedirs(dst_lyric_folder, exist_ok=True)
                print("makedir done")

                cmd1 = "cp " + src_mix_file + " " + dst_mix_file
                os.system(cmd1)
                print(cmd1)

                cmd2 = "cp " + src_bg_file + " " + dst_bg_file
                os.system(cmd2)
                print(cmd2)

                cmd3 = "cp " + src_lyric_file + " " + dst_lyric_file
                os.system(cmd3)
                print(cmd3+"\n\n")

                finish += 1

                # 這裡不能插空白
            except FileNotFoundError as e:
                print(e)
                pass
            except FileExistsError as e:
                print(e)
                pass
            except Exception as e:
                print(e)
                pass

            i += 1
            continue

