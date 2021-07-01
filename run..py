import argparse
import logging
import os
from glob import iglob

import librosa
import numpy as np
import soundfile as sf

from spectrogrammer import spectrogram
from utils import extract_timestamps, join_continuous, mkdir_p

DATA_AUDIO_DIR = "./dataset"
TARGET_SR = 16000
SPEC = False
TARGET_SR = 8000
OUTPUT_DIR = "./output"
OUTPUT_DIR_SPEC = os.path.join(OUTPUT_DIR, "spectrogram")
OUTPUT_DIR_WAV = os.path.join(OUTPUT_DIR, "wav")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-s",
    "--speaker",
    required=True,
    choices=["CHI", "MOT"],
    help="speaker utterances to extract",
)
ap.add_argument(
    "-w",
    "--write_spectrogram",
    default=False,
    required=False,
    help="write spectrogram for utterances",
)
args = vars(ap.parse_args())
target_speaker = args["speaker"]
write_spec = args["write_spectrogram"]


#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
)
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter("%(levelname)s: %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def read_audio(filename_audio: str) -> np.ndarray:
    """Loads audio file from source.

    Parameters
    ----------
    filename_audio : str
        Path to audio file.

    Returns
    -------
    audio : numpy.ndarray
        Array form of the raw audio waveform.
    """
    logger.info("Loading audio.")
    audio, sr = librosa.load(filename_audio, sr=None, mono=True)
    audio = librosa.core.resample(
        y=audio.astype(np.float32), orig_sr=sr, target_sr=TARGET_SR, res_type="scipy"
    )
    logger.info("Done!")
    return audio


def extract_utterances():
    logger.info("Extracting audio.")
    for i, filename in enumerate(
        iglob(os.path.join(DATA_AUDIO_DIR, "**/**.cha"), recursive=True)
    ):
        time_stamps = extract_timestamps(filename, target_speaker)
        utterances = join_continuous(time_stamps)
        audio_filename = str("." + filename.split(".", 2)[1] + ".wav")
        full_audio = read_audio(audio_filename)
        base_name = os.path.basename(filename).split(".", 2)[0]

        for utterance in utterances:
            start = int(utterance[0])
            end = int(utterance[-1])
            output_audio = full_audio[start:end]
            output_name = (
                base_name
                + "_"
                + str(target_speaker)
                + "_"
                + str(utterance[0])
                + "_"
                + str(utterance[-1])
            )
            output_audio_name = os.path.join(OUTPUT_DIR_WAV, output_name + ".wav")
            sf.write(str(output_audio_name), output_audio, TARGET_SR, subtype="PCM_24")
            if write_spec == True:
                output_spec_name = os.path.join(OUTPUT_DIR_SPEC, output_name + ".jpeg")
                spectrogram(output_audio, output_spec_name)
    logger.info("Completed!")


if __name__ == "__main__":
    mkdir_p(OUTPUT_DIR_WAV)
    if write_spec == True:
        mkdir_p(OUTPUT_DIR_SPEC)
    extract_utterances()