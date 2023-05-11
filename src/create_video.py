import os
import moviepy.video.io.ImageSequenceClip
from natsort import natsorted
import moviepy.editor as mpe
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import librosa
import numpy
import soundfile

def create_video():
    image_folder = 'data/frames'
    fps = 0.75

    image_files = natsorted([os.path.join(image_folder,img)
                   for img in os.listdir(image_folder)
                   if img.endswith(".jpg")], reverse=False)
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile('del_video.mp4')


def add_audio():
    videoclip = mpe.VideoFileClip("del_video.mp4")
    initial_duration = int(videoclip.duration)

    audio_path = "data/audio.mp3"
    
    out, sr = librosa.load(audio_path, duration=initial_duration)
    apply_fadeout(out, initial_duration, sr)
    soundfile.write("data/temp_audio.wav", out, samplerate=sr)

    audioclip = mpe.AudioFileClip("data/temp_audio.wav")

    new_audioclip = mpe.CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("del_video_audio.mp4")

    ffmpeg_extract_subclip("del_video_audio.mp4", 0, initial_duration + 3, targetname="result.mp4")

def apply_fadeout(audio, sr, duration=1.0):
    # convert to audio indices (samples)
    length = int(duration*sr)
    end = audio.shape[0]
    start = end - length

    # compute fade out curve
    # linear fade
    fade_curve = numpy.linspace(1.0, 0.0, length)

    # apply the curve
    audio[start:end] = audio[start:end] * fade_curve