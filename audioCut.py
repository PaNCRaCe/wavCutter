import numpy as np
from scipy.io import wavfile
from os.path import split, splitext
import argparse

if __name__ == "__main__":
    # Récupération des arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file to be cutted", type=str)
    parser.add_argument("chunk_length", help="Chunk length in seconds", type=int)
    parser.add_argument("overlap", help="Overlap in seconds", type=int)
    parser.add_argument("--output-dir", dest="output_dir", help="Output directory", type=str)
    parser.add_argument('--keep-incomplete', dest="keep_incomplete", action='store_true',
                        default=False)
    args = parser.parse_args()

    path = args.input
    slice_length = args.chunk_length
    overlap = args.overlap
    keep_incomplete = args.keep_incomplete
    output_dir = args.output_dir

    # lecture du fichier
    frequency, signal = wavfile.read(path)

    # dissociation des repertoires, basename et extension pour les chemins des
    # fichiers de sortie
    directory, basename = split(path)
    basename, ext = splitext(basename)
    if output_dir is None:
        # Si le repertoire n'est pas renseigné, sauvegarder dans le repertoire
        # d'origine
        output_dir = directory

    # durée en secondes de l'input et de chaque trame
    signal_length = len(signal) / frequency
    slices = np.arange(0, signal_length, slice_length-overlap, dtype=np.int)

    # enregistrement des trames
    for start, end in zip(slices[:-1], slices[1:]):
        start_audio = start * frequency
        end_audio = (end + overlap) * frequency
        audio_slice = signal[start_audio: end_audio]
        if keep_incomplete is False and end_audio > len(signal):
            # ne pas enregistrer la dernière partie incomplete si
            # keep_incomplete is False (defaut)
            print("Skipping %s_%s-%s%s" % (basename, start, end + overlap, ext))
            break
        else:
            print(start_audio/frequency, end_audio/frequency)
            wavfile.write("%s/%s_%s-%s%s" % (output_dir, basename, start,
                                             end + overlap, ext),
                          frequency, audio_slice)
