from pedalboard import Pedalboard, LowShelfFilter, load_plugin
from pedalboard.io import AudioFile
from pydub import AudioSegment
import numpy as np
import os

input_path = "C:/Users/user/Desktop/try"
output_path = "C:/Users/user/Desktop/try/output"

plugin_path = "C:/Program Files/Common Files/VST3/iZotope/RX 11 Spectral De-noise.vst3"

parameters_spectral_denoise = {
    "noise_threshold_db" : -5.9,
    "noise_reduction_db" : 9.0,
}

for filename in os.listdir(input_path):
    if filename.endswith(".wav") or filename.endswith(".mp3"):
        input_file = os.path.join(input_path, filename)
        output_file = os.path.join(output_path, f"{os.path.splitext(filename)[0]}_processed.wav")

        if filename.endswith(".mp3"):
            audio_mp3 = AudioSegment.from_mp3(input_file)
            audio_mp3.export(output_file, format="wav")
            input_file = output_file 

        with AudioFile(input_file) as f:
            print("Processing {input_file}...")

            audio = f.read(f.frames)
            audio_data = audio.astype(np.float32)

            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                processed_data = audio_data / max_val
            else:
                processed_data = audio_data


            spectral_denoise = load_plugin(plugin_path, parameter_values=parameters_spectral_denoise)

            board = Pedalboard([spectral_denoise])

            effected_audio = board(processed_data, f.samplerate)

            with AudioFile(output_file, 'w', f.samplerate, f.num_channels) as o:
                o.write(effected_audio)

        print(f"Finished processing {filename}. Output saved to {output_file}")

print("Batch Processing Complete")