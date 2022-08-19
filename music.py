# karplus strong algorithm

""" 
Tasks
visualize the algorithm
implement a ring buffer using the Python deque class
use numpy arrays and unfuncs
play WAV files using pygame
Plot a graph using matplotlib
play the pentatonic musical scale
"""

import argparse, pygame
from collections import deque
import numpy as np
import wave, math
import sys, os
import matplotlib.pyplot as plt
import time, random

# Creating WAV Files

# sRate = 44100
# nSamples = sRate * 5
# x = np.arange(nSamples)/float(sRate)
# vals = np.sin(2.0*math.pi*220.0*x)
# data = np.array(vals*32767, 'int16').tostring()
# file = wave.open('sine220.wav', 'wb')
# file.setparams((1,2, sRate, nSamples, 'NONE', 'uncompressed'))
# file.writeframes(data)
# file.close()

# # The minor pentatoni scale
# # implementing ring buffer with deque

# d = deque(range(10))
# print(d)

# d.append(-1)
# print(d)

# d.popleft()
# print(d)

# Implementing the Karplus-Strong Algorithm
gShowPlot = False

# notes of a pentatonic Minor Sale
# piano C4-E(b)-F-G-B(b)-C5
pmNotes = {'C4': 262, 'Eb':311, 'F':349, 'G':391, 'Bb':466}
# Writing a WAV file
def writeWAVE(fname, data):
    #open file
    file = wave.open(fname, 'wb')
    # WAV file parameters
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
    # set parameters
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()


# generate note of a given frequency
def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    # initialize ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])
    # initialize samples buffer
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.996*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()

    #convert samples to 16-bit values and then to a string
    # the maximum value is 32767 for 16-bit
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()


# Playing WAV files with pygame

#play a WAV file
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # dictionary of notes
        self.notes = {}
    # add a note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    # play a note
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + ' not found!')
    def playRandom(self):
        """play a random note"""
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()


# The main() method
def main():
    # declare global var
    global gShowPlot

    parser = argparse.ArgumentParser(description="Generating sounds with karplus String Algorithm")
    #add arguement
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    args = parser.parse_args()

    # show plot if flag set
    if args.display:
        gShowPlot = True
        plt.ion()

    # create note player
    nplayer = NotePlayer()

    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName) or args.display:
            data = generateNote(freq)
            print('creating ' + fileName + '...')
            writeWAVE(fileName, data)
        else:
            print('fileName already created. skipping...')

        # add note to player
        nplayer.add(name + '.wav')

        # play note if display flag set
        if args.display:
            nplayer.play(name + '.wav')
            time.sleep(0.5)

    # play a random tune
    if args.play:
        while True:
            try: 
                nplayer.playRandom()
                # rest - 1 to 8 beats
                rest = np.random.choice([1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()

    # random piano mode
    if args.piano:
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYUP):
                    print("key pressed")
                    nplayer.playRandom()
                    time.sleep(0.5)

# call main
if __name__ == '__main__':
    main()


