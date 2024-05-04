from scipy.signal import firwin, iirfilter, lfilter

def apply_lowpass_filter(data, samplerate, cutoff_hz=3500.0, numtaps=101):
    # 生成低通FIR滤波器的系数
    fir_coeff = firwin(numtaps, cutoff_hz, fs=samplerate)
    # 应用滤波器
    return lfilter(fir_coeff, [1.0], data)

def apply_highpass_filter(data, samplerate, cutoff_hz=500.0, order=5):
    # 生成高通IIR滤波器的系数
    b, a = iirfilter(order, cutoff_hz, btype='high', ftype='butter', fs=samplerate)
    # 应用滤波器
    return lfilter(b, a, data)

# TODO: frequency
def apply_bandpass_filter(data, samplerate, low_cutoff_hz=600.0, high_cutoff_hz=3300.0, order=5):
    # 生成带通IIR滤波器的系数
    b, a = iirfilter(order, [low_cutoff_hz, high_cutoff_hz], btype='band', ftype='butter', fs=samplerate)
    # 应用滤波器
    return lfilter(b, a, data)

def apply_bandstop_filter(data, samplerate, low_cutoff_hz=1800.0, high_cutoff_hz=2200.0, order=5):
    # 生成带阻IIR滤波器的系数
    b, a = iirfilter(order, [low_cutoff_hz, high_cutoff_hz], btype='bandstop', ftype='butter', fs=samplerate)
    # 应用滤波器
    return lfilter(b, a, data)
