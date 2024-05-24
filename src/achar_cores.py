from colors import *
from random import sample, choice

colors = [RED, GREEN, BLUE, YELLOW, ORANGE, BLACK, WHITE]  # possibilidades de cores
apostas_positivas = []  # apostas de elementos que podem estar certos
apostas_negativas = []  # apostas de elementos que podem estar errados
possibilidades = []  # elementos incertos se estão certos ou errados
blacklist = []  # elementos errados
whitelist = []  # elementos certos
historico_modificado = []
opcoes = []


def checagem(retorno, guess_hist):
    """
    Retorna um valor booleano correspondente à ausência do palpite atual nos palpites anteriores, sendo a ordem das cores no palpite irrelevante para a checagem. Além disso, garante que haja exatamente 4 elementos, sendo nenhum repetido, com todos da whitelist presentes e nenhum da blacklist.
    """
    print(
        "palpite",
        retorno,
        "a_p",
        apostas_positivas,
        "a_n",
        apostas_negativas,
        "poss",
        possibilidades,
        "bl",
        blacklist,
        "wl",
        whitelist,
    )
    return (
        set(retorno) not in map(set, guess_hist)
        and set(retorno).isdisjoint(set(blacklist))
        and set(whitelist).issubset(set(retorno))
        and len(set(retorno)) == 4
    )


def algoritmo_padrao(guess_hist, lista):
    tentativa = lista.copy()  # lista vai ser baseada na ultima tentativa
    apostas_negativas.append(
        choice(tentativa)
    )  # aposta que um elemento da lista ta errado
    apostas_positivas.append(
        choice(list(set(colors) - set(tentativa)))
    )  # aposta que um elemento que não esteja na lista seja um certo
    tentativa.remove(apostas_negativas[-1])  # tira o elemento errado
    tentativa.append(apostas_positivas[-1])  # coloca o elemento certo
    # se checagem == verdadeiro
    if checagem(tentativa, guess_hist):
        return tentativa
    # se checagem == falso
    del apostas_negativas[-1]
    del apostas_positivas[-1]
    return algoritmo_padrao(guess_hist, lista)


def x_acerto(guess_hist):
    global opcoes
    if (
        len(set(set(whitelist) | set(possibilidades))) == 4
    ):  # se whitelist + possibilidades tiver 4 elementos, então estes 4 são a resposta.
        lista = list(set(set(whitelist) | set(possibilidades)))
        # se checagem == verdadeiro
        if checagem(lista, guess_hist):
            return lista
        # se checagem == falso
        return x_acerto(guess_hist)

    try:
        if (
            historico_modificado[-2][0] == historico_modificado[-1][0] + 1
        ):  # perdeu um acerto
            del historico_modificado[
                -1
            ]  # apaga essa ocorrência para que comparações futuras ocorram devidamente
            whitelist.append(
                apostas_negativas[-1]
            )  # coloca o elemento tirado como certo
            blacklist.append(
                apostas_positivas[-1]
            )  # coloca o elemento inserido como errado
            try:
                if (
                    historico_modificado[-3][0] == historico_modificado[-2][0]
                ):  # se o histórico dos dois anteriores for igual e o deste for menor, significa que a lista de possibilidades estava certa
                    whitelist.extend(
                        possibilidades
                    )  # adiciona as possibilidades à lista de elementos garantidos
                    possibilidades.clear()  # limpa a lista de possibilidades
                    if (
                        len(set(whitelist)) == 3
                    ):  # se a whitelist tiver tamanho 3 (muito alto para depender da função checagem. ela cometeria overflow de tantas recursões até garantir que todo este whitelist esteja presente)
                        lista = list(set(whitelist))
                        opcoes = guess_hist[
                            -1
                        ].copy()  # cria uma lista opções que é igual à tentativa anterior, de resultado 1,x. o código iterará por essa lista adicionando um de seus elementos à lista criada a partir da whitelist de tamanho 3
                        apostas_positivas.append(
                            choice(opcoes)
                        )  # aposta que um dos elementos da lista de oppções está correto
                        lista.append(apostas_positivas[-1])
                        opcoes.remove(apostas_positivas[-1])
                        if checagem(lista, guess_hist):
                            return lista
                        del apostas_positivas[-1]
                        return x_acerto(guess_hist)
            except:
                pass
            lista = guess_hist[-1].copy()
            lista.append(
                apostas_negativas[-1]
            )  # se eu perdi um acerto, então o que eu coloquei está errado, e o que eu tirei está certo.
            lista.remove(apostas_positivas[-1])
            return algoritmo_padrao(guess_hist, lista)
        elif (
            historico_modificado[-2][0] == historico_modificado[-1][0] - 1
        ):  # aumentou um acerto
            try:
                if (
                    historico_modificado[-3][0] == historico_modificado[-2][0]
                ):  # se o histórico dos dois anteriores for igual e o deste for maior, significa que a lista de possibilidades estava errada
                    blacklist.extend(
                        possibilidades
                    )  # adiciona as possibilidades à lista de elementos errados
                    possibilidades.clear()  # limpa a lista de possibilidades
            except:
                pass
            whitelist.append(
                apostas_positivas[-1]
            )  # colcoa o elemento inserido como certo
            blacklist.append(
                apostas_negativas[-1]
            )  # coloca o elemento tirado como errado
            if (
                len(set(whitelist)) == 3
            ):  # se pá que eu preciso adicionar o cado de wl == 2
                lista = guess_hist[-1].copy()  # lista vai ser a ultima tentativa
                lista.remove(apostas_positivas[-1])  # tira a ultima aposta
                blacklist.append(apostas_positivas[-1])  # bane ela
                try:
                    opcoes.remove(apostas_positivas[-1])  # tira das opcoes
                except ValueError:
                    pass
                apostas_positivas.append(choice(opcoes))  # faz outra aposta das opcoes
                lista.append(apostas_positivas[-1])  # adiciona à lista
                if checagem(lista, guess_hist):
                    return lista
                # se checagem == falso
                del apostas_positivas[-1]
                opcoes.append(apostas_positivas[-1])
                blacklist.remove(apostas_positivas[-1])
                return x_acerto(guess_hist)
            lista = guess_hist[-1].copy()
            # lista.append(apostas_positivas[-1])
            # lista.remove(apostas_negativas[-1])
            return algoritmo_padrao(guess_hist, lista)
        else:  # continuou igual o numero de acertos
            lista = guess_hist[-1].copy()
            possibilidades.append(
                apostas_positivas[-1]
            )  # o ultimo elemento adicionado pode estar certo
            possibilidades.append(
                apostas_negativas[-1]
            )  # o ultimo elemento removido pode estar certo
            if len(set(whitelist)) == 3:  # mesmo role de antes
                lista.remove(apostas_positivas[-1])
                blacklist.append(apostas_positivas[-1])
                try:
                    opcoes.remove(apostas_positivas[-1])
                except ValueError:
                    pass
                apostas_positivas.append(choice(opcoes))
                lista.append(apostas_positivas[-1])
                if checagem(lista, guess_hist):
                    return lista
                # se checagem == falso
                del apostas_positivas[-1]
                opcoes.append(apostas_positivas[-1])
                blacklist.remove(apostas_positivas[-1])
                return x_acerto(guess_hist)
            if (
                len(set(set(whitelist) | set(possibilidades))) >= 3
                and apostas_positivas[-1] in whitelist
            ):  # caso extraordinário
                lista = guess_hist[-1].copy()
                whitelist.extend(
                    set(possibilidades)
                )  # possibilidade está certa (mova-a à whitelist)
                possibilidades.clear()
                return algoritmo_padrao(guess_hist, lista)
            if (
                len(set(set(whitelist) | set(possibilidades))) == 4
            ):  # se wl + possibilidades = 4 essa eh a resposta
                lista = list(set(set(whitelist) | set(possibilidades)))
                # se checagem == verdadeiro
                if checagem(lista, guess_hist):
                    return lista
                # se checagem == falso
                return x_acerto(guess_hist)
            if (
                len(set(blacklist)) == 2
                and set(guess_hist[-1]).issuperset(set(whitelist))
                and set(guess_hist[-1]).issuperset(set(possibilidades))
            ):  # se a blacklist tiver tamanho 2 e for superconjunto tanto da whitelist quando das possibilidades,
                lista.append(opcoes[0])  # o que lhe falta é a única opção restante
                # se checagem == verdadeiro
                if checagem(lista, guess_hist):
                    return lista
                # se checagem == falso
                return x_acerto(guess_hist)
            if len(set(blacklist)) == 2:  # se a blacklist tiver tamanho 2
                lista = list(
                    set(set(whitelist) | set(possibilidades))
                )  # lista = whitelist + possibilidades
                opcoes = list(
                    set(guess_hist[-1]) - set(lista)
                )  # opcoes = ultima tentativa - whitelist - possibilidades
                apostas_positivas.append(
                    choice(opcoes)
                )  # aposta que uma opção ta certa
                lista.append(apostas_positivas[-1])
                opcoes.remove(apostas_positivas[-1])
                # se checagem == verdadeiro
                if checagem(lista, guess_hist):
                    return lista
                # se checagem == falso
                opcoes.append(apostas_positivas[-1])
                del apostas_positivas[-1]
                return x_acerto(guess_hist)
            # return x_acerto(guess_hist)
            apostas_negativas.append(apostas_positivas[-1])
            apostas_positivas.append(
                choice(list(set(colors) - set(lista)))
            )  # troca o ultimo elemento adicionado por outro
            lista.remove(apostas_negativas[-1])
            lista.append(apostas_positivas[-1])
            # se checagem == verdadeiro
            if checagem(lista, guess_hist):
                return lista
            # se checagem == falso
            del apostas_negativas[-1]
            del apostas_positivas[-1]
            del possibilidades[-1]
            del possibilidades[-1]
            return x_acerto(guess_hist)

    except IndexError:  # so ocorre se for  imediatamente após a tentativa 0
        return algoritmo_padrao(guess_hist, guess_hist[-1])