# Import the flask module for the application
from flask import Flask, request

# Import the redis module for the application
import redis
## NOTE ##
# some code for DeepSpeech (i.e., convert_samplerate), among other calls, were copied from this source:
# https://github.com/mozilla/DeepSpeech/blob/master/native_client/python/client.py

from rq import Queue
# used for speech to text
from deepspeech import Model
import wave
import numpy as np
import subprocess
import shlex

# Import the time module to include some time delay in the application
import time
try:
    from shhlex import quote
except ImportError:
    from pipes import quote

modelPath = "deepspeech-0.9.3-models.pbmm"
scorerPath = "deepspeech-0.9.3-models.scorer"
file1Path = "test1.wav"
file2Path = "test2.wav"

# Create the application directory
app = Flask(__name__)

# Make a connection of the queue and redis
r = redis.Redis()
q = Queue(connection=r)

# function copied from DeepMind source code to convert sample rates
def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)

# Create a working task queue  
def task_in_background(t):  
 
    # delay = 10 
 
    # print("Running Task")  
    # print(f"Simulates the {delay} seconds")  
 
    # time.sleep(delay)  
 
    # print(len(t))  
    # print("Completed Task")  
 
    # return len(t)
    model = Model(modelPath)
    model.enableExternalScorer(scorerPath)
    desired_sample_rate = model.sampleRate()


    if t == '1':
        fin = wave.open(file1Path, 'rb')
        fs_orig = fin.getframerate()
        if fs_orig != desired_sample_rate:
            # print('Warning: original sample rate ({}) is different than {}hz. Resampling might produce erratic speech recognition.'.format(fs_orig, desired_sample_rate), file=sys.stderr)
            fs_new, audio = convert_samplerate(file1Path, desired_sample_rate)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        text = model.stt(audio)
        print(text)
    if t == '2':
        fin = wave.open(file2Path, 'rb')
        fs_orig = fin.getframerate()
        if fs_orig != desired_sample_rate:
            # print('Warning: original sample rate ({}) is different than {}hz. Resampling might produce erratic speech recognition.'.format(fs_orig, desired_sample_rate), file=sys.stderr)
            fs_new, audio = convert_samplerate(file2Path, desired_sample_rate)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        text = model.stt(audio)
        print(text)


@app.route("/task")  
def add_task():  
 
    if request.args.get("t"):  
 
        job= q.enqueue(task_in_background, request.args.get("t"))  
 
        q_len = len(q)  
 
        return f"The task {job.id} is added into the task queue at {job.enqueued_at}. {q_len} task in the queue"  
    return "Task Queue with Flask"  
 
if __name__ == "__main__":  
    app.run()
