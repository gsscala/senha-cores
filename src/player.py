import achar_cores
import permutar_cores

def player(guess_hist, res_hist):
    try:
        match res_hist[-1][0]:
            case 4:
                return permutar_cores.quatro_acertos(guess_hist, res_hist)
            case _:
                try:
                    achar_cores.historico_modificado.append(res_hist[-1])
                except:
                    pass
                return achar_cores.x_acerto(guess_hist)
    except IndexError:  # primeira jogada
        return achar_cores.sample(achar_cores.colors, 4)  # coleta 4 elementos aleatórios da lista de cores