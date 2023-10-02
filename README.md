# Wizard Subtitler
![Wizard Subtitler Mascot](logo.jpeg)

Are you ready to add a touch of magic to your videos? Look no further than the Wizard Subtitler – your ultimate tool for effortlessly transcribing and subtitling your video content. Whether you're a filmmaker, content creator, or just someone who loves to add subtitles to videos, the Wizard is here to make your life easier.

## What is Wizard Subtitler?
The Wizard Subtitler is a powerful script/terminal command that transforms your video files into fully subtitled masterpieces leveraging the power of the Whisper AI model created by OpenAI. With just a single command, it can extract audio, transcribe it, generate subtitles in both the original language and English, and seamlessly 
embed those subtitles into your videos. What's more, if your videos aren't in the MKV format, the Wizard Subtitler will convert them for you automatically! This allows for nearly any video type to be used with this command.

## Dependencies

- Python 3
- ffmpeg
- moviepy
- whisper
- pysubs2
- langcodes

You can install the necessary Python libraries using pip:

```bash
pip install moviepy whisper pysubs2 langcodes
```

## Setup

1. Ensure you have Python 3 and ffmpeg installed on your machine.
2. Install the necessary Python libraries using pip.
3. Clone or download this repository to your local machine.
4. Add an alias to your `.bashrc` or `.bash_aliases` file to run this script using a simple command:

```bash
alias wsub='python /path/to/main.py'
```

## Usage

You can run this script from the command line using the following syntax:

```bash
python script.py INPUT [OPTIONS]
```

- `INPUT`: The path to the input file or directory containing video files.
- `OPTIONS`:
  - `--model model`: The version of whisper AI you wish to run the program with. Defaults to 'base'. Options include 'large', 'small', and 'tiny'.
  - `--output OUTPUT`: The path to the output directory where processed videos will be saved. Defaults to `output/`.

### Examples

Process a single video file and save the output in the default output directory (`output/`):

```bash
wsub /path/to/video.mkv
```

Process all video files in a directory and save the output in a custom output directory:

```bash
wsub /path/to/directory/ --output /path/to/output/
```

If you set up the alias as described in the Setup section, you can use the following simplified syntax:

```bash
wsub /path/to/video.mkv
```

```bash
wsub /path/to/directory/ --output /path/to/output/
```