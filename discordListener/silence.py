import pydub

aud = pydub.AudioSegment.from_wav('test.wav')

# silences = pydub.silence.detect_silence(aud, silence_thresh=-45)

# for silence in silences:
#     silenceClip = pydub.AudioSegment.silent(duration=(silence[1] - silence[0])) # generate silence the length of the detected silence
#     aud.overlay(silenceClip, position=silence[0])

newAud = pydub.silence.split_on_silence(aud, silence_thresh=-45)
print(newAud)

finalAud = pydub.AudioSegment.empty()
for audioSeg in newAud:
    finalAud = finalAud + audioSeg
    print(audioSeg.duration_seconds )
finalAud.export('re.wav')
