import csv
import librosa
import os

from concurrent.futures import ProcessPoolExecutor
from left1728 import get_vocal
from shutil import copyfile


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

    # female_ios.csv:   iOS裝置女生唱 照觀看次數排名
    # male_ios.csv:     iOS裝置男生唱 照觀看次數排名

    # local folder name
    local_folder = "copy/"

    print("\nstart Loader")
    # l = Loader("female_ios.csv", "/home/cswu/nas/17sing/song", "/home/cswu/nas/17sing/final_music")
    # l = Loader("female_ios.csv", "/Users/LEE/nas/17sing/song", "/Users/LEE/nas/17sing/final_music")
    l = Loader("male_ios.csv", "/home/slee/nas/music_grp/17sing/song", "/home/slee/nas/music_grp/17sing/final_music")

    print("---Start ProcessPoolExecutor and check missing songs---")

    with ProcessPoolExecutor() as executor:
        i = 0
        print("start for-loop and get_data")
        for bg, mix, sr, lyric in executor.map(get_data, l):
            # TODO: do something here
            print("\nfor", i + 1, "times")

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
            d_out_file = os.path.join("/Users/LEE/PycharmProjects/aiLAB/devocal/result",
                                      l[i].music_id + l[i].music_name + l[i].song_id + ".wav")
            print("path done & start devocal")
            try:
                # get_vocal(mix_file, bg_file, lyric_file, out_file="out.wav")
                # get_vocal(d_mix_file, d_bg_file, d_lyric_file, d_out_file)

                # copy file
                print("file =", d_mix_file.split("/Users/LEE/nas/"))
                copyfile(d_mix_file, local_folder + str(d_mix_file.split("/Users/LEE/nas/")[1]))
                copyfile(d_bg_file, local_folder + str(d_bg_file.split("/Users/LEE/nas/")[1]))
                copyfile(d_lyric_file, local_folder + str(d_lyric_file.split("/Users/LEE/nas/")[1]))
                print("     " + l[i].music_name + " done")
                # 這裡不能插空白
            except FileNotFoundError:
                print("! fileNotFoundError !")
                pass
            except FileExistsError:
                print("! fileExistError !")
                pass

            i += 1
            continue

    # RuntimeWarning: invalid value encountered in sqrt ret = sqrt(sqnorm)
