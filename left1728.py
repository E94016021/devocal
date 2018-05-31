import librosa
import lyric_parser
# import matplotlib.pyplot as plt
from numpy import linalg as LA
# import numpy as np
import numpy as np
import npp


def ms2sample(time_ms, sr=44100):
    time_sample = int(round(time_ms / 1000 * sr, 0))
    return time_sample


def mute_start(sig):
    sig[0:1000] = 0
    return sig


def compute_t_v(mix, bg, time):
    mix = mix[:time]
    bg = bg[:time]

    # compute shift
    # fine_sample_shift = npp.find_shift(mix, bg)
    fine_sample_shift = int(-1728)

    # compute volume
    a = LA.norm(bg)
    b = LA.norm(mix)

    vol_ratio = a / b

    print("LA.norm(bg) =", a, "LA.norm(mix) =", b)
    print("vol_ratio =", a / b)

    # vol_ratio = LA.norm(bg) / LA.norm(mix)
    if vol_ratio == np.nan:
        print("NAN error : set vol_ratio = 1")

        return fine_sample_shift, 1
    else:
        print("     vol_ratio = ", vol_ratio)
        return fine_sample_shift, vol_ratio


def get_vocal(mix_file, bg_file, lyric_file, out_file="out.wav"):
    print("-----deal with ---", bg_file, "---")
    # 讀audio檔
    mix, sr_m = librosa.load(mix_file, sr=None)
    bg, sr_b = librosa.load(bg_file, sr=None)

    if sr_m != sr_b:
        new_bg = librosa.resample(bg, sr_b, sr_m)
        librosa.output.write_wav("resample_bg.wav", new_bg, sr_m)

    # sr來囉
    sr = sr_m

    # 取得前奏的時間
    l = lyric_parser.Lyric(lyric_file)
    time = l.get_time_before_vocal()

    # 單位變換，從ms換成sample
    time = ms2sample(time - 1000, sr)
    time = time // 2

    # 前處理
    mix = mute_start(mix)
    # bg = mute_start(bg)
    new_bg = mute_start(new_bg)

    # 計算位移，音量
    # shift, vol = compute_t_v(mix, bg, time)
    shift, vol = compute_t_v(mix, new_bg, time)

    # 前處理
    # mix, bg = npp.pad_the_same(mix, bg)
    # mix2 = npp.right_shift(mix, shift)
    mix, new_bg = npp.pad_the_same(mix, new_bg)
    mix2 = npp.right_shift(mix, shift)

    # 訊號相減
    # result = mix2 * vol - bg

    vol = 3.0184395
    a = mix2
    b = mix2 * vol
    c = new_bg

    result = mix2 * vol - new_bg

    # try
    # result = mix2*1.5151645 - bg

    # 輸出
    librosa.output.write_wav("before_devocal_bg.wav", new_bg, sr)
    librosa.output.write_wav("mix_ratio.wav", mix2 * vol, sr)
    librosa.output.write_wav("result.wav", result, sr)


if __name__ == "__main__":
    get_vocal("/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/48336.mp3",
              "/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/1460590726.mp3",
              "/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/104840.lrcx.txt",
              "/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/resample.wav")

    # most listen
    # get_vocal("devocal_test/54010小幸運/mix.mp3", "devocal_test/54010小幸運/back.mp3", "devocal_test/54010小幸運/54010.txt",
    #           "devocal_test/54010小幸運/result.wav")

    # mix1
    # get_vocal("test_data/52888聽見下雨的聲音/mix.mp3","test_data/52888聽見下雨的聲音/back.mp3","test_data/52888聽見下雨的聲音/52888.txt","test_data/52888聽見下雨的聲音/result.wav")
    # # mix2
    # get_vocal("test_data/52888聽見下雨的聲音/mix2.mp3","test_data/52888聽見下雨的聲音/back.mp3","test_data/52888聽見下雨的聲音/52888.txt","test_data/52888聽見下雨的聲音/result2.wav")

    # pitch shifted
    # get_vocal("test_data/52899算什麼男人/mix.mp3","test_data/52899算什麼男人/back.mp3","test_data/52899算什麼男人/52899.txt","test_data/52899算什麼男人/result.wav")

    # 怪
    # get_vocal("test_data/21292給我一個理由忘記/mix.mp3","test_data/21292給我一個理由忘記/back.mp3","test_data/21292給我一個理由忘記/21292.txt","test_data/21292給我一個理由忘記/result.wav")

    # why mix.mp3 only 1:53? GGGGG
    # get_vocal("test_data/52890以後別做朋友【原唱版】/mix.mp3","test_data/52890以後別做朋友【原唱版】/back.mp3","test_data/52890以後別做朋友【原唱版】/52890.txt","test_data/52890以後別做朋友【原唱版】/result.wav")

    # android pitch shifted
    # get_vocal("test_data/53370默/mix.mp3","test_data/53370默/back.mp3","test_data/53370默/53370.txt","test_data/53370默/result.wav")

    # android not efficient but still -1728 maybe wrong with minus
    # get_vocal("test_data/52802可惜沒如果/mix.mp3","test_data/52802可惜沒如果/back.mp3","test_data/52802可惜沒如果/52802.txt","test_data/52802可惜沒如果/result.wav")

    # android
    # get_vocal("test_data/52786父親/mix.mp3", "test_data/52786父親/back.mp3", "test_data/52786父親/52786.txt","test_data/52786父親/result.wav")

    # android -30 30 100 小幸運
    # get_vocal("test_data/54010小幸運/msShift/-30.mp3", "test_data/54010小幸運/msShift/back.mp3", "test_data/54010小幸運/msShift/54010.txt","test_data/54010小幸運/msShift/result-30.wav")
    # get_vocal("test_data/54010小幸運/msShift/30.mp3", "test_data/54010小幸運/msShift/back.mp3", "test_data/54010小幸運/msShift/54010.txt","test_data/54010小幸運/msShift/result30.wav")
    # get_vocal("test_data/54010小幸運/msShift/100.mp3", "test_data/54010小幸運/msShift/back.mp3", "test_data/54010小幸運/msShift/54010.txt","test_data/54010小幸運/msShift/result100.wav")
