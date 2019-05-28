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

def Shift_Reduce(file, tabela_acoes, tabela_desvios, regras, tabela_erros, tabela_follow):

	lex = LEX_DFA(file)
	tabela_simbolos = SymbTable()
	accept = []
	accept =['erro']
	a = '$'
	linha_s0 = 0
	coluna_s0 = 0

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
					linha_s = linha_s0
					coluna_s = coluna_s0
					a = accept[2]
					linha_s0 = file.linha
					coluna_s0 = file.coluna - len(accept[1])
					#print(a)
				else:
					print('erro lexico: {}'.format(accept[1]))

			else:
				a = '$'
		except TypeError:
			a = '$'
			break

	#print('simbolo: {}'.format(a))
	while True:
		#print('ponteiro: {}'.format(file.ponteiro))
		#print("Inicio: {}".format(pilha.dados))
		s = int(pilha.topo())
		#print(pilha.dados)
		#print('a= {} s={}' .format(a,s))
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
							linha_s = linha_s0
							coluna_s = coluna_s0
							a = accept[2]
							#print(accept[2])
							linha_s0 = file.linha
							coluna_s0 = file.coluna - len(accept[1])
							#print("{} {}".format(accept[1],accept[2]))
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
			#print(tabela_desvios.loc[t][Ant])
			print('a= {} s={}' .format(Ant,t))
			pilha.empilha(int(tabela_desvios.loc[t][Ant]))
			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente']+'\n')

		elif 'acc' in tabela_acoes.loc[s][a]:
			print('aceita')
			tabela_simbolos.print_table()
			break
		else:
			#print('erro')
			#print(pilha.dados)
			#print(len(pilha.dados))
			#print(pilha.dados[0])
			erro_num = tabela_acoes.loc[s][a]
			erro_num = erro_num.split('e')
			erro_num = int(erro_num[1])
			#print(erro_num)
			if erro_num == 8:
				print('Erro sintático:{} {} linha: {} coluna: {}' .format(a,tabela_erros.loc[erro_num]['mensagem'],linha_s0, coluna_s0))
			else:
				print('Erro sintático: {} linha: {} coluna: {}' .format(tabela_erros.loc[erro_num]['mensagem'],linha_s0, coluna_s0))
			if a == '$':
				break
			pilha.desempilha()
			p_index = len(pilha.dados)-1
			#print(pilha.dados)
			#print(p_index)
			flag = 0
			while p_index >= 0 and flag == 0:
			#p_index = pilha.desempilha()
			#while p_index != None and flag == 0:
				#print('p_index: {}'.format(p_index))
				for i in range (0,19):
					nao_terminal = tabela_follow.loc[i]['Variavel']
					#print('nao_terminal: {}'.format(nao_terminal))
					goto = tabela_desvios.loc[pilha.dados[p_index]][nao_terminal]
					if goto != ' ':
						#print('goto: {}' .format(goto))
						pilha.empilha(int(goto))
						#print(pilha.dados)
						flag = 1
						conj_follow = tabela_follow.loc[i]['FOLLOW']
						#if 'pt_v' in conj_follow:
						#	print(conj_follow)
						break
				p_index -= 1
				#empilhar = p_index = pilha.desempilha()
			#tabela_simbolos.print_table()
			#pilha.empilha(empilhar)
			accept = ['erro']
			#print('oi1')
			while(accept[0] == 'erro'):
				#print('oi2')
				try:
					accept = False, None, None, None

					if (file.ponteiro < file.eof):
						accept = lex.dfa.lexico(tabela_simbolos)
						#print('ponteiro:{}\neof:{}'.format(file.ponteiro,file.eof))
						#print('oi3')
						if accept[0] != 'erro':
							#print('oi4')
							linha_s = linha_s0
							coluna_s = coluna_s0
							a = accept[2]
							linha_s0 = file.linha
							coluna_s0 = file.coluna - len(accept[1])
							#print(accept[2])
							if accept[2] not in conj_follow:
								#print('accept {}' .format(accept[2]))
								accept = ['erro']
							#print("{} {}".format(accept[1],accept[2]))
						else:
							print('Erro lexico: {}'.format(accept[1]))
					else:
						a = '$'

				except TypeError:
					a = '$'
					#print(file.ponteiro)
					break
			print('a{}'.format(a))
			print(pilha.dados)
			#break