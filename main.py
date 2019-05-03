#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lexico.analisadorlexico import parse
from common.utility.util import bcolors
from common.file.fileHandler import FileHandler
import argparse


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Compilador da linguagem MGOL - Por enquanto, apenas o analisador léxico")
	parser.add_argument('-l', '--lexico', help='Realiza somente a analise léxica', action="store_true")
	parser.add_argument('-v', '--verbose', help='Ativa o modo verboso do compilador', action="store_true")
	parser.add_argument('filename')
	args = parser.parse_args()
	if args.filename.find('.alg') < 0:
		print("\n" + bcolors.RED + bcolors.BOLD+ "Erro" + bcolors.END + " ao abrir '{}'".format(args.filename))
		print("O arquivo {} não está na extensão correta para MGOL\n".format(args.filename))
		exit(0)

	file = FileHandler(args.filename)

	'''_arquivo = open(args.filename, 'r')
		
	lines = _arquivo.readlines()
	eof = _arquivo.tell()'''

	if args.lexico:
		if args.verbose:
			print ("Modo verboso ativado")
		parse(file, args.verbose)
	else:
		print("Ainda não foram desenvolvidas todas as etapas de compilação\nInsira a diretiva '-l' para execução do analisador léxico")
	