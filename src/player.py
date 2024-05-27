from colors import *
from itertools import permutations

def gen():
    '''
    Gera a matriz de possibilidades. Ela é representada por A7,4, ou seja, o arranjo de 7 cores escolhidas 4, sendo que a ordem importa. É uma matriz de 840 entradas, sendo elas todas as possibilidades.'''
    global POSSIBILIDADES
    POSSIBILIDADES = [arranjo for arranjo in permutations([RED, GREEN, BLUE, YELLOW, ORANGE, BLACK, WHITE], 4)]

def player(guess_hist, res_hist):
    '''
    Esta função funciona atualizando a matriz das possibilidades.
    
    Primeiramente, se for a primeira tentativa, quando o histórico é zerado, retorna o primeiro elemento da lista de possibilidades, um palpite qualquer. Depois disso, atualiza a matriz de possibilidades, da seguinte forma:
    
    Dado um palpite qualquer anterior aposta = guess_hist[-1] com res_hist[-1] = (x, y)
    - Sabe-se que o gabarito possui x cores em comum com aposta. Sendo assim, a intersecção dos conjuntos aposta e qualquer tentativa futura deve ter tamanho x.
    - Sabe-se que, das x cores em comum, y cores do gabarito estão naquela mesma posição da aposta. Portanto, comparando-se termo a termo, com um contador inicializado em 0, aposta[i] e gabarito[i] devem ser iguais, atualizando o contador de um em um, pelo menos y vezes, com i no intervalo [0, 4)
    
    Com isso em mente, mantêm-se, na lista de possibilidades, somente os arranjos que satisfazem às condições estabelecidas. Só se deixam na matriz as entradas com intersecção de tamanho x com a aposta que tenham exatamente y elementos na mesma posição. Na próxima iteração, faz-se o mesmo, reduzindo-se, iterativamente, o tamanho da lista de possibilidades. Ao fim, retorna-se sempre o primeiro elemento da matriz atualizada, estatisticamente equivalente a retornar um elemento aleatório.'''
    global POSSIBILIDADES

    if len(guess_hist) == 0:
        gen()
        return POSSIBILIDADES[0]
    
    POSSIBILIDADES = [arranjo for arranjo in POSSIBILIDADES if len(set(arranjo) & set(guess_hist[-1])) == res_hist[-1][0] and sum([1 for i in range(4) if arranjo[i] == guess_hist[-1][i]]) == res_hist[-1][1]]
    
    try:
        return POSSIBILIDADES[0]
    except IndexError:
        gen()
        return player(guess_hist, res_hist)
