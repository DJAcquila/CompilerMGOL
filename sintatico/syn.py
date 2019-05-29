#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import string
from common.utility.util import *
from common.erro.errno import Error
from common.symbtable.table import SymbTable
from common.file.fileHandler import FileHandler
from lexico.analisadorlexico import *

class Pilha(object): #pilha utilizada para guardar estados no algoritmo sintatico
	def __init__(self):
		self.dados = []

	def empilha(self, simbolo):
		self.dados.append(simbolo)

	def desempilha(self):
		if not self.vazia():
			return self.dados.pop(-1)

	def vazia(self):
		return len(self.dados) == 0

	def topo(self): #pega apenas o topo da pilha sem retira-lo dela
		indice = len(self.dados) - 1
		return self.dados[indice]

def Shift_Reduce(file, tabela_acoes, tabela_desvios, regras, tabela_erros, tabela_follow):
	lex = LEX_DFA(file) #instancia do lexico, que sera o unico utilizado para acessar o arquivo
	tabela_simbolos = SymbTable()
	accept = []
	accept =['erro']
	a = '$'
	linha_s0 = 0
	coluna_s0 = 0
	a_antigo = a
	flag_a_antigo = 3

	pilha = Pilha()
	pilha.empilha(0) #empilha 0 para comecar do estado inicial do automato LR 0
	flag_sintatico = 0

	while(accept[0] == 'erro' or accept[2] == 'Comentario'):#utilizado para ignorar/pular os erros lexicos
		try:
			accept = False, None, None, None
			if (file.ponteiro < file.eof): #enquanto o arquivo nao chegou ao fim
				accept = lex.dfa.lexico(tabela_simbolos) #parte em que ocorre a chamada do lexico para pegar o proximo token
				if accept[0] != 'erro':
					linha_s = linha_s0
					coluna_s = coluna_s0
					a = accept[2] #token em que nao ha erro, utilizado para seguir em frente com algoritmo sintatico
					linha_s0 = file.linha
					coluna_s0 = file.coluna - len(accept[1])
					
				else:
					print('erro lexico: {}'.format(accept[1])) #impressao dos erros lexicos
					flag_sintatico = 1

			else:
				a = '$'#caso nao haja mais tokens, indica eof
		except TypeError:
			a = '$'
			break

	while True:
		#utilizado para controle da adicao de tokens faltantes
		if flag_a_antigo == 1:
			flag_a_antigo = 0
			#print('flag 1')
		elif flag_a_antigo == 0:
			#print('flag2')
			a = a_antigo
			flag_a_antigo = 3
			
		s = int(pilha.topo())
		if 's' in tabela_acoes.loc[s][a]: #acao shift
			t = tabela_acoes.loc[s][a]
			print('acao shift {}\n' .format(t))
			t = t.split('s')
			t = int(t[1])
			pilha.empilha(int(t))
			if flag_a_antigo == 3:
				accept = ['erro']
				while(accept[0] == 'erro' or accept[2] == 'Comentario'):
					try:
						accept = False, None, None, None

						if (file.ponteiro < file.eof):
							accept = lex.dfa.lexico(tabela_simbolos)
							if accept[0] != 'erro':
								linha_s = linha_s0
								coluna_s = coluna_s0
								a = accept[2]
								linha_s0 = file.linha
								coluna_s0 = file.coluna - len(accept[1])
							else:
								print('Erro lexico: {}'.format(accept[1]))
								flag_sintatico = 1
						else:
							a = '$'

					except TypeError:
						a = '$'
						break
		elif 'r' in tabela_acoes.loc[s][a]: #acao reduce
			red = tabela_acoes.loc[s][a]
			print('acao reduce {}' .format(red))
			red = red.split('r')
			red = int(red[1])
			B_simbols = int(regras.loc[red]['B_number'])
			while (B_simbols > 0):
				pilha.desempilha()
				B_simbols-= 1

			t = pilha.topo()
			Ant = regras.loc[red]['Antecedente']

			pilha.empilha(int(tabela_desvios.loc[t][Ant]))
			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente']+'\n')

		elif 'acc' in tabela_acoes.loc[s][a]: #aceita o arquivo
			if flag_sintatico == 0:
				print('Analise sintatica realizada. Codigo correto.')
				tabela_simbolos.print_table()
			else:
				print('Analise sintatica realizada. Codigo incorreto.') #deveria ser aceito, mas como teve erro sintatico não aceita
			break
		else: #ocorre um erro sintatico
			flag_sintatico = 1 #utilizada para adicionar tokens faltantes
			erro_num = tabela_acoes.loc[s][a]
			erro_num = erro_num.split('e')
			erro_num = int(erro_num[1])
			
			#impressao dos erros de acordo com o tipo, acontece antes de recuperar do erro
			if erro_num == 8:
				string_erro = 'Erro sintático: \''+a+'\''+tabela_erros.loc[erro_num]['mensagem']+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')'
				print(string_erro)
			elif erro_num == 25 or erro_num == 6 or erro_num == 26:
				string_erro = 'Erro sintático: '+tabela_erros.loc[erro_num]['mensagem']+'\''+a+'\''+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END+str(linha_s0) + bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')'
				print(string_erro)
			else:
				string_erro = 'Erro sintático: '+tabela_erros.loc[erro_num]['mensagem']+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')'
				print(string_erro)
			if a == '$':
				break
				
			#erros tratados individualmente adicionando o que falta
			if erro_num == 1:
				a_antigo = a
				a = 'inicio'
				flag_a_antigo = 1
			elif erro_num == 4:
				a_antigo = a
				a = 'varinicio'
				flag_a_antigo = 1
			elif erro_num == 9:
				a_antigo = a
				a = 'id'
				flag_a_antigo = 1
			elif erro_num == 11:
				a_antigo = a
				a = 'rcb'
				flag_a_antigo = 1
			elif erro_num == 17:
				a_antigo = a
				a = 'ab_p'
				flag_a_antigo = 1
			elif erro_num == 19:
				a_antigo = a
				a = 'opr'
				flag_a_antigo = 1
			elif erro_num == 20:
				a_antigo = a
				a = 'entao'
				flag_a_antigo = 1
			elif erro_num == 21:
				a_antigo = a
				a = 'faca'
				flag_a_antigo = 1
			elif erro_num == 22:
				a_antigo = a
				a = 'fc_p'
				flag_a_antigo = 1
			elif erro_num == 25:
				a_antigo = a
				a = 'pt_v'
				flag_a_antigo = 1
			elif erro_num == 26:
				a_antigo = a
				a = 'lit'
				flag_a_antigo = 1
			elif erro_num == 31:
				a_antigo = a
				a = 'ab_p'
				flag_a_antigo = 1
			elif erro_num == 32:
				a_antigo = a
				a = 'fc_p'
				flag_a_antigo = 1
			elif erro_num == 33:
				a_antigo = a
				a = 'fc_p'
				flag_a_antigo = 1
			else:	#implementa o modo panico
				flag = 0
				p_index = pilha.desempilha()
				while p_index != None and flag == 0:
					for i in range (0,19):
						nao_terminal = tabela_follow.loc[i]['Variavel']
						
						goto = tabela_desvios.loc[ p_index][nao_terminal]
						if goto != ' ':
							pilha.empilha(p_index)
							pilha.empilha(int(goto))
							flag = 1
							conj_follow = tabela_follow.loc[i]['FOLLOW'] #seleciona o seguinte
							break
					p_index = pilha.desempilha()
					empilhar = p_index
				pilha.empilha(empilhar)
				accept = ['erro']
				while(accept[0] == 'erro' or accept[2] == 'Comentario'):
					try:
						accept = False, None, None, None

						if (file.ponteiro < file.eof):
							accept = lex.dfa.lexico(tabela_simbolos)
							if accept[0] != 'erro':
								linha_s = linha_s0
								coluna_s = coluna_s0
								a = accept[2]
								linha_s0 = file.linha
								coluna_s0 = file.coluna - len(accept[1])
								if accept[2] not in conj_follow:
									accept = ['erro']

							else:
								print('Erro lexico: {}'.format(accept[1]))
						else:
							a = '$'

					except TypeError:
						a = '$'
						break
