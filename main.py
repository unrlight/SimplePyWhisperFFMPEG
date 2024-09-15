import os
import whisper
import ffmpeg
from whisper.utils import get_writer
import easygui

MODEL_SIZE = 'medium'
LECTURE_NAME = 'F2'
TEMP_DIR = './temp'

model = whisper.load_model(MODEL_SIZE)

def select_file():
    files = easygui.fileopenbox(title="Choose mp4, mp4 sequence, mp3 or wav", 
                                filetypes=["*.mp4", "*.mp3", "*.wav"], 
                                multiple=True)
    return list(files) if files else []

def convert_mp4_to_wav(input_file, output_file):
    ffmpeg.input(input_file).output(output_file, format='wav').run()

def concatenate_wav_files(files, output_file):
    inputs = [ffmpeg.input(f) for f in files]
    (
        ffmpeg
        .concat(*inputs, v=0, a=1)
        .output(output_file, acodec='pcm_s16le')
        .run()
    )

def transcribe_audio(audio: str, language: str = 'ru'):
    result = model.transcribe(audio=audio, language=language, verbose=False)
    return result

def save_file(results, format='tsv'):
    output_dir = os.path.join('./output', LECTURE_NAME)
    os.makedirs(output_dir, exist_ok=True)
    writer = get_writer(format, output_dir)
    writer(results, f'{LECTURE_NAME}_transcribe.{format}')

def main():
    files = select_file()

    if not files:
        print("Please select file")
        return

    if len(files) == 1:
        file = files[0]
        ext = os.path.splitext(file)[-1].lower()
        
        if ext == '.mp4':
            os.makedirs(TEMP_DIR, exist_ok=True)
            wav_file = os.path.join(TEMP_DIR, f'{LECTURE_NAME}.wav')
            convert_mp4_to_wav(file, wav_file)
            result = transcribe_audio(audio=wav_file)
        elif ext == '.mp3' or ext == '.wav':
            result = transcribe_audio(audio=file)
        else:
            print(f"Unsupported file type: {ext}")
            return
    else:
        if all([os.path.splitext(f)[-1].lower() == '.mp4' for f in files]):
            os.makedirs(TEMP_DIR, exist_ok=True)
            wav_files = []
            
            for i, file in enumerate(files):
                wav_file = os.path.join(TEMP_DIR, f'{LECTURE_NAME}_{i}.wav')
                convert_mp4_to_wav(file, wav_file)
                wav_files.append(wav_file)

            final_wav = os.path.join(TEMP_DIR, f'{LECTURE_NAME}_combined.wav')
            concatenate_wav_files(wav_files, final_wav)

            result = transcribe_audio(audio=final_wav)
        else:
            print("You can combine only mp4 files")
            return

    print('-' * 50)
    print(result.get('text', ''))

    save_file(result, 'tsv')
    save_file(result, 'txt')
    save_file(result, 'srt')

if __name__ == "__main__":
    main()
