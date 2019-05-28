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
	a_antigo = 'nao'
	flag_a_antigo = 3

	pilha = Pilha()
	pilha.empilha(0)
	flag_sintatico = 0
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
		if flag_a_antigo == 1:
			flag_a_antigo = 0
			#print('flag 1')
		elif flag_a_antigo == 0:
			#print('flag2')
			a = a_antigo
			flag_a_antigo = 3
		#print('a inicial = {} flag = {}'.format(a,flag_a_antigo))
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
			if flag_a_antigo == 3:
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
			#print('a= {} s= {}' .format(a,s))

			pilha.empilha(int(tabela_desvios.loc[t][Ant]))
			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente']+'\n')

		elif 'acc' in tabela_acoes.loc[s][a]:
			if flag_sintatico == 0:
				print('aceita')
				tabela_simbolos.print_table()
			else:
				print('rejeita')
			break
		else:
			flag_sintatico = 1
			#print('erro')
			#print(pilha.dados)
			#print(len(pilha.dados))
			#print(pilha.dados[0])
			#print("a: {}\ns: {}\n".format(a, s))
			erro_num = tabela_acoes.loc[s][a]
			erro_num = erro_num.split('e')
			erro_num = int(erro_num[1])
			#print(erro_num)
			if erro_num == 8:
				print("Erro sintático: '{}' {} (linha: {} coluna: {})" .format(a,tabela_erros.loc[erro_num]['mensagem'],linha_s0, coluna_s0))
			elif erro_num == 25 or erro_num == 6 or erro_num == 26:
				print("Erro sintático: {} '{}' (linha: {} coluna: {})" .format(tabela_erros.loc[erro_num]['mensagem'], a,linha_s0, coluna_s0))
			else:
				print('Erro sintático: {} (linha: {} coluna: {})' .format(tabela_erros.loc[erro_num]['mensagem'],linha_s0, coluna_s0))
			if a == '$':
				break
			if erro_num == 1:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'inicio'
				flag_a_antigo = 1
				#print('erro inicio')
			elif erro_num == 4:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'varinicio'
				flag_a_antigo = 1
			elif erro_num == 9:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'id'
				flag_a_antigo = 1
			elif erro_num == 10:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'id'
				flag_a_antigo = 1
			elif erro_num == 11:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'rcb'
				flag_a_antigo = 1
			elif erro_num == 17:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'ab_p'
				flag_a_antigo = 1
			elif erro_num == 18:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'id'
				flag_a_antigo = 1
			elif erro_num == 19:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'opr'
				flag_a_antigo = 1
			elif erro_num == 20:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'entao'
				flag_a_antigo = 1
			elif erro_num == 21:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'faca'
				flag_a_antigo = 1
			elif erro_num == 22:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'fc_p'
				flag_a_antigo = 1
			elif erro_num == 25:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'pt_v'
				flag_a_antigo = 1
			elif erro_num == 26:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'lit'
				flag_a_antigo = 1
			elif erro_num == 31:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'ab_p'
				flag_a_antigo = 1
			elif erro_num == 32:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'fc_p'
				flag_a_antigo = 1
			elif erro_num == 33:
				#file.ponteiro-= len(accept[2])
				a_antigo = a
				a = 'fc_p'
				flag_a_antigo = 1
			else:	
				#p_index = len(pilha.dados)-1
				#print(pilha.dados)
				#print(p_index)
				flag = 0
				#while p_index >= 0 and flag == 0:
				p_index = pilha.desempilha()
				while p_index != None and flag == 0:
					#print('p_index: {}'.format(p_index))
					for i in range (0,19):
						nao_terminal = tabela_follow.loc[i]['Variavel']
						
						goto = tabela_desvios.loc[ p_index][nao_terminal]
						if goto != ' ':
							#print('nao_terminal: {}\npilha.dados[p_index]: {}\n'.format(nao_terminal, pilha.dados[p_index]))
							#print('goto: {}' .format(goto))
							pilha.empilha(p_index)
							pilha.empilha(int(goto))
							#print(pilha.dados)
							flag = 1
							conj_follow = tabela_follow.loc[i]['FOLLOW']
							#if 'pt_v' in conj_follow:
							#print("Conjunto follow: {}".format(conj_follow))
							break
					p_index = pilha.desempilha()
					empilhar = p_index
				#tabela_simbolos.print_table()
				pilha.empilha(empilhar)
				accept = ['erro']
				#print('oi1')
				while(accept[0] == 'erro'):
					#print('oi2')
					try:
						accept = False, None, None, None

						if (file.ponteiro < file.eof):
							accept = lex.dfa.lexico(tabela_simbolos)
							#print('accept[0]: {}\nponteiro:{}\neof:{}'.format(accept[0], file.ponteiro,file.eof))
							#print('oi3')
							if accept[0] != 'erro':
								#print('oi4')
								linha_s = linha_s0
								coluna_s = coluna_s0
								a = accept[2]
								linha_s0 = file.linha
								coluna_s0 = file.coluna - len(accept[1])
								#print("accept[2]: {}".format(accept[2]))
								if accept[2] not in conj_follow:
									#print('Dentro de erro: accept[2] {}' .format(accept[2]))
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
				#print('a -- {}'.format(a))
				#print(pilha.dados)
				#break