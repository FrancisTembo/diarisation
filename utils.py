import collections
import os
from shutil import rmtree


def extract_timestamps(filename_cha: str, target_speaker: str) -> list:
    """Extracts timestamps from the given .char file

    Parameters
    ----------
    filename_cha : str
        The target .char file.
    target_speaker : str
        The target speaker to which utterances will be extracted.

    Returns
    -------
    list
        Time stamps indicating each time the target speaker spoke.
    """
    time_stamps = []
    speaker = "*" + target_speaker
    with open(filename_cha, encoding="utf8") as f:
        for line in f:
            if speaker in line and "" in line:
                time_stamps.append(line.split("", maxsplit=2)[1])
    time_stamps = [
        i for n, i in enumerate(time_stamps) if i not in time_stamps[:n]
    ]  # Remove duplicates
    return [element.split("_") for element in time_stamps]


def join_continuous(time_stamps: list) -> list:
    """Joins successive timestamps for better segmentation.

    Parameters
    ----------
    time_stamps : list
        List of timestamps.

    Returns
    -------
    list
        List of processed timestamps
    """
    time = []
    # Changing to one continuous list
    for element in time_stamps:
        time.append(element[0])
        time.append(element[1])
    counter = collections.Counter(time)
    times_joined = [k for k, v in counter.items() if v == 1]
    start = times_joined[0::2]
    end = times_joined[1::2]
    return list(zip(start, end))


def mkdir_p(path):
    import errno

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise


def del_folder(path):
    try:
        rmtree(path)
    except:
        pass
