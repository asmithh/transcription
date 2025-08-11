# Transcription via huggingface
Heavily borrows from [this tutorial](https://www.doczamora.com/audio-transcription-from-huggingface-pre-trained-model)

## To run this code:
Make sure you're running this in an environment that has python >= 3.10 and has the packages in `requirements.txt` installed. 

If you're running this on the CoMM Lab machine, you can use the virtual environment that I made a long time ago with much suffering.

Activate it using `source /home/asmithh/gbpn/bin/activate`. 

**PLEASE DO NOT EDIT THIS VIRTUAL ENVIRONMENT ON YOUR OWN**

### TSV version:
You can run the script with this syntax:
`python3 transcribe_interview.py -i $INFILE -o $OUTFILE -c $CONFIG_FILE`

`INFILE` should be a .mp3 file with your audio you'd like to transcribe.

`OUTFILE` should be a .tsv file that has a name you'll successfully associate with your input audio (`test.tsv` may not be ideal, for example)

`CONFIG_FILE` is optional; if you don't include a config file it will default to the one that's included with this code. 

### VTT version:
You can run the script with this syntax:
`python3 vtt_transcribe_interview.py -i $INFILE -o $OUTFILE -c $CONFIG_FILE`

`INFILE` should be a .mp3 file with your audio you'd like to transcribe.

`OUTFILE` should be a .vtt file that has a name you'll successfully associate with your input audio (`test.vtt` may not be ideal, for example)

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
4. Once you have a terminal window open, request a session: `srun --partition=gpu --nodes=1 --pty --gres=gpu:1 --ntasks=1 --mem=4GB --time=02:00:00 /bin/bash`
5. Next, clone this repository and enter its directory (`cd transcription`). To clone a repository, you can find instructions [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or you can click the green button at the top of this page and choose the `HTTPS` tab. Then click the "copy" icon. 
6. Now we'll load CUDA; CUDA is a piece of software that lets Python talk to the GPU: `module load cuda/12.1`
7. Load `conda` (Anaconda, a Python package manager) using this command: `module load anaconda3/2022.05`
8. Create a blank Conda environment: `conda create -y -n NAME python==3.12.1` where `NAME` should be something you'll remember is associated with this project.
9. Activate your Conda environment: `source activate NAME`
10. Install the necessary packages: `python3 -m pip install -r requirements.txt` (this will take forever).
11. Back at https://ood.discovery.neu.edu, go to the "Files" tab and open up your home directory. Click the "Upload" button and upload a .mp3 file. Keep track of its name. 
12. The fun part: go back to your terminal window and run `python3 transcribe_interview.py -i ~/INPUT_FILE_NAME -o ~/OUT_FILE_NAME.tsv`, where INPUT_FILE_NAME is the name of your input file, and OUT_FILE_NAME is some name for your output file that you'll remember is associated with that input file.
13. Go back to your file browser and look for OUT_FILE_NAME.tsv. You can download it and open it in Excel or Google Sheets.

### Transcribing once you're set up:
1. Go to https://ood.discovery.neu.edu.
2. Click on the "Cluster" tab and then click "Discovery Shell Access".
3. Once you have a terminal window open, request a session: `srun --partition=gpu --nodes=1 --pty --gres=gpu:1 --ntasks=1 --mem=4GB --time=02:00:00 /bin/bash`
4. Now we'll load CUDA; CUDA is a piece of software that lets Python talk to the GPU: `module load cuda/12.1`
5. Load `conda` (Anaconda, a Python package manager) using this command: `module load anaconda3/2022.05`
6. Activate your Conda environment: `source activate NAME`
7. Back at https://ood.discovery.neu.edu, go to the "Files" tab and open up your home directory. Click the "Upload" button and upload a .mp3 file. Keep track of its name.
8. The fun part: go back to your terminal window and run `python3 transcribe_interview.py -i ~/INPUT_FILE_NAME -o ~/OUT_FILE_NAME.tsv`, where INPUT_FILE_NAME is the name of your input file, and OUT_FILE_NAME is some name for your output file that you'll remember is associated with that input file.
9. Go back to your file browser and look for OUT_FILE_NAME.tsv. You can download it and open it in Excel or Google Sheets.
