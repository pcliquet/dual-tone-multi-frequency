#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    sounds = {
        '1': [697, 1209], '2': [697, 1336], '3': [697, 1477], 'A': [697, 1633],
        '4': [770, 1209], '5': [770, 1336], '6': [770, 1477], 'B': [770, 1633],
        '7': [852, 1209], '8': [852, 1336], '9': [852, 1477], 'C': [852, 1633],
        'X': [941, 1209], '0': [941, 1336], '#': [941, 1477], 'D': [941, 1633]
    }

    signal = Signal() 
    sd.default.samplerate = 44100
    sd.default.channels = 2
    duration = 1
    
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
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=2)
    sd.wait()
    print("...     FIM")

    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações).
    # min = 697
    # max = 1633

    canal1 = []
    canal2 = []
    for canal in audio:
        canal1.append(canal[0])
        canal2.append(canal[1])
        
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo1 = np.linspace(0.0, duration, len(canal1))
    tempo2 = np.linspace(0.0, duration, len(canal2))

    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) .
    plt.plot(tempo1, canal1)
    plt.plot(tempo2, canal2)
    plt.title('Frequências no tempo')
    plt.legend(['Canal 1', 'Canal 2'])
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência (hz)')
    plt.show()

    # Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(canal1, freqDeAmostragem)
    signal.plotFFT(xf, yf)
    xf, yf = signal.calcFFT(canal2, freqDeAmostragem)
    signal.plotFFT(xf, yf)
    # print(yf)
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.4, min_dist=50)
    print(f"index de picos {index}") #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    # Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
