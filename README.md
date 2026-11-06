# Ponderada CC08: do pipeline ao deadlock

**Nome:** Ana Júlia Rodrigues Ribeiro

**Descrição:** análise de arquitetura, pipeline, concorrência e deadlock aplicada à pulseira sensorial Tato, com a decisão do CTO.

## Instruções para rodar o código

Requer Python 3 e não tem dependências externas. Na raiz do repositório, entre na pasta do código:

```bash
cd ponderada/codigo
```

Cada comando roda uma versão da questão A4, com 3 execuções de 20.000 amostras e N = 7:

```bash
python3 versao1.py   # sem sincronização
python3 versao2.py   # com semáforos
python3 versao3.py   # ordem dos semáforos trocada no produtor
```

Para mudar a carga, use `--amostras` e `--execucoes`, por exemplo `python3 versao1.py --amostras 1000 --execucoes 1`.

A resposta completa está em [`ponderada/ponderada-tato.md`](ponderada/ponderada-tato.md).
