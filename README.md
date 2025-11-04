# Transcription via huggingface
Heavily borrows from [this tutorial](https://www.doczamora.com/audio-transcription-from-huggingface-pre-trained-model)

## Using the GUI
First, make sure you have python >= 3.10 and < 3.14 (>= 3.14 will break because of some deprecated `numba` calls) installed (you can check this by typing `python` or `python3` into your terminal.

Also make sure you have [ffmpeg](https://ffmpeg.org/download.html) installed on your computer if you will be convering .mp4 files to .mp3 files.

Then, [clone this code from GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) and navigate to the directory where the code lives using your terminal [navigating directories for Mac/Linux](https://www.cyberciti.biz/faq/how-to-change-directory-in-linux-terminal/) [navigating directories w/ command prompt](https://www.geeksforgeeks.org/techtips/change-directories-in-command-prompt/)

Finally, unless you know you have an NVIDIA GPU with the proper CUDA drivers installed, run `python3 -m pip install requirements.txt` in your terminal.

To run the program, run `python3 gui.py` and follow the prompts.

## To run the code:
Make sure you're running this in an environment that has python >= 3.10 and has the packages in `requirements.txt` installed. 

If you are running this on a machine with a GPU, please install the packages in `gpu_requirements.txt` instead.

Either way, you will install this using `python3 -m pip install -r requirements.txt` (or `gpu_requirements.txt`). 

If you're running this on the CoMM Lab machine, you can use the virtual environment that I made a long time ago with much suffering.

Activate it using `source /home/asmithh/gbpn/bin/activate`. 

**PLEASE DO NOT EDIT THIS VIRTUAL ENVIRONMENT ON YOUR OWN**

## Output File Types
You can choose from 3 kinds of output files:
VTT (compatible with MAXQDA)
TXT (regular plain text file)
TSV (tab-separated values file with beginning timestamp for utterance, ending timestamp for utterance, and the utterance. most compatible with Excel & friends but a little hard to work with)

To run the command line script:
`python3 transcribe_interview.py -i $INFILE -o $OUTFILE -c $CONFIG_FILE`

`INFILE` should be a .mp3 file with your audio you'd like to transcribe.

`OUTFILE` should be a .tsv, .txt, or .vtt  file that has a name you'll successfully associate with your input audio (`test.tsv` may not be ideal, for example)

`CONFIG_FILE` is optional; if you don't include a config file it will default to the one that's included with this code. 

### The config file:
Currently specifies which device to use (0 for the main GPU on the CoMM Lab machine; `cpu` for CPU (which I do not recommend)) and which transcription model to use (defaults to `distil-whisper/distil-medium.en`). You can change these settings, but please do so cautiously!!  

## Useful tips:

To transform m4a to mp3, you can use the `ffmpeg` command line utility: `ffmpeg -i "infile.m4a" -c:v copy -c:a libmp3lame -q:a 4 outf.mp3`

This is intended to run on GPU; running the model on CPU is much slower (~20 minutes for ~30 minutes of audio on my 2021 M1 Macbook with 16 GB of RAM). 

The `whisper` class of transcription models may hallucinate when given audio without speech; please keep an eye out for this!

You may also see utterances or sentences duplicated in the transcribed text.

## Running on Explorer
### Setup
1. Get a Explorer account using [these instructions](https://rc.northeastern.edu/getting-access/).
2. Go to https://ood.explorer.neu.edu.
3. Click on the "Cluster" tab and then click "Explorer Shell Access".
4. Once you have a terminal window open, request a session: `srun --partition=gpu --nodes=1 --pty --gres=gpu:1 --ntasks=1 --mem=4GB --time=02:00:00 /bin/bash`
5. Next, clone this repository and enter its directory (`cd transcription`). To clone a repository, you can find instructions [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or you can click the green button at the top of this page and choose the `HTTPS` tab. Then click the "copy" icon. 
6. Now we'll load CUDA; CUDA is a piece of software that lets Python talk to the GPU: `module load cuda/12.1`
7. Load `conda` (Anaconda, a Python package manager) using this command: `module load anaconda3/2024.06`
8. Create a blank Conda environment: `conda create -y -n NAME python==3.12.1` where `NAME` should be something you'll remember is associated with this project.
9. Activate your Conda environment: `source activate NAME`
10. Install the necessary packages: `python3 -m pip install -r gpu_requirements.txt` (this will take forever).
11. Back at https://ood.explorer.neu.edu, go to the "Files" tab and open up your home directory. Click the "Upload" button and upload a .mp3 file. Keep track of its name. 
12. The fun part: go back to your terminal window and run `python3 transcribe_interview.py -i ~/INPUT_FILE_NAME -o ~/OUT_FILE_NAME`, where INPUT_FILE_NAME is the name of your input file, and OUT_FILE_NAME is some name for your output file that you'll remember is associated with that input file.

### Transcribing once you're set up:
1. Go to https://ood.explorer.neu.edu.
2. Click on the "Cluster" tab and then click "Explorer Shell Access".
3. Once you have a terminal window open, request a session: `srun --partition=gpu --nodes=1 --pty --gres=gpu:1 --ntasks=1 --mem=4GB --time=02:00:00 /bin/bash`
4. Now we'll load CUDA; CUDA is a piece of software that lets Python talk to the GPU: `module load cuda/12.1`
5. Load `conda` (Anaconda, a Python package manager) using this command: `module load anaconda3/2024.06`
6. Activate your Conda environment: `source activate NAME`
7. Back at https://ood.explorer.neu.edu, go to the "Files" tab and open up your home directory. Click the "Upload" button and upload a .mp3 file. Keep track of its name.
8. The fun part: go back to your terminal window and run `python3 transcribe_interview.py -i ~/INPUT_FILE_NAME -o ~/OUT_FILE_NAME`, where INPUT_FILE_NAME is the name of your input file, and OUT_FILE_NAME is some name for your output file that you'll remember is associated with that input file.
