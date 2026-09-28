import numpy as np

def avg_freq_pwr(data):
    weighted_power = 0
    sum_power = 0

    for index, sample in enumerate(data):
        weighted_power += index * float(sample)
        sum_power += float(sample)

    if len(data) <= 0:
        return 0

    if sum_power == 0:
        return 0

    return weighted_power / float(sum_power)


def estimate(spectrum, thr):
    spectrum = np.append(spectrum, np.zeros(1))
    length = len(spectrum)

    channels = []
    lnbins = []
    bins = []

    index = 0
    while index < length:
        if spectrum[index] > thr:
            bins.append(spectrum[index])
            index += 1

        elif len(bins) > 5:
            avg_freq = avg_freq_pwr(bins)
            channels.append(index - len(bins) + avg_freq)
            lnbins.append(len(bins))
            index += 1
            bins = []

        else:
            index += 1
            bins = [] 

    return channels, lnbins


channels = []
lnbin = []
ret = [0, 0]
channel_spacing = 0.0005


def detect(data, fs, thr, freq):
    print("detecting .....")

    global channels, lnbin, ret, channel_spacing

    try:
        spectrum = np.array([float(x) for x in data])

        channels, lnbin = estimate(spectrum, thr)

        channels = np.array(channels)
        lnbin = np.array(lnbin)

        if len(channels) > 0:
            resolution = fs / len(spectrum)

            channels = (channels - len(spectrum) / 2) * resolution
            channels = np.round(channels / channel_spacing) * channel_spacing

            print(channels, lnbin)

            tmpf = []
            for ch in channels:
                tuned_channels = np.round((ch + freq * 1e6), 3)
                tmpf.append(tuned_channels)

            channels = tmpf
            ret = [channels[0] / 1e6, lnbin[0]]

        else:
            ret = [0, 0]

    except Exception as e:
        print("ERROR:", e)

    print(ret)
    return ret