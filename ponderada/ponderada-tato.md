**Ana Júlia Rodrigues Ribeiro | D1 = 3 | D2 = 4 | N = 7**

## Parâmetros individuais

| Parâmetro | Fórmula | Valor |
|---|---|---|
| Instruções por amostra (IC) | 100.000 + 20.000 × D2 | 180.000 |
| Taxa de falta na cache L1 do SoC (m) | 3% + 0,5% × D1 | 4,5% |
| Tamanho do buffer de amostras (N) | 3 + (D2 mod 5) | 7 |

## PARTE A - Problema Técnico

### A1. Arquitetura e memória: qual processador vai na pulseira?
1. Calcule o tempo para processar uma amostra na Plataforma H, usando o seu IC. Ela atende os 5 ms?

2. Para a Plataforma V, calcule o tempo médio de acesso à memória (AMAT) e o CPI efetivo, usando a sua taxa de falta m. Considere CPI efetivo = 1,0 + (acessos por instrução × m × penalidade). Calcule o tempo por amostra e o pior caso, somando o atraso do sistema operacional. Ela atende os 5 ms?

3. O time oferece um acelerador DSP para a Plataforma H que executa o filtro 5 vezes mais rápido. O filtro é 60% do tempo de processamento. Use a Lei de Amdahl para calcular o speedup global e o novo tempo por amostra. Agora atende?

4. Em até cinco linhas: por que a Plataforma V precisa de cache e a H funciona sem? Use a ideia de gargalo de Von Neumann.

5. **Evidência da sua máquina.** Cole o print das caches do seu computador (Linux: lscpu; macOS: sysctl -a | grep cachesize; Windows: aba Caches do CPU-Z). A sua L1 é dividida em instruções e dados? Então o seu computador é Von Neumann ou Harvard? Justifique.

### A2. Pipeline: o loop do filtro
1. Liste as dependências de dados (RAW) do trecho: qual instrução depende de qual, por qual registrador.

2. Sem forwarding: desenhe o diagrama do pipeline ciclo a ciclo e diga quantos ciclos o trecho leva do primeiro IF ao último WB.

3. Com forwarding: mesmo diagrama e total. Qual dependência continua causando bolha mesmo com forwarding, e por quê?

4. Reordene as instruções, sem mudar o resultado, para eliminar todas as bolhas com forwarding. Mostre a nova ordem e o novo total de ciclos.

### A3. Processos e threads: como organizar o software
1. Proponha uma organização: quais tarefas viram threads de um mesmo processo e quais viram processos separados. Justifique com compartilhamento de memória, custo de criação e troca de contexto e isolamento de falhas.

2. O módulo BLE recebe dados de fora. Se alguém explorar uma falha nele, que diferença faz ele ser uma thread ou um processo separado?

3. Desenhe o diagrama de estados de um processo. Em qual estado a thread do sensor passa a maior parte do tempo? Por quê?

### A4. Código com semáforos: o buffer entre o sensor e o motor
1. Versão 1, sem sincronização. Use um contador compartilhado de posições ocupadas e espera ocupada. Para a condição de corrida aparecer, coloque um time.sleep(0) (em C, sched_yield()) entre ler e escrever o contador: isso simula a thread sendo interrompida no pior momento. Se o consumidor ficar 1 s sem receber nada, encerre e registre como travamento.

2. Versão 2, com semáforos. Três semáforos: vazio (começa em N), cheio (começa em 0) e mutex (começa em 1).

3. Versão 3, ordem trocada. Igual à versão 2, mas o produtor faz wait(mutex) antes de wait(vazio).

Rode cada versão 3 vezes com 20.000 amostras. No ponderada-tato.md, entregue:
- Uma tabela com, para cada execução: amostras consumidas, perdidas, duplicadas e se travou.
- O print de pelo menos uma execução de cada versão.
- Qual é a região crítica da versão 1, e por que ela perde ou duplica amostras.
- O que cada um dos três semáforos garante na versão 2.
- O que aconteceu na versão 3, e por quê.


### A5. Deadlock: a pulseira congelou
1. Descreva uma sequência de execução que leva ao deadlock e desenhe o grafo de alocação de recursos nesse instante.

2. Mostre como cada uma das quatro condições necessárias para o deadlock aparece nesse código.

3. Proponha duas correções de tipos diferentes (por exemplo, uma de prevenção e uma de detecção e recuperação). Para cada uma, diga o que muda para quem está usando a pulseira.




## PARTE B - Decisão como CTO
