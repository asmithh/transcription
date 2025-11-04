
import argparse
import datetime as dt
import yaml

import librosa
import numpy as np
import soundfile as sf
from transformers import pipeline
from transformers.utils import logging
from webvtt import WebVTT, Caption

def load_config(CONFIG_F):
    # load config file
    try:
        CONFIG = yaml.safe_load(open(CONFIG_F, 'r'))
    except Exception as e:
        print(e)
        raise ValueError('invalid YAML config file')
    return CONFIG

def run_pipeline(INFILE, CONFIG, OUTFILE, filetype='VTT'):

    # loading model; putting it on the GPU
    MODEL = CONFIG['model']
    DEVICE = CONFIG['device']
    asr = pipeline("automatic-speech-recognition", model=MODEL, device=DEVICE)
    asr_sampling_rate = asr.feature_extractor.sampling_rate
    
    # loading and processing raw .mp3 file
    audio, sampling_rate = sf.read(INFILE)
    audio_transposed = np.transpose(audio)
    audio_mono = librosa.to_mono(audio_transposed)
    print('the shape of the audio file is ', audio_mono.shape)
    audio_for_asr = librosa.resample(audio_mono.transpose(), orig_sr = sampling_rate, target_sr= asr_sampling_rate)
    
    # run automatic speech recognition pipeline
    print("beginning transcription; this might take a while without a GPU. please be patient!")
    tr = asr(audio_for_asr, chunk_length_s=30, batch_size=4, return_timestamps=True)['chunks']
    
    if filetype == 'VTT':
        # create new blank VTT object
        vtt = WebVTT()
        for ix, line in enumerate(tr):
            try:
                caption = Caption(
                    format_timestamp(line['timestamp'][0]),
                    format_timestamp(line['timestamp'][1]),
                    line['text'],
                )
            except Exception as e:
                # handle missing timestamp by extrapolating from previous line's timestamp.
                print('this is a warning about an issue with this line, but the program is not broken yet!')
                print(e)
                print('this is the relevant line:')
                print(line)
                print('we will fix this by extrapolating a bit from the timestamp for the previous line')
                caption = Caption(
                    format_timestamp(tr[ix-1]['timestamp'][1] + 1),
                    format_timestamp(tr[ix-1]['timestamp'][1] + 2),
                    line['text']
                )
            vtt.captions.append(caption)
        
        # save final VTT object to .vtt file.
        vtt.save(OUTFILE)
    elif filetype == 'TSV':
        with open(OUTFILE, 'w') as f:
            for line in tr:
                f.write(str(line['timestamp'][0]) + '\t' + str(line['timestamp'][1]) + '\t' + line['text'] + '\n')   

    elif filetype == 'TXT':
        with open(OUTFILE, 'w') as f:
            for line in tr:
                f.write(line['text'] + '\n')
 
def format_timestamp(ts):
    """
    Given a numeric timestamp (seconds since start of the audio file), return a timestamp in the format HH:MM:SS.fff.

    Inputs:
      ts: numeric timestamp tha tindicates seconds since the start of the original audio file.

    Outputs:
      timestamp in the format VTT wants it (string) in HH:MM:SS.fff format (e.g. 01:15:03.256 for 1 hour, 15 min, 3.256 seconds)
    """
    return dt.datetime.strftime(dt.datetime.utcfromtimestamp(ts), '%H:%M:%S.%f')[:-3]

if __name__ == "__main__":
    logging.set_verbosity_error()
    
    parser = argparse.ArgumentParser(
                        prog='transcription via distil-whisper',
                        description='Transcribes a .mp3 file to a transcription w/ timestamps in .vtt format.',
                        )
    parser.add_argument('-i', '--infile', help='the file (hopefully mp3) that you want to transcribe')
    parser.add_argument('-o', '--outfile', help='the filename of your output file (hopefully .vtt)')
    parser.add_argument('-c', '--config', help='the filepath of your configuration file; default is config.yml', default='config.yml')
    
    # parse command line arguments
    args = parser.parse_args()
    INFILE = args.infile
    OUTFILE = args.outfile
    CONFIG_F = args.config

    CONFIG = load_config(CONFIG_F)
    if outfile[-4:] == '.vtt':
        run_pipeline(INFILE, CONFIG, OUTFILE, filetype='VTT')
    elif outfile[-4:] == '.txt':
        run_pipeline(INFILE, CONFIG, OUTFILE, filetype='TXT')
    elif outfile[-4:] == '.tsv':
        print("TSV format is cumbersome, just FYI")
        run_pipeline(INFILE, CONFIG, OUTFILE, filetype='TSV')
    else:
        print("that file extension is not supported as output!")

