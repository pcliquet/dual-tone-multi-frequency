
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window



class signalMeu:
    
    def __init__(self):
        self.init = 0
    

    def __init__(self):
        self.init = 0

    #gera a senoid
    def senoid(self,f, A, t,fs):
        n = t*fs
        x = np.linspace(0.0, t, n)
        s = A*np.sin(f*x*2*np.pi)
        return s
    
    #Define a tecla precionada
    def dtmf(self,tecla,DTMF):
        freq_1= DTMF[tecla][0]
        freq_2= DTMF[tecla][1]
        return freq_1,freq_2

    #Gera o sinal
    def signal(self,s_1,s_2):
        return s_1+s_2

    #Simula a tecla do telefone 
    def discar(self,DTMF):
        while True:
            tecla = input("Qual numero digital: ")
            if tecla in DTMF.keys():
                break
        return tecla
 
    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')

    def picos(self,index,x):

        freq_baixas = [697,770,852,941]
        freq_altas = [1209,1336,1477,1633]

        picks = []
        for freq in x[index]:
            picks.append(freq)



        tolerancia = 50

        f1 = 0
        f2 = 0
        for pico in picks:
            for value in freq_baixas:
                if value-tolerancia < pico < value+tolerancia:
                    f1 = value
            for value2 in freq_altas:
                if value2-tolerancia < pico < value2+tolerancia:
                    f2 = value2
        return f1,f2

    def detecta_tecla(self, teclas,sons,f1,f2):
        for t in sons:
        # print([int(f1),int(f2)])
            if [int(f1),int(f2)] in sons:
                tec = sons.index([f1,f2])
                
        return teclas[tec]