#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import string
from common.utility.util import *
from common.erro.errno import Error
from common.symbtable.table import SymbTable
from common.file.fileHandler import FileHandler
from lexico.analisadorlexico import *
import array

#Sempre que roda o programa o arquivo programa.c é apagado
arq_obj = open('programa.c','w')
arq_obj.close()

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
	a = []
	a.append('')
	a.append('')
	a.append('$')
	linha_s0 = 0
	coluna_s0 = 0
	a_antigo = a
	flag_a_antigo = 3
	flag_a_novo = 0

	var_temp = -1
	pilha = Pilha()
	pilha_semantico = Pilha()
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
					a = accept #token em que nao ha erro, utilizado para seguir em frente com algoritmo sintatico
					a = list(a)
					linha_s0 = file.linha
					coluna_s0 = file.coluna - len(accept[1])
					 #tem que ver sobre constante numerica, por causa do exponencial
					if accept[2] == 'Comentario':
						pass
					else:

						val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[3]}
						pilha_semantico.empilha(val_semantico)
						flag_a_novo = 1
						print('struct Semantico: {}'.format(val_semantico['lexema']))
				else:
					print('erro lexico: {}'.format(accept[1])) #impressao dos erros lexicos
					flag_sintatico = 1
					print('1@@@@@@@@@@@@@@@@@@ flag erro @@@@@@@@@@@@@@@@@@@@@@@@')

			else:
				a[2] = '$'#caso nao haja mais tokens, indica eof
		except TypeError:
			a[2] = '$'
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
		if 's' in tabela_acoes.loc[s][a[2]]: #acao shift
			t = tabela_acoes.loc[s][a[2]]
			print('acao shift {}\n' .format(t))
			t = t.split('s')
			t = int(t[1])
			pilha.empilha(int(t))
			if flag_a_antigo == 3:
				accept = ['erro']
				while(accept[0] == 'erro' or accept[2] == 'Comentario'):
					try:
						accept = False, None, None, None
						print(file.ponteiro)
						print(file.eof)
						if (file.ponteiro < file.eof):
							accept = lex.dfa.lexico(tabela_simbolos)
							print(str(accept[0]))
							print(file.ponteiro)
							print(file.eof)
							if accept[0] != 'erro':
								linha_s = linha_s0
								coluna_s = coluna_s0
								a = accept
								a = list(a)
								linha_s0 = file.linha
								coluna_s0 = file.coluna - len(accept[1])
								print(accept[1])
								#tem que ver sobre constante numerica, por causa do exponencial
								if accept[2] == 'Comentario':
									pass
								else:
									val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[3]}
									pilha_semantico.empilha(val_semantico)
									flag_a_novo = 1
									print('struct Semantico: {} {}'.format(val_semantico['lexema'],val_semantico['tipo']))
							else:
								print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
								print(accept[[1]])
								print('@@@@@@@@@@@@@@@@@@ flag erro @@@@@@@@@@@@@@@@@@@@@@@@')
								print('2Erro lexico: {}'.format(accept[1]))
								flag_sintatico = 1
						else:
							a[2] = '$'

					except TypeError:
						a[2] = '$'
						break
		elif 'r' in tabela_acoes.loc[s][a[2]]: #acao reduce
			red = tabela_acoes.loc[s][a[2]]
			print('acao reduce {}' .format(red))
			red = red.split('r')
			red = int(red[1])
			B_simbols = int(regras.loc[red]['B_number'])
			count = B_simbols
			while (count > 0):
				pilha.desempilha()
				count-= 1
			t = pilha.topo()
			Ant = regras.loc[red]['Antecedente']

			pilha.empilha(int(tabela_desvios.loc[t][Ant]))
			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente']+'\n')
						#SEMANTICO
			resultado = regras.loc[red]['Semantico']
			#print('pilha: {}'.format(pilha_semantico.dados))
			a_repetido = 0
			if resultado == '-':
				if flag_a_novo:
					a_repetido = pilha_semantico.desempilha()
					flag_a_novo=0
				while (B_simbols > 0):
					pilha_semantico.desempilha()
					B_simbols-= 1
				preenche = {'lexema':'', 'token':'', 'tipo':''}
				pilha_semantico.empilha(preenche)
			else:
				num_semantico = int(resultado)
				if num_semantico == 5:
					arq_obj = open('programa.c', 'a+')
					arq_obj.write('\n\n\n')
					arq_obj.close()
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
				elif num_semantico == 6:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					arq_obj = open('programa.c', 'a+')
					tipo = pilha_semantico.desempilha()
					ident = pilha_semantico.desempilha()
					tabela_simbolos.put_tipo(ident['lexema'],ident['token'],tipo['tipo'])
					print(tabela_simbolos.get_symbol(ident['lexema'],ident['token']))
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					arq_obj.write(tipo['tipo'])
					arq_obj.write(' ')
					arq_obj.write(ident['lexema'])
					arq_obj.write('\n')
					arq_obj.close()
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
				elif num_semantico == 7:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					inteiro = pilha_semantico.desempilha()
					print(inteiro['tipo'])
					TIPO = {'lexema':'','token':'','tipo':inteiro['tipo']}
					pilha_semantico.empilha(TIPO)
				elif num_semantico == 8:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					real = pilha_semantico.desempilha()
					TIPO = {'lexema':'','token':'','tipo':real['tipo']}
					pilha_semantico.empilha(TIPO)
				elif num_semantico == 9:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					print(pilha_semantico.topo())
					lit = pilha_semantico.desempilha()
					TIPO = {'lexema':'','token':'','tipo':lit['tipo']}
					pilha_semantico.empilha(TIPO)
				elif num_semantico == 11:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					pilha_semantico.desempilha()
					identificador = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])
					if tipo_teste:
						if tipo_teste['tipo'] == 'lit':
							arq_obj = open('programa.c', 'a+')
							arq_obj.write('scanf(\"%s\",')
							arq_obj.write(tipo_teste['lexema'])
							arq_obj.write(')')
							arq_obj.close()
						elif tipo_teste['tipo'] == 'inteiro':
							arq_obj = open('programa.c', 'a+')
							arq_obj.write('scanf(\"%d\",')
							arq_obj.write(tipo_teste['lexema'])
							arq_obj.write(')')
							arq_obj.close()
						elif tipo_teste['tipo'] == 'real':
							arq_obj = open('programa.c', 'a+')
							arq_obj.write('scanf(\"%lf\",')
							arq_obj.write(tipo_teste['lexema'])
							arq_obj.write(')')
							arq_obj.close()
						else:
							print('Erro semântico: Variável {} não declarada'.format(identificador['lexema']))
					else:
						print('Erro semântico: Variável {} não declarada'.format(identificador['lexema']))
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
				elif num_semantico == 12:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					pilha_semantico.desempilha()
					argumento = pilha_semantico.desempilha()
					escreva = pilha_semantico.desempilha()
					arq_obj = open('programa.c', 'a+')
					arq_obj.write('printf(\"')
					arq_obj.write(argumento['lexema'])
					arq_obj.write('\");\n')
					arq_obj.close()
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
				elif num_semantico == 13:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					literal = pilha_semantico.desempilha()
					argumento = {'lexema':literal['lexema'], 'token':literal['token'],'tipo':literal['tipo']}
					pilha_semantico.empilha(argumento)
				elif num_semantico == 14:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					num = pilha_semantico.desempilha()
					argumento = {'lexema':num['lexema'], 'token':num['token'],'tipo':num['tipo']}
					pilha_semantico.empilha(argumento)
				elif num_semantico == 15:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					identificador = pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])
					if tipo_teste['tipo'] == 'lit' or tipo_teste['tipo'] == 'real' or tipo_teste['tipo'] == 'inteiro':
						argumento = {'lexema':tipo_teste['lexema'], 'token':tipo_teste['token'],'tipo':tipo_teste['tipo']}
						pilha_semantico.empilha(tipo_teste)
					else:
						print('Erro semântico: Variável {} não declarada'.format(identificador['lexema']))
						tipo_erro = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(tipo_erro)
				elif num_semantico == 17:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					pilha_semantico.desempilha()
					LD = pilha_semantico.desempilha()
					rcb = pilha_semantico.desempilha()
					identificador = pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])
					if tipo_teste['tipo'] == 'lit' or tipo_teste['tipo'] == 'real' or tipo_teste['tipo'] == 'inteiro':
						if LD['tipo'] == tipo_teste['tipo']:
							arq_obj = open('programa.c', 'a+')
							arq_obj.write(identificador['lexema'])
							arq_obj.write(rcb['tipo'])
							arq_obj.write(LD['lexema'])
							arq_obj.write('\n')
							arq_obj.close()
						else:
							print('Erro semantico: Tipos diferentes para atribuição. {} {}'.format(LD['tipo'],tipo_teste['tipo']))
						tipo_erro = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(tipo_erro)
				elif num_semantico == 18:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					OPRD2 = pilha_semantico.desempilha()
					opm = pilha_semantico.desempilha()
					OPRD1 = pilha_semantico.desempilha()
					if OPRD1['tipo'] != 'lit' and (OPRD2['tipo'] == OPRD1['tipo']):
						var_temp+=1
						LD = {'lexema':'T'+var_temp, 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
						arq_obj = open('programa.c', 'a+')
						arq_obj.write('T')
						arq_obj.write(var_temp)
						arq_obj.write(OPRD1['lexema'])
						arq_obj.write(' ')
						arq_obj.write(opm['tipo'])
						arq_obj.write(' ')
						arq_obj.write(OPRD2['lexema'])
						arq_obj.write('\n')
						arq_obj.close()
					else:
						print ('Erro semantico: Operandos {} {} com tipos incompativeis.'.format(OPRD1['tipo'],OPRD2['tipo']))
						LD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
				elif num_semantico == 19:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					OPRD = pilha_semantico.desempilha()
					LD = {'lexema':OPRD['lexema'], 'token':OPRD['token'],'tipo':OPRD['tipo']}
					pilha_semantico.empilha(LD)
				elif num_semantico == 20:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					identificador = pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])
					if tipo_teste['tipo'] == 'lit' or tipo_teste['tipo'] == 'real' or tipo_teste['tipo'] == 'inteiro':
						OPRD = {'lexema':tipo_teste['lexema'], 'token':tipo_teste['token'],'tipo':tipo_teste['tipo']}
						pilha_semantico.empilha(OPRD)
					else:
						print('Erro semantico: Variavel {} nao declarada.'.format(identificador['lexema']))
						OPRD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(OPRD)
				elif num_semantico == 21:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					num = pilha_semantico.desempilha()
					OPRD = {'lexema':num['lexema'], 'token':num['token'],'tipo':num['tipo']}
					pilha_semantico.empilha(OPRD)
				elif num_semantico == 23:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					COND = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(COND)
					arq_obj = open('programa.c', 'a+')
					arq_obj.write('}')
					arq_obj.write('\n')
					arq_obj.close()
				elif num_semantico == 24:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					entao = pilha_semantico.desempilha()
					fechap = pilha_semantico.desempilha()
					expressao = pilha_semantico.desempilha()
					abrep = pilha_semantico.desempilha()
					se = pilha_semantico.desempilha()
					arq_obj = open('programa.c', 'a+')
					arq_obj.write('if(')
					arq_obj.write(expressao['lexema'])
					arq_obj.write('){')
					arq_obj.write('\n')
					arq_obj.close()
					cabecalho = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(cabecalho)
				elif num_semantico == 25:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					OPRD2 = pilha_semantico.desempilha()
					opr = pilha_semantico.desempilha()
					OPRD1 = pilha_semantico.desempilha()
					if OPRD1['tipo'] != 'lit' and (OPRD2['tipo'] == OPRD1['tipo']):
						var_temp+=1
						EXP = {'lexema':'T'+var_temp, 'token':'','tipo':''}
						pilha_semantico.empilha(EXP)
						arq_obj = open('programa.c', 'a+')
						arq_obj.write('T')
						arq_obj.write(var_temp)
						arq_obj.write(OPRD1['lexema'])
						arq_obj.write(' ')
						arq_obj.write(opm['tipo'])
						arq_obj.write(' ')
						arq_obj.write(OPRD2['lexema'])
						arq_obj.write('\n')
						arq_obj.close()
					else:
						print ('Erro semantico: Operandos {} {} com tipos incompativeis. linha {} coluna {}'.format(OPRD1['tipo'],OPRD2['tipo'],linha_s0,coluna_s0))
						print('pilha: {}'.format(pilha_semantico.dados))
						EXP = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(EXP)
				elif num_semantico == 33:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					REP = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(REP)
					arq_obj = open('programa.c', 'a+')
					arq_obj.write('}')
					arq_obj.write('\n')
					arq_obj.close()
				elif num_semantico == 34:
					if flag_a_novo:
						a_repetido = pilha_semantico.desempilha()
						flag_a_novo=0
					faca = pilha_semantico.desempilha()
					fechap = pilha_semantico.desempilha()
					expressao = pilha_semantico.desempilha()
					abrep = pilha_semantico.desempilha()
					enquanto = pilha_semantico.desempilha()
					arq_obj = open('programa.c', 'a+')
					arq_obj.write('while(')
					arq_obj.write(expressao['lexema'])
					arq_obj.write('){')
					arq_obj.write('\n')
					arq_obj.close()
					w = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(w)
						#SEMANICO
				print(pilha_semantico.topo())
				if a_repetido != 0:
					pilha_semantico.empilha(a_repetido)
		elif 'acc' in tabela_acoes.loc[s][a[2]]: #aceita o arquivo
			if flag_sintatico == 0:
				print('Analise sintatica realizada. Codigo correto.')
				tabela_simbolos.print_table()
			else:
				print('Analise sintatica realizada. Codigo incorreto.') #deveria ser aceito, mas como teve erro sintatico não aceita
			break
		else: #ocorre um erro sintatico
			flag_sintatico = 1 #utilizada para adicionar tokens faltantes
			erro_num = tabela_acoes.loc[s][a[2]]
			erro_num = erro_num.split('e')
			erro_num = int(erro_num[1])

			#impressao dos erros de acordo com o tipo, acontece antes de recuperar do erro
			if erro_num == 8:
				string_erro = 'Erro sintático: \''+a[2]+'\''+tabela_erros.loc[erro_num]['mensagem']+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')'
				print(string_erro)
			elif erro_num == 25 or erro_num == 6 or erro_num == 26:
				string_erro = 'Erro sintático: '+tabela_erros.loc[erro_num]['mensagem']+'\''+a[2]+'\''+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END+str(linha_s0) + bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')'
				print(string_erro)
			else:
				string_erro = 'Erro sintático: '+tabela_erros.loc[erro_num]['mensagem']+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')'
				print(string_erro)
			if a[2] == '$':
				break

			#erros tratados individualmente adicionando o que falta
			if erro_num == 1:
				a_antigo = a
				a[2] = 'inicio'
				flag_a_antigo = 1
			elif erro_num == 4:
				a_antigo = a
				a[2] = 'varinicio'
				flag_a_antigo = 1
			elif erro_num == 9:
				a_antigo = a
				a[2] = 'id'
				flag_a_antigo = 1
			elif erro_num == 11:
				a_antigo = a
				a[2] = 'rcb'
				flag_a_antigo = 1
			elif erro_num == 17:
				a_antigo = a
				a[2] = 'ab_p'
				flag_a_antigo = 1
			elif erro_num == 19:
				a_antigo = a
				a[2] = 'opr'
				flag_a_antigo = 1
			elif erro_num == 20:
				a_antigo = a
				a[2] = 'entao'
				flag_a_antigo = 1
			elif erro_num == 21:
				a_antigo = a
				a[2] = 'faca'
				flag_a_antigo = 1
			elif erro_num == 22:
				a_antigo = a
				a[2] = 'fc_p'
				flag_a_antigo = 1
			elif erro_num == 25:
				a_antigo = a
				a[2] = 'pt_v'
				flag_a_antigo = 1
			elif erro_num == 26:
				a_antigo = a
				a[2] = 'lit'
				flag_a_antigo = 1
			elif erro_num == 31:
				a_antigo = a
				a[2] = 'ab_p'
				flag_a_antigo = 1
			elif erro_num == 32:
				a_antigo = a
				a[2] = 'fc_p'
				flag_a_antigo = 1
			elif erro_num == 33:
				a_antigo = a
				a[2] = 'fc_p'
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
								a = accept
								a = list(a)
								flag_a_novo = 1
								linha_s0 = file.linha
								coluna_s0 = file.coluna - len(accept[1])
								if accept[2] not in conj_follow:
									accept = ['erro']
								else:
									if accept[2] == 'Comentario':
										pass
									else:
										val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[3]}
										pilha_semantico.empilha(val_semantico)
										flag_a_novo = 1
										print('struct Semantico: {}'.format(val_semantico['lexema']))

							else:
								print('Erro lexico: {}'.format(accept[1]))
						else:
							a[2] = '$'

					except TypeError:
						a[2] = '$'
						break
