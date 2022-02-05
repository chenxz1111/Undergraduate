import librosa
import numpy as np
from scipy import signal
import soundfile
import os
from pathlib import Path

WAV_NUN = 4
SAMPLE_RATE = 8000
FILTER_FREQ = 3400
DURATION = 30

os.makedirs('output', exist_ok=True)

def wav_read():
    wavs = []
    for i in range(WAV_NUN):
        # 预处理
        raw_data, ori_sample_rate = librosa.load(f'./data/{i + 1}.wav', duration=DURATION)
        b, a = signal.butter(10, FILTER_FREQ, fs=ori_sample_rate)
        filted_data = signal.filtfilt(b, a, raw_data)
        resample_data = librosa.resample(filted_data, ori_sample_rate, SAMPLE_RATE)
        wavs.append(resample_data)
    return wavs

def wav_save(path, wavs):
    for i in range(WAV_NUN):
        soundfile.write(os.path.join(path, f'decode_{i + 1}.wav'), wavs[i], SAMPLE_RATE)

def wav_merge(wavs, num):
    res = []
    index = 0
    while index < len(wavs):
        single = []
        for _ in range(num):
            single.append(wavs[index])
            index += 1
        res.append(np.concatenate(single))
    return res

wav_4 = wav_read()
# Path("output/preprocess").mkdir(parents=True, exist_ok=True)
# wav_save(os.path.join('output', 'preprocess'), wav_4)

for frame_len in [1, 2, 5, 10, 30]:
    frame_num = DURATION // frame_len
    frame_tot = WAV_NUN * frame_num
    frame_feq = frame_len * SAMPLE_RATE
    path = os.path.join('output', f'N={frame_len}')
    Path(path).mkdir(parents=True, exist_ok=True)
    
    encode_wav = []
    for j in range(frame_num):
        for i in range(WAV_NUN):
            encode_wav.append(wav_4[i][(j * frame_feq):((j + 1) * frame_feq)])

    fd_value = [np.fft.fft(wav) for wav in encode_wav]
    # 滤波, 并对f(0)和f(N/2)保留来计算共轭
    fd_len = SAMPLE_RATE * frame_len // 2 + 1
    fd_left = [fd[: fd_len] for fd in fd_value]
    fd_left = np.concatenate(fd_left)
    zero_num = 48000 * DURATION - 2 * len(fd_left) - 1
    zero_arr = np.zeros(zero_num)
    zero_one = np.zeros(1)
    # 计算共轭并拼接
    fd = np.concatenate((zero_one, fd_left, zero_arr, fd_left.conjugate()[::-1]))
    # 验证 fd 长度为 48000 * DURATION
    # print(len(fd))
    y = np.fft.ifft(fd).real
    # 验证 ifft 后虚部全为 0
    # print(np.fft.ifft(fd).imag)
    soundfile.write(os.path.join(path, 'encode.wav'), y, 48000)
    fd = np.fft.fft(y)

    decode_wavs = []
    for i in range(WAV_NUN):
        for j in range(frame_num):
            wav = fd[(j * WAV_NUN + i) * fd_len + 1 : ((j * WAV_NUN + i + 1)) * fd_len + 1]
            wav = np.concatenate((wav, wav.conjugate()[-2:0:-1]))
            # 验证其共轭对称
            # print(wav[1], wav[-1])
            decode_wavs.append(wav)

    save_wavs = []
    for wav in decode_wavs:
        save_wavs.append(np.fft.ifft(wav).real)
    save_wavs = wav_merge(save_wavs, frame_num)
    wav_save(path, save_wavs)
    