"""Questão A4, versão 2: buffer circular com três semáforos.

vazio conta as posições livres (começa em N), cheio conta as posições
ocupadas (começa em 0) e mutex garante exclusão mútua (começa em 1). O
time.sleep(0) da versão 1 continua no mesmo ponto, agora dentro da região
crítica, para mostrar que a mesma interrupção deixa de causar erro.

Uso: python3 versao2.py [--amostras 20000] [--execucoes 3]
"""

import threading
import time

from comum import LIMITE_TRAVAMENTO_S, N, rodar_versao

INTERVALO_VERIFICACAO_S = 0.1


class Estado:
    """Dados compartilhados e semáforos de uma execução."""

    def __init__(self):
        """Cria o buffer vazio e os três semáforos com seus valores iniciais."""
        self.buffer = [-1] * N
        self.ocupadas = 0
        self.parar = False
        self.vazio = threading.Semaphore(N)
        self.cheio = threading.Semaphore(0)
        self.mutex = threading.Semaphore(1)


def esperar_ou_parar(estado, semaforo):
    """Faz wait no semáforo, desistindo se a execução for encerrada.

    Parâmetros:
        estado: dados compartilhados.
        semaforo: semáforo a adquirir.

    Retorno:
        True se adquiriu o semáforo, False se estado.parar foi ligado.
    """
    while not semaforo.acquire(timeout=INTERVALO_VERIFICACAO_S):
        if estado.parar:
            return False
    return True


def produtor(estado, total):
    """Gera as amostras 0 a total-1: wait(vazio), depois wait(mutex).

    Parâmetros:
        estado: dados compartilhados.
        total: quantidade de amostras a produzir.

    Retorno:
        None. Encerra antes do fim se estado.parar for ligado.
    """
    entrada = 0
    for amostra in range(total):
        if not esperar_ou_parar(estado, estado.vazio):
            return
        if not esperar_ou_parar(estado, estado.mutex):
            return
        estado.buffer[entrada] = amostra
        entrada = (entrada + 1) % N
        lido = estado.ocupadas
        time.sleep(0)
        estado.ocupadas = lido + 1
        estado.mutex.release()
        estado.cheio.release()


def consumidor(estado, total, lidas):
    """Retira total amostras: wait(cheio), depois wait(mutex).

    Parâmetros:
        estado: dados compartilhados.
        total: quantidade de leituras a fazer.
        lidas: lista que recebe os valores lidos.

    Retorno:
        True se ficou 1 s sem receber nada (travamento), False caso contrário.
    """
    saida = 0
    for _ in range(total):
        if not estado.cheio.acquire(timeout=LIMITE_TRAVAMENTO_S):
            return True
        if not estado.mutex.acquire(timeout=LIMITE_TRAVAMENTO_S):
            return True
        lidas.append(estado.buffer[saida])
        saida = (saida + 1) % N
        lido = estado.ocupadas
        time.sleep(0)
        estado.ocupadas = lido - 1
        estado.mutex.release()
        estado.vazio.release()
    return False


def executar(total):
    """Roda uma execução completa da versão 2.

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
    rodar_versao("Versão 2: com semáforos", executar)
