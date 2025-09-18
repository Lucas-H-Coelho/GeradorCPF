---

# 🚀 Gerador Otimizado de CPFs Válidos

Um script em Python para gerar massivamente números de CPF válidos. Utiliza uma abordagem otimizada, dividindo o processo em geração de "partes" e posterior combinação, ideal para criar grandes datasets de CPFs para fins de teste e desenvolvimento.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=yellow)![License](https://img.shields.io/badge/License-MIT-green)![Status](https://img.shields.io/badge/Status-Ativo-brightgreen)

---

## 🎯 Conceito Principal

A geração de todos os CPFs possíveis (1 trilhão de combinações) para validação é um processo computacionalmente intenso. Este script otimiza a tarefa ao dividir o CPF em quatro partes:

-   **Parte 1:** Os três primeiros dígitos (`XXX`).
-   **Parte 2:** Os três dígitos seguintes (`XXX`).
-   **Parte 3:** Os três dígitos subsequentes (`XXX`).
-   **Parte 4:** Os dois dígitos verificadores (`XX`).

O script primeiro gera todas as combinações possíveis para cada parte em arquivos `.csv` separados. Em seguida, ele combina essas partes para montar CPFs completos e os valida usando o algoritmo padrão, salvando apenas os válidos. Essa abordagem segmentada permite maior controle e escalabilidade.

> **Aviso:** Esta ferramenta foi desenvolvida para fins educacionais e de teste de software. A geração e o uso de dados pessoais para fins ilícitos são crime.

---

## ✨ Funcionalidades

-   **Geração Massiva:** Capaz de gerar milhões de CPFs válidos.
-   **Estratégia de 4 Partes:** Otimiza o processo de geração e validação.
-   **Interface de Linha de Comando (CLI):** Controle total sobre a execução via `argparse`.
-   **Modos Flexíveis:** Execute o processo completo, apenas a geração das partes ou apenas a combinação.
-   **Ranges Customizáveis:** Defina faixas numéricas específicas para as partes 1, 2 e 3.
-   **Modo de Amostra (`--sample`):** Execute um teste rápido com um pequeno conjunto de dados.
-   **Gravação em Lotes (`batch`):** Otimiza o uso de memória e disco durante a escrita do arquivo final.
-   **Relatórios Detalhados:** Gera arquivos `.json` com estatísticas completas do processo.
-   **Logging Informativo:** Acompanhe cada etapa da execução em tempo real.
-   **Sem Dependências Externas:** Utiliza apenas bibliotecas padrão do Python.

---

## 🔧 Requisitos

-   **Python 3.7 ou superior.**

Nenhuma biblioteca externa é necessária para a execução do script.

---

## ⚙️ Como Usar

1.  Salve o código com um nome, por exemplo, `gerador_cpf.py`.
2.  Abra um terminal ou prompt de comando no diretório onde o arquivo foi salvo.
3.  Execute os comandos abaixo conforme sua necessidade.

### Comandos Principais

#### 1. Execução Completa (Padrão)
Gera as partes e depois as combina, criando o arquivo final com os CPFs válidos.

```bash
python gerador_cpf.py --action completo
```

#### 2. Modo Amostra (Recomendado para Testes)
Executa o processo completo usando um pequeno intervalo de números (0 a 9 para as partes 1, 2 e 3), ideal para um teste rápido.

```bash
python gerador_cpf.py --sample```

#### 3. Gerar Apenas as Partes
Cria apenas os arquivos `.csv` no diretório `cpf_parts/`.

```bash
python gerador_cpf.py --action gerar-partes
```

#### 4. Combinar Partes Já Existentes
Assume que os arquivos de partes já existem no diretório `cpf_parts/` e executa apenas a combinação e validação.

```bash
python gerador_cpf.py --action combinar
```

### Argumentos Avançados

#### Definir Ranges Customizados
Gere CPFs dentro de uma faixa específica. Útil para segmentar a geração.

```bash
# Gera CPFs começando com 000.XXX.XXX-XX até 099.XXX.XXX-XX
python gerador_cpf.py --parte1-inicio 0 --parte1-fim 99
```

#### Limitar a Quantidade de CPFs
Pare a execução após atingir um número máximo de CPFs válidos.

```bash
python gerador_cpf.py --max-cpfs 10000
```

#### Alterar Diretórios
Especifique diretórios de saída diferentes para as partes e para o resultado final.

```bash
python gerador_cpf.py --parts-dir ./minhas_partes --output-dir ./meu_resultado
```

---

## 📁 Estrutura de Arquivos Gerados

Após uma execução completa, a seguinte estrutura de diretórios e arquivos será criada:

```
.
├── gerador_cpf.py
│
├── cpf_parts/
│   ├── parte_1.csv
│   ├── parte_2.csv
│   ├── parte_3.csv
│   ├── parte_4_digitos_verificadores.csv
│   └── partes_info.json                # Relatório da geração das partes
│
└── cpf_output/
    ├── cpfs_validos_final.csv          # Arquivo final com CPFs válidos
    └── relatorio_combinacao.json       # Relatório da combinação e validação
```

---

## 🛠️ Como Funciona

O script é dividido em três componentes principais:

1.  **`CPFValidator`**: Uma classe que contém a lógica de validação matemática de um CPF.
2.  **`CPFPartGenerator`**: Responsável por criar os 4 arquivos `.csv`. Cada arquivo contém todas as combinações para uma das partes do CPF (ex: `parte_1.csv` contém números de `000` a `999`).
3.  **`CPFCombiner`**: Lê os 4 arquivos `.csv`, itera sobre todas as combinações possíveis (`p1 + p2 + p3 + p4`), valida cada uma usando o `CPFValidator` e escreve os CPFs válidos no arquivo de saída.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.