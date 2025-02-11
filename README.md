# Transcription via huggingface
Heavily borrows from [this tutorial](https://www.doczamora.com/audio-transcription-from-huggingface-pre-trained-model)

## To run this script:
Make sure you're running this in an environment that has python >= 3.10 and has the packages in `requirements.txt` installed. 

If you're running this on the CoMM Lab machine, you can use the virtual environment that I made a long time ago with much suffering.

Activate it using `source /home/asmithh/gbpn/bin/activate`. 

**PLEASE DO NOT EDIT THIS VIRTUAL ENVIRONMENT ON YOUR OWN**

You can run the script with this syntax:
`python3 transcribe_interview.py -i $INFILE -o $OUTFILE -c $CONFIG_FILE`

`INFILE` should be a .mp3 file with your audio you'd like to transcribe.

`OUTFILE` should be a .tsv file that has a name you'll successfully associate with your input audio (`test.tsv` may not be ideal, for example)

`CONFIG_FILE` is optional; if you don't include a config file it will default to the one that's included with this code. 

### The config file:
Currently specifies which device to use (0 for the main GPU on the CoMM Lab machine; `cpu` for CPU (which I do not recommend)) and which transcription model to use (defaults to `distil-whisper/distil-medium.en`). You can change these settings, but please do so cautiously!!  


## Useful tips:

To transform m4a to mp3, you can use the `ffmpeg` command line utility: `ffmpeg -i "infile.m4a" -c:v copy -c:a libmp3lame -q:a 4 outf.mp3`

This is intended to run on GPU; running the model on CPU may be much slower. 

The `whisper` class of transcription models may hallucinate when given audio without speech; please keep an eye out for this!

## Running on Discovery
### Setup
1. Get a Discovery account using [these instructions](https://rc.northeastern.edu/getting-access/).
2. Go to https://ood.discovery.neu.edu.
3. Click on the "Cluster" tab and then click "Discovery Shell Access".
4. Once you have a terminal window open, request a session: `srun --partition=short --nodes=1 --cpus-per-task=4 --pty /bin/bash`
5. Next, clone this repository and enter its directory (`cd transcription`).
6. Load `conda` (Anaconda, a Python package manager) using this command: `module load anaconda3/2022.05`
7. Create a blank Conda environment: `conda create -y -n NAME python==3.12.1` where `NAME` should be something you'll remember is associated with this project.
8. Activate your Conda environment: `conda activate NAME`
9. Install the necessary packages: `python3 -m pip install -r requirements.txt` (this will take forever).
10. Now we'll open up a GPU session: `srun --partition=gpu --nodes=1 --pty --gres=gpu:1 --ntasks=1 --mem=4GB --time=01:00:00 /bin/bash`
11. Now we'll load CUDA; CUDA is a piece of software that lets Python talk to the GPU: `module load cuda/12.1`
12. Once again, load `conda`: `module load anaconda3/2022.05`
13. And then activate your environment: `conda activate NAME`
