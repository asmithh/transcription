from transformers.utils import logging
logging.set_verbosity_error()

import soundfile as sf
import io
import numpy as np
import librosa

from transformers import pipeline
import pickle

INFILE = 'FILENAME.mp3'
OUTFILE = 'TRANSCRIBED.tsv'

asr = pipeline("automatic-speech-recognition", model="distil-whisper/distil-medium.en", device=0)
asr_sampling_rate = asr.feature_extractor.sampling_rate
audio, sampling_rate = sf.read(INFILE)

audio_transposed = np.transpose(audio)
audio_mono = librosa.to_mono(audio_transposed)
print(audio_mono.shape)
audio_for_asr = librosa.resample(audio_mono.transpose(), orig_sr = sampling_rate, target_sr= asr_sampling_rate)

tr = asr(audio_for_asr, chunk_length_s=30, batch_size=4, return_timestamps=True)['chunks']

with open(OUTFILE, 'w') as f:
    for line in tr:
        f.write(str(line['timestamp'][0]) + '\t' + str(line['timestamp'][1]) + '\t' + line['text'] + '\n')
