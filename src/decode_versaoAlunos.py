#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib

import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    DTMF = {
        '1': [697, 1209], '2': [697, 1336], '3': [697, 1477], 'A': [697, 1633],
        '4': [770, 1209], '5': [770, 1336], '6': [770, 1477], 'B': [770, 1633],
        '7': [852, 1209], '8': [852, 1336], '9': [852, 1477], 'C': [852, 1633],
        'X': [941, 1209], '0': [941, 1336], '#': [941, 1477], 'D': [941, 1633]
    }
    SINAL = signalMeu()
    sd.default.samplerate = 44100
    sd.default.channels = 2
    duration = 3
    
    numAmostras = duration * sd.default.samplerate
    freqDeAmostragem = sd.default.samplerate

    print('A captação começará em 3 segundos')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    time.sleep(1)
    print('\n==================')

    print('A gravação começou')
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")


        
    
    tempo = np.linspace(0.0, duration, duration*freqDeAmostragem)
    x,y = SINAL.calcFFT(audio[:,0],freqDeAmostragem)

    # Frequência no Tempo
    plt.plot(tempo,audio[:,0])
    plt.title('Frequência no Tempo')
    plt.show()

    # Fourier
    plt.plot(x, y)
    plt.title('Fourier')
    plt.show()
    
 
    index = peakutils.indexes(y, thres=0.4, min_dist=50)
    print(f"index de picos {index}") #yf é o resultado da transformada de fourier


    f1,f2 = SINAL.picos(index,x)              
    
    teclas = list(DTMF.keys())
    sons = list(DTMF.values())  

    resposta = SINAL.detecta_tecla(teclas,sons,f1,f2)


    print(f'a tecla pressionada foi: {resposta}')


  
    # Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
