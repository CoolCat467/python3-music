#!/usr/bin/env python3
# Music
# -*- coding: utf-8 -*-

# Based of https://github.com/tsoding/haskell-music

NAME = 'Music'
AUTHOR = 'CoolCat467'
__version__ = '0.0.0'

import os, math, struct

VOLUME = 0.3
SAMPLERATE = 44100#48000#Samples Per Seccond
PITCHSTANDARD = 440#440 hz
BPM = 120#120 Beats Per Minute
BEATDURATION = 60 / BPM#Secconds per beat

#-- NOTE: the formula is taken from https://pages.mtu.edu/~suits/NoteFreqCalcs.html
#f = Semitones -> Hz
getHz = lambda s : PITCHSTANDARD * (2 ** (1 / 12)) ** s

def sine(x):
    return math.sin(x)

def square(x):
    if math.sin(x) > 0:
        return 1
    return -1

def triangle(x):
    #return abs(x % 4 - 2) - 1
    a = 1
    p = 12.5
    return ((2 * a) / math.pi) * math.asin(math.sin(((math.pi * 2) / p) * x))

def sawtooth(x):
    return (x % 4 - 2)

def trisquare(x):
    return -((x) % 4) + (x % 3)

FUNCTIONS = [sine, square, triangle, sawtooth, trisquare]

def getAttackAndRelease(outlen):
    def attack():
        n = 0
        while True:
            yield min(1, n)
            n += 0.001
    def release():
        t = outlen
        n = 1
        cng = 0.001
        active = outlen * cng
        while True:
            yield max(0, n)
            if t <= active*2:
                n -= cng
            t -= 1
    return attack(), release()

def freq(hz, duration, function=0, continuous=False):
    step = (hz * 2 * math.pi) / SAMPLERATE
    output = [FUNCTIONS[function](i * step) for i in range(0, int(SAMPLERATE * duration))]
    attack, release = getAttackAndRelease(int(SAMPLERATE * duration))
    if continuous:
        return [x * VOLUME for x in output]
    return [(x * y * z) * VOLUME for x, y, z in zip(attack, output, release)]

note = lambda n, beats, function=0, continuous=False: freq(getHz(n), (beats * BEATDURATION), function, continuous)

song = lambda notes, beats, function=0, continuous=False: sum([note(n, b, function, continuous) for n, b in zip(notes, beats)], [])

##wave = [note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.5)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.5)
##    , note(5, 0.25)
##    , note(5, 0.25)
##    , note(5, 0.25)
##    , note(5, 0.25)
##    , note(5, 0.25)
##    , note(5, 0.25)
##    , note(5, 0.5)
##    , note(3, 0.25)
##    , note(3, 0.25)
##    , note(3, 0.25)
##    , note(3, 0.25)
##    , note(3, 0.25)
##    , note(3, 0.25)
##    , note(3, 0.5)
##    , note((-2), 0.5)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.25)
##    , note(0, 0.5)
##    ]
##wave = sum([note(0, 0.25)*4,
##            note(0, 0.5),
##            note(0, 0.25)*6,
##            note(0, 0.5),
##            note(5, 0.25)*6,
##            note(5, 0.5),
##            note(3, 0.25)*6,
##            note(3, 0.5),
##            note((-2), 0.5),
##            note(0, 0.25)*4,
##            note(0, 0.5)], [])
notes = [0]*12+[5]*7+[3]*7+[-2]+[0]*2
beats = [0.25]*4+sum([[0.5]+[0.25]*6]*3, [])+[0.5]*2+[0.25, 0.5]
wave = song(notes, beats, 0)
#wave5 = [sum(i) for i in zip(*[song(notes, beats, i) for i in range(len(FUNCTIONS))])]

hehehe = sum([note(0, 0.25),
              note(0, 0.25),
              note(12, 0.5),
              note(7, (0.5 + 0.25)),
              note(6, 0.5),
              note(5, 0.5),
              note(3, 0.5),
              note(0, 0.25),
              note(3, 0.25),
              note(5, 0.25)], [])*2

#test = sum([note(i/4, 0.25) for i in range(-128, 128)], [])
#test = sum([note(i, 1) for i in range(16, -40, -8)], [])
#test = note(0, 20)
##notes = [i/4 for i in range(16, -40, -8)]
##notes = notes+[i for i in reversed(notes[:-1])]
##beats = [1 for i in range(len(notes))]
##test = song(notes, beats, 0)
#test5 = [sum(i) for i in zip(*[song(notes, beats, i) for i in range(len(FUNCTIONS))])]


def save(data, filename):
    file = open(filename, 'wb')
    
    file.write(struct.pack(str(len(data))+'f', *data))

def play(filename):
    # f32le = 32 bit float encoding in Little-endian byte order 
    os.system('ffplay -autoexit -showmode 1 -f f32le -ar %f %s' % (SAMPLERATE, filename))

def run():
    save(wave, 'output.bin')
    play('output.bin')

if __name__ == '__main__':
    run()
