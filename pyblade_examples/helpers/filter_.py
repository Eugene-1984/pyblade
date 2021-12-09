
from scipy.signal import butter, lfilter, decimate


def lpf(s_t, ts, f_cutoff, order=5):

    fs = 1. / ts

    nyq = 0.5 * fs
    normal_cutoff = f_cutoff / nyq

    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    return lfilter(b, a, s_t)


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def bpf(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y