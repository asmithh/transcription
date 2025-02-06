# Transcription via huggingface
Heavily borrows from [this tutorial](https://www.doczamora.com/audio-transcription-from-huggingface-pre-trained-model)

## To run this script:
`INFILE` should be a .mp3 file with your audio you'd like to transcribe.

`OUTFILE` should be a .tsv file that has a name you'll successfully associate with your input audio (`test.tsv` may not be ideal, for example)


## Useful tips:

Note: to transform m4a to mp3: `ffmpeg -i "infile.m4a" -c:v copy -c:a libmp3lame -q:a 4 outf.mp3`

This is intended to run on GPU; running the model on CPU may be much slower. 
