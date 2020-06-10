''' audio file manager for ursulaListener '''
import pydub
import logging

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(name)s | %(message)s'))
logger = logging.getLogger('audioManager')

def trimSilence(pathToAudio, pathToNewAudio=None):
    '''
    removes silence from an audio file and exports to a new file
    if pathToNewAudio is not given, it will overwrite the original file
    '''

    # check if a new path was given, if not, new path is old path
    if pathToNewAudio is None:
        pathToNewAudio = pathToAudio

    # grab the audio
    audio = pydub.AudioSegment.from_wav(pathToAudio)
    cutoff = audio.max_dBFS*1.9 # 1.9 is a magic number, can be tuned later, tbh this is a dumb way to make a cutoff
    logger.debug(f'audio max dBFS {round(audio.max_dBFS, 2)}, cutoff is {round(cutoff, 2)}')

    # trim the audio
    audioTrimmed = pydub.effects.strip_silence(audio, silence_thresh=cutoff)
    logger.debug(f'trimmed {round(audio.duration_seconds - audioTrimmed.duration_seconds, 2)} seconds of audio')

    # export trimmed audio to a file
    audioTrimmed.export(pathToNewAudio)
    logger.debug(f'exported audio to {pathToNewAudio}')

if __name__ == "__main__":
    logger.setLevel('DEBUG')
    logger.debug('hey there cowboy')
    trimSilence('test.wav', 'testnew.wav')
