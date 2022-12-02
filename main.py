import pysrt
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import whisper
import opencc
from cleaners import Character_to_Pinyin, Character_to_IPA, Character_to_Phoneme, No_Cleaner
import re

root_dst = 'E:/vits_cache/'
root_from = 'F:/VITS/data/origin/'
folder_name = '20221029'
model_size = 'small'
cleanner = No_Cleaner
print_information = True


def cut(min_threshold=1000):
    subtitle_dir = root_from+folder_name+'/subtitle.srt'
    audiopath = root_from+folder_name+'/vocal.mp3'
    audiotype = 'wav'
    dst_path = root_dst+folder_name+'/chunks/'
    
    subtitles = pysrt.open(subtitle_dir)
    audio = AudioSegment.from_file(audiopath, format='mp3')
    audio_mono = audio.set_channels(1).set_frame_rate(22050)

    if not os.path.exists(dst_path): os.makedirs(dst_path)

    count = 0

    for subtitle in subtitles:

        time_start = subtitle.start.milliseconds
        time_start += subtitle.start.seconds * 1000
        time_start += subtitle.start.minutes * 1000 * 60
        time_start += subtitle.start.hours * 1000 * 60 * 60

        time_end = subtitle.end.milliseconds
        time_end += subtitle.end.seconds * 1000
        time_end += subtitle.end.minutes * 1000 * 60
        time_end += subtitle.end.hours * 1000 * 60 * 60

        duration = time_end - time_start

        if duration > min_threshold:
            chunk = audio_mono[time_start: time_end]
            save_name = dst_path+'%04d.%s' % (count, audiotype)
            chunk.export(save_name, format=audiotype)
            count += 1
            if print_information:
                print('%04d %d' % (count, len(chunk)))

    return count


def to_text(count):
    chunks_path = root_dst+folder_name+'/chunks/'
    model = whisper.load_model(model_size)
    cc = opencc.OpenCC('t2s')
    simplified_text = []

    for i in range(count):
        audio_name = chunks_path+'%04d.%s' % (i, 'wav')
        transcribe = model.transcribe(audio_name)['text']
        convert = cc.convert(transcribe)
        simplified_text.append(convert)
        if print_information:
            print('toText %d: %s     %s'%(i,convert,transcribe))

    return simplified_text


def to_file(texts):
    texts_cleanned = cleanner(texts)
    file_path = root_dst+folder_name+'/text.txt'

    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(len(texts_cleanned)):
            string = '%04d.' % (i)+'wav|'+texts_cleanned[i]+'\n'
            f.write(string+'\n')
            if print_information:
                print('toFile: '+str(i)+' '+string)
    f.close()


if __name__ == '__main__':

    count = cut()
    texts = to_text(count)
    to_file(texts)
