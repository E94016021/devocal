import librosa
import lyric_parser
# import matplotlib.pyplot as plt
from numpy import linalg as LA
# import numpy as np
import numpy as np
import npp
from write_arr_mp3 import write_arr_mp3
import scipy
import resampy


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
    print("bg norm = ", a)
    b = LA.norm(mix)
    print("mix norm = ", b)
    vol_ratio = a / b
    # vol_ratio = LA.norm(bg) / LA.norm(mix)
    if vol_ratio == np.nan:
        print("NAN error : set vol_ratio = 1")

        return fine_sample_shift, 1
    else:
        print("     vol_ratio = ", vol_ratio)
        return fine_sample_shift, vol_ratio


def get_vocal(mix_file, bg_file, lyric_file, out_file="out.wav"):
    '''
/Users/LEE/anaconda3/python.app/Contents/MacOS/python /Users/LEE/PycharmProjects/devocal_fac/test_filter.py
deal with ----- /Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/殘酷月光.mp3 -----
start resampling.....mix finish
bg len =  6351864
resample mix sr =  24000 to 44100
mix len =  11669760
bg_res len =  11671551
bg norm =  11.206697
mix norm =  3.7127454
     vol_ratio =  3.0184395
result len =  11671551

Process finished with exit code 0

    :param mix_file:
    :param bg_file:
    :param lyric_file:
    :param out_file:
    :return:
    '''
    print("deal with -----", bg_file, "-----")

    # 讀audio檔
    print("start resampling.....", end='')

    mix, sr_m = librosa.load(mix_file, sr=44100, mono=True)
    print("mix finish ", end='')
    bg, sr_b = librosa.load(bg_file, sr=None, mono=True)
    print("bg len = ", len(bg))
    new_len = int(len(bg) * 44100 / sr_b)
    print("new len = ", new_len)



    print("sr bg = ", sr_b, "  mix = ", sr_m)
    '''

    # bg = librosa.core.resample(bg, sr_b, 44100, 'kaiser_best', fix=True, scale=False)
    # bg = scipy.signal.resample_poly(bg, 44100, sr_b, axis=0, window=('kaiser', 5.0))
    # bg = scipy.signal.resample(bg, new_len, t=None, axis=0, window=None)
    # bg = resampy.resample(bg, sr_b, 44100)

    print("resample mix sr = ", sr_b, "to 44100")

    print("mix len = ", len(mix))
    print("bg_res len = ", len(bg))

    # bg_bytes = bg.tobytes()

    # write_arr_mp3("bg_resample.mp3", bg, sr_b)
    # librosa.output.write_wav("bg_res.wav", bg, sr_b)

    # if sr_m != 44100:
    #     print("resample mix sr = ", sr_m, "to 44100")
    #     mix = librosa.core.resample(mix, sr_m, 44100, res_type='kaiser_best', fix=True, scale=False)
    # if sr_b != 44100:
    #     print("resample bg sr = ", sr_b, "to 44100")
    #     mix = librosa.core.resample(mix, sr_b, 44100, res_type='kaiser_best', fix=True, scale=False)

    # 取得前奏的時間
    l = lyric_parser.Lyric(lyric_file)
    time = l.get_time_before_vocal()

    # 單位變換，從ms換成sample
    time = ms2sample(time - 1000, sr=44100)
    time = time // 2

    # 前處理
    mix = mute_start(mix)
    bg = mute_start(bg)

    # 計算位移，音量
    shift, vol = compute_t_v(mix, bg, time)

    # 前處理
    mix, bg = npp.pad_the_same(mix, bg)
    mix2 = npp.right_shift(mix, shift)

    # 訊號相減
    result = mix2 * vol - bg
    print("result len = ", len(result))

    # try
    # result = mix2*1.5151645 - bg

    # 輸出
    # librosa.output.write_wav(out_file, result, sr=44100)
    write_arr_mp3(out_file, result)
    '''


if __name__ == "__main__":
    get_vocal("/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/48336.mp3",
              "/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/殘酷月光.mp3",
              "/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/104840.lrcx.txt",
              "/Users/LEE/PycharmProjects/devocal_fac/devocal_test/48336殘酷月光/res.mp3")

    # most listen
    get_vocal("test_data/54010小幸運/mix.mp3", "test_data/54010小幸運/back.mp3", "test_data/54010小幸運/54010.txt",
              "test_data/54010小幸運/result.mp3")

    # mix1
    get_vocal("test_data/52888聽見下雨的聲音/mix.mp3","test_data/52888聽見下雨的聲音/back.mp3","test_data/52888聽見下雨的聲音/52888.txt","test_data/52888聽見下雨的聲音/result.wav")
    # # mix2
    get_vocal("test_data/52888聽見下雨的聲音/mix2.mp3","test_data/52888聽見下雨的聲音/back.mp3","test_data/52888聽見下雨的聲音/52888.txt","test_data/52888聽見下雨的聲音/result2.wav")

    # pitch shifted
    get_vocal("test_data/52899算什麼男人/mix.mp3","test_data/52899算什麼男人/back.mp3","test_data/52899算什麼男人/52899.txt","test_data/52899算什麼男人/result.wav")

    # 怪
    get_vocal("test_data/21292給我一個理由忘記/mix.mp3","test_data/21292給我一個理由忘記/back.mp3","test_data/21292給我一個理由忘記/21292.txt","test_data/21292給我一個理由忘記/result.wav")

    # why mix.mp3 only 1:53? GGGGG
    get_vocal("test_data/52890以後別做朋友【原唱版】/mix.mp3","test_data/52890以後別做朋友【原唱版】/back.mp3","test_data/52890以後別做朋友【原唱版】/52890.txt","test_data/52890以後別做朋友【原唱版】/result.wav")

    # android pitch shifted
    get_vocal("test_data/53370默/mix.mp3","test_data/53370默/back.mp3","test_data/53370默/53370.txt","test_data/53370默/result.wav")

    # android not efficient but still -1728 maybe wrong with minus
    get_vocal("test_data/52802可惜沒如果/mix.mp3","test_data/52802可惜沒如果/back.mp3","test_data/52802可惜沒如果/52802.txt","test_data/52802可惜沒如果/result.wav")

    # android
    get_vocal("test_data/52786父親/mix.mp3", "test_data/52786父親/back.mp3", "test_data/52786父親/52786.txt","test_data/52786父親/result.wav")

    # android -30 30 100 小幸運
    get_vocal("test_data/54010小幸運/msShift/-30.mp3", "test_data/54010小幸運/msShift/back.mp3", "test_data/54010小幸運/msShift/54010.txt","test_data/54010小幸運/msShift/result-30.wav")
    get_vocal("test_data/54010小幸運/msShift/30.mp3", "test_data/54010小幸運/msShift/back.mp3", "test_data/54010小幸運/msShift/54010.txt","test_data/54010小幸運/msShift/result30.wav")
    get_vocal("test_data/54010小幸運/msShift/100.mp3", "test_data/54010小幸運/msShift/back.mp3", "test_data/54010小幸運/msShift/54010.txt","test_data/54010小幸運/msShift/result100.wav")
