import argparse
import os
import glob
import subprocess
import whisper
import pysubs2
from moviepy.editor import VideoFileClip
import langcodes
# install with pip install langcodes[data]


def convert_language_code_to_name(language_code):
    try:
        language_name = langcodes.Language.make(language_code).language_name()
        return language_name.capitalize()
    except:
        return "Unknown"

def extract_audio(video_file):
    audio_file = 'audio.wav'
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)
    return audio_file

def transcribe_audio(audio_file, ai_model):
    model = whisper.load_model(ai_model)
    result = model.transcribe(audio_file)
    translation = model.transcribe(audio_file, task="translate")
    return result, translation

def create_subtitles(transcription, filename):
    subs = pysubs2.load_from_whisper(transcription)
    subs_file = filename
    subs.save(subs_file)
    return subs_file


def add_subtitles_to_video(video_file, subtitle_file1, subtitle_file2, output_file, language1, language2):
    # Convert .ass to .srt
    subtitle_srt1 = subtitle_file1.replace('.ass', '.srt')
    subprocess.run(['ffmpeg', '-i', subtitle_file1, subtitle_srt1], check=True)

    subtitle_srt2 = subtitle_file2.replace('.ass', '.srt')
    subprocess.run(['ffmpeg', '-i', subtitle_file2, subtitle_srt2], check=True)

    # Add subtitles to video
    subprocess.run([
        'ffmpeg', '-i', video_file, '-i', subtitle_srt1, '-i', subtitle_srt2,
        '-map', '0:v', '-map', '0:a', '-map', '1', '-map', '2',
        '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'srt', '-c:s', 'srt',
        '-metadata:s:s:0', 'language=' + language1,
        '-metadata:s:s:0', 'title=AI Generated: ' + convert_language_code_to_name(language1),
        '-metadata:s:s:1', 'language=en',
        '-metadata:s:s:1', 'title=AI Generated: English',
        output_file
    ], check=True)

    # Delete the temporary .srt files
    os.remove(subtitle_srt1)
    os.remove(subtitle_srt2)


def process_video(video_file, output_folder, ai_model):
    video_file = convert_to_mkv(video_file)  # Convert to .mkv if necessary
    # Get the base name of the video file to use in naming the output file
    base_name = os.path.basename(video_file)
    base_name_no_ext = os.path.splitext(base_name)[0]

    audio_file = extract_audio(video_file)

    transcription, translation = transcribe_audio(audio_file, ai_model)

    subtitle_file1 = create_subtitles(transcription, f'{base_name_no_ext}_subtitles.ass')
    subtitle_file2 = create_subtitles(translation, f'{base_name_no_ext}_subtitles_translated.ass')

    # save as
    output_file = output_folder + base_name_no_ext + '.mkv'

    add_subtitles_to_video(video_file=video_file, subtitle_file1=subtitle_file1, subtitle_file2=subtitle_file2,
                           output_file=output_file, language1=transcription["language"],
                           language2=translation["language"])
    print(f'Success! Output file: {output_file}')

    # Delete the temporary .ass files
    os.remove(subtitle_file1)
    os.remove(subtitle_file2)
    os.remove("audio.wav")

def convert_to_mkv(input_file):
    if not input_file.endswith('.mkv'):
        output_file = os.path.splitext(input_file)[0] + '.mkv'
        command = ["ffmpeg", "-fflags", "+genpts", "-i", input_file, "-c", "copy", output_file]
        subprocess.run(command)
        return output_file  # Return the new file path
    return input_file  # Return the original file path if it's already an .mkv

def find_and_convert_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith('.mkv'):
                input_file = os.path.join(root, file)
                convert_to_mkv(input_file)

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe and subtitle videos.",
        epilog="This script processes video files to extract audio, transcribe the audio, generate subtitles, "
               "and add the subtitles to the video. If the video files are not in MKV format, they will be "
               "converted to MKV before processing."
    )
    parser.add_argument(
        "input",
        help="The path to the input file or directory containing video files."
    )
    parser.add_argument(
        "--output",
        default="output/",
        help="The path to the output directory where processed videos will be saved. Defaults to 'output/'."
    )
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "small", "base", "large"],
        help="The model to use for transcription and translation. Defaults to 'base'."
    )
    args = parser.parse_args()

    input_path = args.input
    output_folder = args.output
    os.makedirs(output_folder, exist_ok=True)

    if os.path.isdir(input_path):
        find_and_convert_files(input_path)  # Convert all non-.mkv files to .mkv
        for video_file in glob.glob(os.path.join(input_path, '*.mkv')):  # Now only process .mkv files
            process_video(video_file, output_folder)
    elif os.path.isfile(input_path):
        video_file = convert_to_mkv(input_path)  # Convert to .mkv if necessary
        process_video(video_file, output_folder)
    else:
        raise ValueError(f"Invalid input: {input_path}")

if __name__ == '__main__':
    main()