"""Questão A4, versão 1: buffer circular sem sincronização.

Produtor e consumidor usam um contador compartilhado de posições ocupadas
e espera ocupada. O time.sleep(0) entre ler e escrever o contador simula a
thread sendo interrompida no pior momento, o que expõe a condição de corrida.

O time.sleep(0) dentro dos laços de espera apenas cede o GIL a cada volta: a
espera continua ocupada, mas cada execução leva segundos em vez de um minuto.

Uso: python3 versao1.py [--amostras 20000] [--execucoes 3]
"""

import threading
import time

from comum import LIMITE_TRAVAMENTO_S, N, rodar_versao


class Estado:
    """Dados compartilhados entre as threads, sem nenhuma proteção."""

    def __init__(self):
        """Cria o buffer vazio, com -1 marcando posições nunca escritas.

        Parâmetros:
            nenhum.

        Retorno:
            None.
        """
        self.buffer = [-1] * N
        self.ocupadas = 0
        self.parar = False


def produtor(estado, total):
    """Gera as amostras 0 a total-1 e as coloca no buffer.

    Parâmetros:
        estado: dados compartilhados.
        total: quantidade de amostras a produzir.

    Retorno:
        None. Encerra antes do fim se estado.parar for ligado.
    """
    entrada = 0
    for amostra in range(total):
        while estado.ocupadas == N:
            if estado.parar:
                return
            time.sleep(0)
        estado.buffer[entrada] = amostra
        entrada = (entrada + 1) % N
        lido = estado.ocupadas
        time.sleep(0)
        estado.ocupadas = lido + 1


def consumidor(estado, total, lidas):
    """Retira até total leituras do buffer, anotando cada valor.

    Parâmetros:
        estado: dados compartilhados.
        total: quantidade de leituras a fazer.
        lidas: lista que recebe os valores lidos.

    Retorno:
        True se ficou 1 s sem receber nada (travamento), False caso contrário.
    """
    saida = 0
    for _ in range(total):
        ultimo_recebimento = time.monotonic()
        while estado.ocupadas == 0:
            if time.monotonic() - ultimo_recebimento > LIMITE_TRAVAMENTO_S:
                return True
            time.sleep(0)
        lidas.append(estado.buffer[saida])
        saida = (saida + 1) % N
        lido = estado.ocupadas
        time.sleep(0)
        estado.ocupadas = lido - 1
    return False


def executar(total):
    """Roda uma execução completa da versão 1.

    Parâmetros:
        total: quantidade de amostras da execução.

    Retorno:
        Tupla (lidas, travou) com os valores lidos e o estado de travamento.
    """
    estado = Estado()
    lidas = []
    thread = threading.Thread(target=produtor, args=(estado, total))
    thread.start()
    travou = consumidor(estado, total, lidas)
    estado.parar = True
    thread.join()
    return lidas, travou


if __name__ == "__main__":
    rodar_versao("Versão 1: sem sincronização", executar)
