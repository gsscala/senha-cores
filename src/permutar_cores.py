from itertools import permutations
from random import *

global posicao_cor
global cor_certa 

def achar_cores_certas(jogada, guess_hist):
    cor_certa = [color for color in jogada if color in guess_hist[-1]]
    posicao_cor = [jogada.index(color) for color in guess_hist[-1] if color in jogada]
    return cor_certa, posicao_cor

def checagem(palpite, guess_hist):
    if palpite not in guess_hist:
        return True
    else:
        return False

def quatro_acertos(guess_hist, res_hist):

    listas_provaveis = []
    listas_improvaveis = []
    permutacoes_possiveis = [list(p) for p in permutations(guess_hist[-1])]

    for i in range(len(res_hist)):
        tupla = res_hist[i]
        jogada = guess_hist[i]
        cor_certa, posicao_cor = achar_cores_certas(jogada,guess_hist)

        # case (3,3) no res_hist: adiciona cor certa conhecida na posição da cor errada de aposta (3,3)
        if tupla == (3,3):
            lista = [color for color in jogada if color in guess_hist[-1]]
            cor_falta = [color for color in guess_hist[-1] if color not in jogada]
            cor_errada_em_jogada = [color for color in jogada if color not in guess_hist[-1]]
            lista.insert(jogada.index(cor_errada_em_jogada[0]),cor_falta[0])
            return lista
        
        #case (1,0) no res_hist: gera todas as permutações de guess_hist[-1] com a cor certa na posição errada fixada
        elif tupla == (1,0):
            lista = [aposta for aposta in permutacoes_possiveis if aposta.index(cor_certa[0]) == posicao_cor[0]]
            listas_improvaveis.extend(lista)
        
        #case(1,1): gera todas as permutações possiveis de guess_hist[-1] com a cor que se sabe a posição certa fixada    
        elif tupla == (1,1):
            lista = [aposta for aposta in permutacoes_possiveis if aposta.index(cor_certa[0]) == posicao_cor[0]]
            listas_provaveis.extend(lista)

        #case (2,0): gera todas as permutações possiveis de guess_hist[-1] com as cores certas nos locais errados fixadas, adicionando-as a 'listas improváveis'
        elif tupla == (2,0):
            lista = [aposta for aposta in permutacoes_possiveis if aposta.index(cor_certa[0]) == posicao_cor[0] or aposta.index(cor_certa[1]) == posicao_cor[1]]
            listas_improvaveis.extend(lista)

        #Case (2,2): gera todas as permutações possiveis de guess_hist[-1] com as cores certas nos locais corretos fixadas, adicionando-as ao set 'listas prováveis'
        elif tupla == (2,2):
            lista = [aposta for aposta in permutacoes_possiveis if aposta.index(cor_certa[0]) == posicao_cor[0] and aposta.index(cor_certa[1]) == posicao_cor[1]]
            listas_provaveis.extend(lista)
        
        elif tupla == (3,0):
            lista = [aposta for aposta in permutacoes_possiveis if aposta.index(cor_certa[0]) == posicao_cor[0] or aposta.index(cor_certa[1]) == posicao_cor[1] or aposta.index(cor_certa[2]) == posicao_cor[2]]
            listas_improvaveis.extend(lista)

            '''elif tupla == (4,0):
            posicao_cor4 = jogada.index(cor_certa[3])
            lista = [aposta for aposta in permutacoes_possiveis if aposta.index(cor_certa[0]) == posicao_cor[0] or aposta.index(cor_certa[1]) == posicao_cor[1] or aposta.index(cor_certa[2]) == posicao_cor[2] or aposta.index(cor_certa[3]) == posicao_cor4]
            listas_improvaveis.extend(lista)'''

        else: #Case (2,1) (3,1) (3,2): Não é possivel retirar informações uteis que ajudem a reduzir o numero de possibilidades possíveis
            continue


    #Removendo repetições
    listas_improvaveis_sem_rep = []
    listas_provaveis_sem_rep = []

    for i in listas_provaveis:
        if i not in listas_provaveis_sem_rep:
            listas_provaveis_sem_rep.append(list(i))
        else:
            continue
    
    for i in listas_improvaveis:
        if i not in listas_improvaveis_sem_rep:
            listas_improvaveis_sem_rep.append(list(i))
        else:
            continue
            
        
        #se listas prováveis < all permutations - listas improváveis -> choice listas prováveis
        #se listas prováveis > all permutations - listas improváveis -> choice from all permujtations - listas improváveis

    if len(listas_provaveis_sem_rep) < (len(permutacoes_possiveis) - len(listas_improvaveis_sem_rep)) and len(listas_provaveis_sem_rep) > 0:
        palpite = choice(listas_provaveis_sem_rep)
    else:
        palpite = choice([p for p in permutacoes_possiveis if p not in listas_improvaveis_sem_rep and p not in guess_hist])

    if checagem(palpite, guess_hist):
        return palpite
    else:
        return quatro_acertos(guess_hist,res_hist)







    
"""    else:
    color_dict = {
            "vermelho": RED,
            "verde": GREEN,
            "azul": BLUE,
            "amarelo": YELLOW,
            "laranja": ORANGE,
            "preto": BLACK,
            "branco": WHITE,
        }
        list = input().split()
        for l in range(4):
            list[l] = color_dict[list[l]]
        return list"""

        