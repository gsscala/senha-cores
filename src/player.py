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
from random import sample, randint
import itertools
from permutar_cores import quatro_acertos

# Cores disponíveis para o palpite
colors = [RED, GREEN, BLUE, YELLOW, ORANGE, BLACK, WHITE]

def compare_tuple_Lists(tuple_list_one, tuple_list_two):
    return [tuple1 for tuple1 in tuple_list_one for tuple2 in tuple_list_two if set(tuple1) == set(tuple2)]

def get_remaining_colors(sub_color_list, super_color_list):
    return [possible_color for possible_color in super_color_list if possible_color not in sub_color_list]

def create_possible_list(right_colors_combinations_list, all_colors):
    possible_combination = []
    for right_color_combination in right_colors_combinations_list:
        possible_combination.extend(complete_guess(right_color_combination, all_colors))

    return possible_combination

def intersect_and_filter(guess_hist, result_index, include):
    previoues_guess = guess_hist[result_index]
    actual_guess = guess_hist[-1]
    intersection_colors = list(set(previoues_guess) & set(actual_guess))
    intersection_colors_positions = [previoues_guess.index(color) for color in intersection_colors]

    for color, position in zip(intersection_colors, intersection_colors_positions):
        filter_List(color, position, include)

def complete_guess(right_colors, all_colors):
    right_colors_list = [right_color for right_color in right_colors]
    remaining_colors = get_remaining_colors(all_colors, colors)
    all_possible_colors = right_colors_list + remaining_colors
    all_possible_combinations = list(itertools.combinations(all_possible_colors, 4))
    final_combination = [possible_combinations for possible_combinations in all_possible_combinations if set(right_colors_list).issubset(set(possible_combinations))]

    return final_combination 

def filter_List(right_color, right_position, inclusion):
    global all_combinations_right_colors_already

    for combination in all_combinations_right_colors_already:
        if (inclusion == 0) and (combination[right_position] == right_color):
            all_combinations_right_colors_already.remove(combination)

        if (inclusion == 1) and (combination[right_position] != right_color):
            all_combinations_right_colors_already.remove(combination)

def player(guess_hist, res_hist):
    """
    Função principal do jogador.

    Esta função deve retornar o seu palpite, que deve ser uma lista de 4 cores.
    As cores disponíveis são: RED, GREEN, BLUE, YELLOW, ORANGE, BLACK, WHITE.

    Parâmetros:
    - guess_hist: lista de palpites anteriores
    - res_hist: lista de resultados anteriores

    Retorna:
    - lista de 4 cores

    Exemplo:
    return [RED, GREEN, BLUE, YELLOW]
    """

    global historic_of_possible_guess
    global all_combinations_right_colors_already 

    # If no guesses have been made
    if len(guess_hist) == 0 or res_hist[-1] == (0, 0):
        historic_of_possible_guess = []
        all_combinations_right_colors_already = []
        return sample(colors, 4)
    
    if res_hist[-1][0] == 4:
        quatro_acertos(guess_hist,res_hist)
        '''if not all_combinations_right_colors_already:
            all_combinations_right_colors_already = list(itertools.permutations(guess_hist[-1], len(guess_hist[0])))
        
        for result_index, result in enumerate(res_hist):
            previoues_guess = guess_hist[result_index]
            actual_guess = guess_hist[-1]
            
            if result[1] == 0:
                intersect_and_filter(guess_hist, result_index, 0)
            
            if (result[0] == result[1]):
                intersect_and_filter(guess_hist, result_index, 1)

            if (len(res_hist) > 2) and (res_hist[result_index][0] == 3) and (res_hist[-1][1] == res_hist[result_index][1]):
                if sum(x == y for x, y in zip(actual_guess, previoues_guess)) == 3:
                    color = list(set(actual_guess) - set(previoues_guess))
                    filter_List(color[0], list(actual_guess).index(color[0]), 0)

        final_guess = all_combinations_right_colors_already[randint(0, len(all_combinations_right_colors_already) -1)]
        all_combinations_right_colors_already.remove(final_guess)
        return final_guess'''
    
    right_possible_colors = list(itertools.combinations(guess_hist[-1], res_hist[-1][0]))
    if(historic_of_possible_guess):
        historic_of_possible_guess = compare_tuple_Lists(historic_of_possible_guess, create_possible_list(right_possible_colors, guess_hist[-1]))
    else:
        historic_of_possible_guess = create_possible_list(right_possible_colors, guess_hist[-1])

    return historic_of_possible_guess[randint(0, len(historic_of_possible_guess) -1)]

