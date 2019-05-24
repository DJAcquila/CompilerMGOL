#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
from lexico.analisadorlexico import parse
from sintatico.syn import Shift_Reduce
from common.utility.util import bcolors
from common.file.fileHandler import FileHandler
import argparse


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Compilador da linguagem MGOL - Por enquanto, apenas o analisador léxico")
	parser.add_argument('-l', '--lexico', help='Realiza somente a analise léxica', action="store_true")
	parser.add_argument('-v', '--verbose', help='Ativa o modo verboso do compilador', action="store_true")
	parser.add_argument('-s', '--sintatico', help='Realiza somente a analise lexica e sintatica', action="store_true")
	parser.add_argument('filename')
	args = parser.parse_args()
	if args.filename.find('.alg') < 0:
		print("\n" + bcolors.RED + bcolors.BOLD+ "Erro" + bcolors.END + " ao abrir '{}'".format(args.filename))
		print("O arquivo {} não está na extensão correta para MGOL\n".format(args.filename))
		exit(0)

	file = FileHandler(args.filename)
	tabela_acoes = pd.read_csv("sintatico/erros2.csv")
	#print(tabela_acoes.loc[3]['id'])

	tabela_desvios = pd.read_csv("sintatico/tabela-sintatica-desvios.csv")
	#print (tabela_desvios.loc[0]['P'])

	#gramatica, usadas no algoritmo para o reduce
	regras = pd.read_csv("sintatico/gramatica.csv")

	tabela_erros = pd.read_csv("sintatico/mensagensErros.csv")

	'''_arquivo = open(args.filename, 'r')
		
	lines = _arquivo.readlines()
	eof = _arquivo.tell()'''

	if args.lexico:
		if args.verbose:
			print ("Modo verboso ativado")
		parse(file, args.verbose)

	if args.sintatico:
		Shift_Reduce(file, tabela_acoes, tabela_desvios, regras, tabela_erros)
	else:
		print("Ainda não foram desenvolvidas todas as etapas de compilação\nInsira a diretiva '-l' para execução do analisador léxico")
	