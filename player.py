#!/usr/bin/env python3
"""
Implemente aqui o seu código para o jogador.

Seu principal objetivo é implementar a função `player`, que deve retornar uma lista de 4 cores, o seu próximo palpite.
Como exemplo, a função abaixo retorna um palpite aleatório.

Dicas:
- Você pode implementar outras funções para auxiliar a função `player`.
- Você pode salvar informações entre os palpites usando variáveis globais (fora de qualquer função).
"""
from colors import *
from random import sample

# Cores disponíveis para o palpite
colors = [RED, GREEN, BLUE, YELLOW, ORANGE, BLACK, WHITE]
color_dict = {
    "vermelho": RED,
    "verde": GREEN,
    "azul": BLUE,
    "amarelo": YELLOW,
    "laranja": ORANGE,
    "preto": BLACK,
    "branco": WHITE,
}


def comparar_amostra(ultimos_acertos, guess_hist):
    amostra1 = sample(colors, 4 - ultimos_acertos[0])
    amostra2 = sample(guess_hist[-1], ultimos_acertos[0])
    for i in range(len(amostra2)):  ##Como fazer com while?
        if amostra1.count(amostra2[i]) != 0:
            amostra1 = sample(colors, 4 - ultimos_acertos[0])
            i = 0
    return amostra2.extend(amostra1)


def player(guess_hist, res_hist):
    if len(guess_hist) == 0:
        return sample(colors, 4)
    if res_hist[-1][0] == 0:  # todo juntar 2 if pela tupla
        amostra = sample(colors, 4)
        while amostra in guess_hist:
            amostra = sample(colors, 4)
        return amostra
    ultimos_acertos = res_hist[-1]
    return comparar_amostra(ultimos_acertos, guess_hist)
