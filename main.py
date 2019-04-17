# -*- coding: utf-8 -*-
from lexico.analisadorlexico import analisador_lexico
from lexico.util import bcolors
import argparse


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Compilador da linguagem MGOL - Por enquanto, apenas o analisador léxico")
	parser.add_argument('-l', '--lexico', help='Realiza somente a analise léxica', action="store_true")
	parser.add_argument('filename')
	args = parser.parse_args()
	if args.filename.find('.alg') < 0:
		print("\n" + bcolors.RED + bcolors.BOLD+ "Erro" + bcolors.END + " ao abrir '{}'".format(args.filename))
		print("O arquivo não está na extensão correta para MGOL\n".format(args.filename))
		exit(0)

	_arquivo = open(args.filename, 'r')
		
	lines = _arquivo.readlines()
	eof = _arquivo.tell()

	if args.lexico:
		analisador_lexico(_arquivo, lines, eof)
	else:
		print("Nada a fazer")
	