import easygui
import sys
from transcribe_interview import *
import os

msg = "What kind of file are you loading for for transcription?"
reply = easygui.buttonbox(msg, choices=['cancel', 'mp3', 'mp4'])
if reply == 'cancel':
    sys.exit(0)
elif reply == 'mp3':
    mp3_fname = easygui.fileopenbox('Select the .mp3 file to transcribe')
    try:
        if mp3_fname[-4:] != '.mp3':
            raise ValueError('this file does not have a .mp3 extension')
    except Exception as e:
        easygui.exceptionbox()         
else:
    mp4_fname = easygui.fileopenbox(msg='Select the .mp4 file to convert to .mp3')
    try:
        if mp4_fname[-4:] != '.mp4':
            raise ValueError('this file does not have a .mp4 extension')
        else:
            mp3_fname = easygui.filesavebox('Name your converted .mp3 file.')
            print("Converting mp4 to mp3")
            os.system('ffmpeg -i "{}" -c:v copy -c:a libmp3lame -q:a 4 "{}"'.format(
                mp4_fname,
                mp3_fname
            ))
    except Exception as e:
        easygui.exceptionbox()                    

msg = "What kind of output file do you want?"
reply = easygui.buttonbox(msg, choices=['cancel', 'VTT', 'TXT', 'TSV (unwieldy)'])
if reply == 'cancel':
    sys.exit(0)
elif reply == 'VTT':
    outf_name = easygui.filesavebox('Name your transcribed VTT file')
    CONFIG = vtt_load_config('./config.yml') 
    print("converting...")
    run_pipeline(mp3_fname, CONFIG, outf_name) 
    print("success!")
    sys.exit(0)
elif reply == 'TXT':
    outf_name = easygui.filesavebox('Name your transcribed TXT file.')
    CONFIG = load_config('./config.yml')
    print("converting...")
    run_pipeline(mp3_fname, CONFIG, outf_name, filetype='TXT')
    print("success!")
    sys.exit(0)
else:
    outf_name = easygui.filesavebox('Name your transcribed TSV file.')
    CONFIG = load_config('./config.yml')
    print("converting...")
    run_pipeline(mp3_fname, CONFIG, outf_name, filetype='TSV')
    print("success!")
    sys.exit(0)


