
import argparse
import yaml

import audio2numpy
import librosa
import numpy as np
from transformers import pipeline
from transformers.utils import logging
logging.set_verbosity_error()

parser = argparse.ArgumentParser(
                    prog='transcription via distil-whisper',
                    description='Transcribes a .mp3 file to a transcription w/ timestamps in .tsv format.',
                    )
parser.add_argument('-i', '--infile', help='the file (hopefully mp3) that you want to transcribe')
parser.add_argument('-o', '--outfile', help='the filename of your output file (hopefully .tsv)')
parser.add_argument('-c', '--config', help='the filepath of your configuration file; default is config.yml', default='config.yml')

args = parser.parse_args()
INFILE = args.infile
OUTFILE = args.outfile
CONFIG_F = args.config
try:
    CONFIG = yaml.safe_load(open(CONFIG_F, 'r'))
except Exception as e:
    print(e)
    raise ValueError('invalid YAML config file')

MODEL = CONFIG['model']
DEVICE = CONFIG['device']

asr = pipeline("automatic-speech-recognition", model=MODEL, device=DEVICE)
asr_sampling_rate = asr.feature_extractor.sampling_rate
audio, sampling_rate = audio2numpy.audio_from_file(INFILE)

audio_transposed = np.transpose(audio)
audio_mono = librosa.to_mono(audio_transposed)
print(audio_mono.shape)
audio_for_asr = librosa.resample(audio_mono.transpose(), orig_sr = sampling_rate, target_sr= asr_sampling_rate)

tr = asr(audio_for_asr, chunk_length_s=30, batch_size=4, return_timestamps=True)['chunks']

with open(OUTFILE, 'w') as f:
    for line in tr:
        f.write(str(line['timestamp'][0]) + '\t' + str(line['timestamp'][1]) + '\t' + line['text'] + '\n')
