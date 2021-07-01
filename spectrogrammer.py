import pylab
import scipy
import librosa
import librosa.display
import numpy as np 

def spectrogram(audio: np.ndarray, filename: str) -> None:
    """Generates a spectrogram for source audio.

    Parameters
    ----------
    audio: numpy.ndarray
        Source audio.
    filename: str
        filename of the resultant spectrogram. 
    """
    f, t, Zxx = scipy.signal.stft(audio, 8000, nperseg = 455, noverlap = 420, window='hann')
    Zxx = np.abs(Zxx[0:227, 2:-1])
    Zxx = librosa.amplitude_to_db(Zxx, ref = np.max)
    pylab.figure()
    pylab.axis('off') 
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
    librosa.display.specshow(Zxx, cmap='viridis')
    pylab.savefig(filename, bbox_inches=None, pad_inches=0)
    pylab.close()