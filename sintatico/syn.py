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

def Shift_Reduce(file, tabela_acoes, tabela_desvios, regras):

	lex = LEX_DFA(file)
	tabela_simbolos = SymbTable()
	accept = []
	accept =['erro']
	a = '$'

	pilha = Pilha()
	pilha.empilha(0)
	#a = 'id' #simbolo do lexico
	while(accept[0] == 'erro'):	
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
					print('erro lexico: {}'.format(accept[1]))

			else:
				a = '$'
		except TypeError:
			a = '$'
			break

	print('simbolo: {}'.format(a))
	while True:
		#print('ponteiro: {}'.format(file.ponteiro))
		#print("Inicio: {}".format(pilha.dados))
		s = int(pilha.topo())
		#print('topo: {}'.format(s))
		if 's' in tabela_acoes.loc[s][a]:
			t = tabela_acoes.loc[s][a]
			print('acao shift {}\n' .format(t))
			t = t.split('s')
			t = int(t[1])
			#print(t)
			pilha.empilha(int(t))
			#a = #proximo simbolo de entrada
			accept = ['erro']
			while(accept[0] == 'erro'):
				try:
					accept = False, None, None, None

					if (file.ponteiro < file.eof):
						accept = lex.dfa.lexico(tabela_simbolos)
						#print('ponteiro:{}\neof:{}'.format(file.ponteiro,file.eof))
						if accept[0] != 'erro':
							a = accept[2]
							print("{} {}".format(accept[1],accept[2]))
						else:
							print('Erro lexico: {}'.format(accept[1]))
					else:
						a = '$'

				except TypeError:
					a = '$'
					#print(file.ponteiro)
					break
			#print('simbolo: {} '.format(a))
		elif 'r' in tabela_acoes.loc[s][a]:
			red = tabela_acoes.loc[s][a]
			print('acao reduce {}' .format(red))
			red = red.split('r')
			red = int(red[1])
			B_simbols = int(regras.loc[red]['B_number'])
			#print(B_simbols)
			while (B_simbols > 0):
				pilha.desempilha()
				#print("Depois do desempilha: {}".format(pilha.dados))
				B_simbols-= 1
			#print("Depois do while: {}".format(pilha.dados))
			t = pilha.topo()
			#print('topo: {}'.format(t))
			Ant = regras.loc[red]['Antecedente']
			#print(Ant)
			pilha.empilha(int(tabela_desvios.loc[t][Ant]))
			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente']+'\n')

		elif 'acc' in tabela_acoes.loc[s][a]:
			print('aceita')
			tabela_simbolos.print_table()
			break
		else:
			print('erro')
			tabela_simbolos.print_table()
			break