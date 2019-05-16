#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import string
from common.utility.util import *
from common.erro.errno import Error
from common.symbtable.table import SymbTable
from common.file.fileHandler import FileHandler
from lexico.analisadorlexico import *

class Pilha(object):
	def __init__(self):
		self.dados = []

	def empilha(self, simbolo):
		self.dados.append(simbolo)

	def desempilha(self):
		if not self.vazia():
			return self.dados.pop(-1)

	def vazia(self):
		return len(self.dados) == 0

	def topo(self):
		indice = len(self.dados) - 1
		return self.dados[indice]

# def Shift_Reduce():
# 	pilha = Pilha()
# 	pilha.empilha(18)
# 	a = 'id' #simbolo do lexico
# 	while True:
# 		s = int(pilha.desempilha())
# 		if 's' in tabela_acoes.loc[s][a]:
# 			print('acao shift')
# 			t = tabela_acoes.loc[s][a]
# 			t = t.split('s')
# 			t = int(t[1])
# 			pilha.empilha(int(t))
# 			#a = #proximo simbolo de entrada
# 		elif 'r' in tabela_acoes.loc[s][a]:
# 			print('acao reduce')
# 			red = tabela_acoes.loc[s][a]
# 			red = red.split('r')
# 			red = int(red[1])
# 			B_simbols = int(regras.loc[red]['B_number'])
# 			while (B_simbols > 0):
# 				print(pilha.desempilha())
# 				B_simbols-= B_simbols
# 			t = pilha.desempilha()
# 			A = regras.loc[red]['Antecedente']
# 			print(A)
# 			pilha.empilha(tabela_desvios.loc[t][A])
# 			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente'])

# 		elif 'acc' in tabela_acoes.loc[s][a]:
# 			print('aceita')
# 			break
# 		else:
# 			print('erro')

def Shift_Reduce(file, tabela_acoes, tabela_desvios, regras):

	lex = LEX_DFA(file)
	tabela_simbolos = SymbTable()

	pilha = Pilha()
	pilha.empilha(0)
	#a = 'id' #simbolo do lexico
	try:
		accept = False, None, None, None
		if (file.ponteiro < file.eof):
			#p = int(tok)
			accept = lex.dfa.lexico(tabela_simbolos)
			if accept[0] != 'erro':
				#print('\nLexema: {}\nToken: {}\nTipo: {}\n'.format(accept[1],accept[2],accept[3]))
				a = accept[2]
				print(a)

		else:
			a='$'
	except TypeError:
		pass

	while True:
		print("Inicio: {}".format(pilha.dados))
		s = int(pilha.topo())
		print('topo: {}'.format(s))
		if 's' in tabela_acoes.loc[s][a]:
			print('acao shift')
			t = tabela_acoes.loc[s][a]
			t = t.split('s')
			t = int(t[1])
			print(t)
			pilha.empilha(int(t))
			#a = #proximo simbolo de entrada
			try:
				accept = False, None, None, None
				if (file.ponteiro < file.eof):
					#p = int(tok)
					accept = lex.dfa.lexico(tabela_simbolos)
					if accept[0] != 'erro':
						#print('\nLexema: {}\nToken: {}\nTipo: {}\n'.format(accept[1],accept[2],accept[3]))
						a = accept[2]
						#print(a)

				else:
					a='$'
			except TypeError:
				pass
			print(a)
		elif 'r' in tabela_acoes.loc[s][a]:
			print('acao reduce')
			red = tabela_acoes.loc[s][a]
			red = red.split('r')
			red = int(red[1])
			B_simbols = int(regras.loc[red]['B_number'])
			print(B_simbols)
			while (B_simbols > 0):
				pilha.desempilha()
				print("Depois do desempilha: {}".format(pilha.dados))
				B_simbols-= 1
			print("Depois do while: {}".format(pilha.dados))
			t = pilha.topo()
			print('topo: {}'.format(t))
			Ant = regras.loc[red]['Antecedente']
			print(Ant)
			pilha.empilha(tabela_desvios.loc[t][Ant])
			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente'])

		elif 'acc' in tabela_acoes.loc[s][a]:
			print('aceita')
			break
		else:
			print('erro')
			break

#while True:
#	topo_pilha_s = 
#	if ACTION(topo_pilha_s,token_a) == st:
#		empilha(t)
		
#if __name__ == "__main__":

#	Shift_Reduce()