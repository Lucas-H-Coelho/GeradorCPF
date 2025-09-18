#!/usr/bin/env python3
"""
Gerador otimizado de CPFs válidos usando divisão em 4 partes separadas
Gera CSVs por parte e depois combina e valida
"""

import csv
import json
import os
import time
import multiprocessing as mp
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Any, Generator
import argparse
import logging


class CPFValidator:
        
    @staticmethod
    def valida_cpf(cpf: str, silent: bool = True) -> Tuple[bool, str, str]:
        """
        Função de validação original adaptada para uso em lote
        Retorna: (é_válido, cpf_sem_formato, cpf_formatado)
        """
        original_cpf = cpf
        cpf = cpf.replace('.', '').replace('-', '')
        
        if len(cpf) == 11:
            validar = True
            digitos_verificadores = cpf[9:]
        else:
            validar = False
            
        cpf_9_digitos = cpf[:9]
        
        try:
            dig_1 = int(cpf_9_digitos[0]) * 1
            dig_2 = int(cpf_9_digitos[1]) * 2
            dig_3 = int(cpf_9_digitos[2]) * 3
            dig_4 = int(cpf_9_digitos[3]) * 4
            dig_5 = int(cpf_9_digitos[4]) * 5
            dig_6 = int(cpf_9_digitos[5]) * 6
            dig_7 = int(cpf_9_digitos[6]) * 7
            dig_8 = int(cpf_9_digitos[7]) * 8
            dig_9 = int(cpf_9_digitos[8]) * 9
        except (IndexError, ValueError):
            if not silent:
                print('Quantidade de caracteres incorreto ou caracteres inválidos.')
            return False, "", ""
            
        dig_1_ao_9_somados = (dig_1 + dig_2 + dig_3 + dig_4 + dig_5 + dig_6 + dig_7 + dig_8 + dig_9)
        dig_10 = dig_1_ao_9_somados % 11
        if dig_10 > 9:
            dig_10 = 0
            
        cpf_10_digitos = cpf_9_digitos + str(dig_10)
        
        dig_1 = int(cpf_10_digitos[0]) * 0
        dig_2 = int(cpf_10_digitos[1]) * 1
        dig_3 = int(cpf_10_digitos[2]) * 2
        dig_4 = int(cpf_10_digitos[3]) * 3
        dig_5 = int(cpf_10_digitos[4]) * 4
        dig_6 = int(cpf_10_digitos[5]) * 5
        dig_7 = int(cpf_10_digitos[6]) * 6
        dig_8 = int(cpf_10_digitos[7]) * 7
        dig_9 = int(cpf_10_digitos[8]) * 8
        dig_10 = int(cpf_10_digitos[9]) * 9
        
        dig_1_ao_10_somados = (dig_1 + dig_2 + dig_3 + dig_4 + dig_5 + dig_6 + dig_7 + dig_8 + dig_9 + dig_10)
        dig_11 = dig_1_ao_10_somados % 11
        if dig_11 > 9:
            dig_11 = 0
            
        cpf_validado = cpf_10_digitos + str(dig_11)
        cpf_formatado = (cpf_validado[:3] + '.' + cpf_validado[3:6] + '.' +
                        cpf_validado[6:9] + '-' + cpf_validado[9:])
        
        if validar:
            is_valid = digitos_verificadores == cpf_validado[9:]
            if not silent:
                if is_valid:
                    print('Os dígitos verificadores estão corretos.')
                else:
                    print('Os dígitos verificadores estão incorretos.')
                    print(f'CPF: {cpf_formatado}')
            return is_valid, cpf_validado, cpf_formatado
        else:
            if not silent:
                print(f'CPF: {cpf_formatado}')
            return True, cpf_validado, cpf_formatado


class CPFPartGenerator:
    """Gerador de partes individuais de CPF"""
    
    def __init__(self, output_dir: str = "cpf_parts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Configura logging"""
        logger = logging.getLogger('cpf_part_generator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def gerar_parte_csv(self, parte_num: int, inicio: int = 0, fim: int = 999) -> str:
        """Gera CSV com todas as combinações para uma parte específica (1, 2, 3 ou 4)"""
        if parte_num == 4:
            # Parte 4 são os dígitos verificadores (00-99)
            output_file = self.output_dir / f"parte_4_digitos_verificadores.csv"
            inicio, fim = 0, 99
            formato = "{:02d}"
        else:
            # Partes 1, 2, 3 são blocos de 3 dígitos (000-999)
            output_file = self.output_dir / f"parte_{parte_num}.csv"
            formato = "{:03d}"
        
        self.logger.info(f"Gerando parte {parte_num}: {inicio} a {fim}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f'parte_{parte_num}'])
            
            count = 0
            for i in range(inicio, fim + 1):
                valor = formato.format(i)
                writer.writerow([valor])
                count += 1
                
        self.logger.info(f"Parte {parte_num} concluída: {count} valores em {output_file}")
        return str(output_file)
    
    def gerar_todas_as_partes(self, 
                             parte1_range: Tuple[int, int] = (0, 999),
                             parte2_range: Tuple[int, int] = (0, 999),
                             parte3_range: Tuple[int, int] = (0, 999)) -> Dict[str, str]:
        """Gera todos os 4 CSVs de partes"""
        
        self.logger.info("Iniciando geração de todas as partes...")
        inicio = datetime.now()
        
        arquivos = {}
        
        # Gera partes 1, 2, 3
        arquivos['parte_1'] = self.gerar_parte_csv(1, parte1_range[0], parte1_range[1])
        arquivos['parte_2'] = self.gerar_parte_csv(2, parte2_range[0], parte2_range[1])
        arquivos['parte_3'] = self.gerar_parte_csv(3, parte3_range[0], parte3_range[1])
        
        # Gera parte 4 (dígitos verificadores - sempre 00 a 99)
        arquivos['parte_4'] = self.gerar_parte_csv(4)
        
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        
        self.logger.info(f"Todas as partes geradas em {duracao:.2f}s")
        
        # Salva informações sobre os arquivos gerados
        info_file = self.output_dir / "partes_info.json"
        info = {
            'timestamp': inicio.isoformat(),
            'duracao_segundos': duracao,
            'arquivos_gerados': arquivos,
            'ranges': {
                'parte1': parte1_range,
                'parte2': parte2_range,
                'parte3': parte3_range,
                'parte4': (0, 99)
            }
        }
        
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, default=str)
            
        return arquivos


class CPFCombiner:
    """Combina as 4 partes e valida CPFs completos"""
    
    def __init__(self, parts_dir: str = "cpf_parts", output_dir: str = "cpf_output"):
        self.parts_dir = Path(parts_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.validator = CPFValidator()
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Configura logging"""
        logger = logging.getLogger('cpf_combiner')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def ler_parte_csv(self, parte_num: int) -> List[str]:
        """Lê valores de uma parte específica do CSV"""
        if parte_num == 4:
            arquivo = self.parts_dir / "parte_4_digitos_verificadores.csv"
        else:
            arquivo = self.parts_dir / f"parte_{parte_num}.csv"
            
        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo da parte {parte_num} não encontrado: {arquivo}")
        
        valores = []
        with open(arquivo, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Pula cabeçalho
            for row in reader:
                if row:  # Ignora linhas vazias
                    valores.append(row[0])
        
        return valores
    
    def combinar_e_validar(self, 
                          output_file: str = None,
                          batch_size: int = 10000,
                          max_cpfs: int = None) -> Dict[str, Any]:
        """
        Combina todas as partes e valida CPFs completos usando sua função
        """
        if output_file is None:
            output_file = str(self.output_dir / "cpfs_validos_final.csv")
        
        self.logger.info("Iniciando combinação e validação...")
        inicio = datetime.now()
        
        # Carrega todas as partes
        self.logger.info("Carregando partes dos CSVs...")
        parte1_valores = self.ler_parte_csv(1)
        parte2_valores = self.ler_parte_csv(2)
        parte3_valores = self.ler_parte_csv(3)
        parte4_valores = self.ler_parte_csv(4)
        
        self.logger.info(f"Partes carregadas: P1={len(parte1_valores)}, P2={len(parte2_valores)}, P3={len(parte3_valores)}, P4={len(parte4_valores)}")
        
        # Calcula total de combinações
        total_combinacoes = len(parte1_valores) * len(parte2_valores) * len(parte3_valores) * len(parte4_valores)
        self.logger.info(f"Total de combinações a processar: {total_combinacoes:,}")
        
        stats = {
            'inicio': inicio,
            'total_combinacoes': total_combinacoes,
            'total_processados': 0,
            'total_validos': 0,
            'total_invalidos': 0,
            'sequencias_repetidas': 0,
            'output_file': output_file
        }
        
        # Processa combinações
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['cpf'])
            
            batch = []
            processados = 0
            
            for p1 in parte1_valores:
                for p2 in parte2_valores:
                    for p3 in parte3_valores:
                        for p4 in parte4_valores:
                            # Monta CPF completo
                            cpf_completo = f"{p1}{p2}{p3}{p4}"
                            processados += 1
                            
                            # Verifica sequência repetida
                            if cpf_completo == cpf_completo[0] * 11:
                                stats['sequencias_repetidas'] += 1
                                continue
                            
                            # Valida
                            is_valid, cpf_validado, cpf_formatado = self.validator.valida_cpf(cpf_completo, silent=True)
                            
                            if is_valid:
                                batch.append([cpf_validado])
                                stats['total_validos'] += 1
                            else:
                                stats['total_invalidos'] += 1
                            
                            # Escreve batch
                            if len(batch) >= batch_size:
                                writer.writerows(batch)
                                batch = []
                            
                            # Progress log
                            if processados % 100000 == 0:
                                self.logger.info(f"Processados: {processados:,} | Válidos: {stats['total_validos']:,} | Taxa: {(stats['total_validos']/processados*100):.2f}%")
                            
                            # Limite máximo se especificado
                            if max_cpfs and stats['total_validos'] >= max_cpfs:
                                self.logger.info(f"Limite de {max_cpfs:,} CPFs válidos atingido")
                                break
                                
                        if max_cpfs and stats['total_validos'] >= max_cpfs:
                            break
                    if max_cpfs and stats['total_validos'] >= max_cpfs:
                        break
                if max_cpfs and stats['total_validos'] >= max_cpfs:
                    break
            
            # Escreve batch restante
            if batch:
                writer.writerows(batch)
        
        stats['fim'] = datetime.now()
        stats['total_processados'] = processados
        stats['duracao_segundos'] = (stats['fim'] - stats['inicio']).total_seconds()
        stats['taxa_validez'] = (stats['total_validos'] / stats['total_processados'] * 100) if stats['total_processados'] > 0 else 0
        
        # Salva relatório
        relatorio_file = self.output_dir / "relatorio_combinacao.json"
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, default=str)
        
        self.logger.info("=== COMBINAÇÃO CONCLUÍDA ===")
        self.logger.info(f"Total processados: {stats['total_processados']:,}")
        self.logger.info(f"CPFs válidos: {stats['total_validos']:,}")
        self.logger.info(f"CPFs inválidos: {stats['total_invalidos']:,}")
        self.logger.info(f"Sequências repetidas: {stats['sequencias_repetidas']:,}")
        self.logger.info(f"Taxa de validez: {stats['taxa_validez']:.2f}%")
        self.logger.info(f"Duração: {stats['duracao_segundos']:.2f}s")
        self.logger.info(f"Arquivo final: {output_file}")
        self.logger.info(f"Relatório: {relatorio_file}")
        
        return stats


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Gerador CPF por Partes Separadas')
    parser.add_argument('--action', choices=['gerar-partes', 'combinar', 'completo'], 
                       default='completo', help='Ação a executar')
    parser.add_argument('--parts-dir', default='cpf_parts',
                       help='Diretório das partes')
    parser.add_argument('--output-dir', default='cpf_output',
                       help='Diretório de saída')
    parser.add_argument('--parte1-inicio', type=int, default=0)
    parser.add_argument('--parte1-fim', type=int, default=999)
    parser.add_argument('--parte2-inicio', type=int, default=0)
    parser.add_argument('--parte2-fim', type=int, default=999)
    parser.add_argument('--parte3-inicio', type=int, default=0)
    parser.add_argument('--parte3-fim', type=int, default=999)
    parser.add_argument('--max-cpfs', type=int,
                       help='Limite máximo de CPFs válidos a gerar')
    parser.add_argument('--batch-size', type=int, default=10000,
                       help='Tamanho do batch para gravação')
    parser.add_argument('--sample', action='store_true',
                       help='Executa sample pequeno (000-009 para cada parte)')
    
    args = parser.parse_args()
    
    # Modo sample
    if args.sample:
        args.parte1_inicio = 0
        args.parte1_fim = 9
        args.parte2_inicio = 0
        args.parte2_fim = 9
        args.parte3_inicio = 0
        args.parte3_fim = 9
        args.max_cpfs = 1000  # Limita para teste
        print("🧪 Modo SAMPLE ativado")
    
    parte1_range = (args.parte1_inicio, args.parte1_fim)
    parte2_range = (args.parte2_inicio, args.parte2_fim)
    parte3_range = (args.parte3_inicio, args.parte3_fim)
    
    if args.action in ['gerar-partes', 'completo']:
        # Gera as 4 partes
        print("📋 Gerando partes...")
        part_generator = CPFPartGenerator(args.parts_dir)
        arquivos = part_generator.gerar_todas_as_partes(
            parte1_range, parte2_range, parte3_range
        )
        print("✅ Partes geradas!")
        for nome, arquivo in arquivos.items():
            print(f"  {nome}: {arquivo}")
    
    if args.action in ['combinar', 'completo']:
        # Combina e valida
        print("🔄 Combinando partes e validando...")
        combiner = CPFCombiner(args.parts_dir, args.output_dir)
        stats = combiner.combinar_e_validar(
            batch_size=args.batch_size,
            max_cpfs=args.max_cpfs
        )
        print("✅ Combinação concluída!")
        print(f"📊 CPFs válidos gerados: {stats['total_validos']:,}")
        print(f"📁 Arquivo final: {stats['output_file']}")


if __name__ == '__main__':
    main()