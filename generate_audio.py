import numpy as np
import scipy.io.wavfile as wavfile

from mlx_audio.tts.utils import load_model

REFERENCE_AUDIO = 'reference_audios/appa_reference.wav'
REFERENCE_AUDIO_TRANSCRIPT = 'reference_audios/appa_reference.txt'
OUTPUT_FILE = 'output_audios/output.wav'
TEXT_TO_GENERATE = 'Hey there, how are you?'

def main():
    generate_audio(output_file='output_audios/test.wav')

def generate_audio(
        reference_audio=REFERENCE_AUDIO,
        reference_audio_transcript=REFERENCE_AUDIO_TRANSCRIPT,
        output_file=OUTPUT_FILE,
        text_to_generate=TEXT_TO_GENERATE
    ):

    # Open reference text file to extract reference text used in recording to give to model
    with open(reference_audio_transcript, 'r') as file:
        reference_text = file.read()

    print('🔮 Generating audio...\n')
    # Using MLX Audio and Qwen Voice Cloning, clone a reference voice to any sentence you want
    model = load_model('mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16')
    results = list(model.generate(
        text=text_to_generate,
        ref_audio=reference_audio,
        ref_text=reference_text
    ))

    audio = results[0].audio # This is a mx array which has be converted using SciPy

    print('\n🚀 Done generating!\n')

    print('Saving to file...')

    # Converting audio result and save to file
    audio_data = np.array(audio)
    sample_rate = 24000

    wavfile.write(output_file, sample_rate, audio_data)

    print(f'Saved to: {output_file}!')


if __name__ == '__main__':
    main()