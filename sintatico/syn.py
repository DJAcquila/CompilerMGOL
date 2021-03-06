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
import os

#Sempre que roda o programa o arquivo rascunho.c é apagado
arq_obj = open('rascunho.c','w')
arq_obj.close()

arq_obj_final = open('programa.c', 'w')
arq_obj_final.close()

expressao_while = []

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
	qnt_tabs = 1

	var_temp = -1
	var_temp_tipo = []
	pilha = Pilha()
	pilha_semantico = Pilha()
	var_while = Pilha()
	variaveis = []
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
					if accept[2] == 'Comentario':
						pass
					else:
						if accept[2] == 'rcb':
							val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'='}
						elif accept[2] == 'opr':
							if accept[1] == '<>':
								val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'!='}
							elif accept[1] == '=':
								val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'=='}
							else:
								val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[1]}
						elif accept[2] == 'num':
							if '.' in accept[1]:
								val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'real'}
							else:
								val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'inteiro'}
						elif accept[2] == 'literal':
								val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'lit'}
						else:
							val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[1]}

						pilha_semantico.empilha(val_semantico)
						flag_a_novo = 1
				else:
					print('erro lexico: {}'.format(accept[1])) #impressao dos erros lexicos
					flag_sintatico = 1

			else:
				a[2] = '$'#caso nao haja mais tokens, indica eof
		except TypeError:
			a[2] = '$'
			break

	while True:
		#utilizado para controle da adicao de tokens faltantes
		if flag_a_antigo == 1:
			flag_a_antigo = 0
		elif flag_a_antigo == 0:
			a = a_antigo
			flag_a_antigo = 3

		s = int(pilha.topo())
		if 's' in tabela_acoes.loc[s][a[2]]: #acao shift
			t = tabela_acoes.loc[s][a[2]]
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
								a = accept
								a = list(a)
								linha_s0 = file.linha
								coluna_s0 = file.coluna - len(accept[1])
								if accept[2] == 'Comentario':
									pass
								else:
									if accept[2] == 'rcb':
										val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'='}
									elif accept[2] == 'opr':
										if accept[1] == '<>':
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'!='}
										elif accept[1] == '=':
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'=='}
										else:
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[1]}
									elif accept[2] == 'num':
										if '.' in accept[1]:
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'real'}
										else:
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'inteiro'}
									elif accept[2] == 'literal':
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'lit'}
									else:
										val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[1]}

									pilha_semantico.empilha(val_semantico)
									flag_a_novo = 1
							else:
								print('Erro lexico: {}'.format(accept[1]))
								flag_sintatico = 1
						else:
							a[2] = '$'

					except TypeError:
						a[2] = '$'
						break
		elif 'r' in tabela_acoes.loc[s][a[2]]: #acao reduce
			red = tabela_acoes.loc[s][a[2]]
			print('Sintático: {}ação reduce {} {}' .format(bcolors.GREEN,bcolors.END,red))
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
			############################SEMANTICO############################
			resultado = regras.loc[red]['Semantico']
			a_repetido = 0
			if resultado == '-': #casos em que nao ha regra semantica
				a_repetido = pilha_semantico.desempilha()
				while (B_simbols > 0):
					pilha_semantico.desempilha()
					B_simbols-= 1
				preenche = {'lexema':'', 'token':'', 'tipo':''}
				pilha_semantico.empilha(preenche)
				pilha_semantico.empilha(a_repetido)
			else: #casos em que ha regra semantica, especificados com if/else para determinar suas acoes
				num_semantico = int(resultado)#pega o numero da regra semantica para aplica-la
				if num_semantico == 5:
					arq_obj = open('rascunho.c', 'a+')
					arq_obj.write('\n\n\n')
					arq_obj.close()
					a_repetido = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
					print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
					print("[!] Inserir: Três espaços vazios\n")
				elif num_semantico == 6:
					a_repetido = pilha_semantico.desempilha()
					arq_obj = open('rascunho.c', 'a+')
					pilha_semantico.desempilha()
					tipo = pilha_semantico.desempilha()
					ident = pilha_semantico.desempilha()
					if ident['lexema'] in variaveis:
						flag_sintatico=1
						print('Erro semântico: Variável '+ident['lexema']+' já declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
					else:
						variaveis.append(ident['lexema'])
						tabela_simbolos.put_tipo(ident['lexema'],ident['token'],tipo['tipo'])
						val_semantico = {'lexema':'', 'token':'','tipo':''}
						if tipo['tipo'] == 'inteiro':
							tipo['tipo'] = 'int'
						elif tipo['tipo'] == 'lit':
							tipo['tipo'] = 'literal'
						elif tipo['tipo'] == 'real':
							tipo['tipo'] = 'double'
						arq_obj.write('\t'+tipo['tipo']+' '+ident['lexema']+';\n')
						arq_obj.close()
						print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
						print("[*] Imprimir( {}{} {};{} )\n".format(bcolors.BOLD, tipo['tipo'], ident['lexema'], bcolors.END))
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
				elif num_semantico == 7:
					a_repetido = pilha_semantico.desempilha()
					inteiro = pilha_semantico.desempilha()
					TIPO = {'lexema':'','token':'','tipo':inteiro['tipo']}
					pilha_semantico.empilha(TIPO)

				elif num_semantico == 8:
					a_repetido = pilha_semantico.desempilha()
					real = pilha_semantico.desempilha()
					TIPO = {'lexema':'','token':'','tipo':real['tipo']}
					pilha_semantico.empilha(TIPO)
				elif num_semantico == 9:
					a_repetido = pilha_semantico.desempilha()
					lit = pilha_semantico.desempilha()
					TIPO = {'lexema':'','token':'','tipo':lit['tipo']}
					pilha_semantico.empilha(TIPO)
				elif num_semantico == 11:
					a_repetido = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					identificador = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])
					print("Semântico: {}tabela de símbolos{}".format(bcolors.BLUE, bcolors.END))
					print("[!] Verificar: {}.tipo = {}\n".format(identificador['token'], tipo_teste['tipo']))
					if tipo_teste:
						count_tab = 0
						if tipo_teste['tipo'] == 'lit':
							arq_obj = open('rascunho.c', 'a+')
							while count_tab < qnt_tabs:
								arq_obj.write('\t')
								count_tab+=1
							arq_obj.write('scanf(\"%s\",'+tipo_teste['lexema']+');\n')
							print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
							print("[*] Imprimir( {}scanf(\"%s\",{});{} )\n".format(bcolors.BOLD, tipo_teste['lexema'], bcolors.END))
							arq_obj.close()
						elif tipo_teste['tipo'] == 'inteiro':
							arq_obj = open('rascunho.c', 'a+')
							while count_tab < qnt_tabs:
								arq_obj.write('\t')
								count_tab+=1
							arq_obj.write('scanf(\"%d\",&'+tipo_teste['lexema']+');\n')
							print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
							print("[*] Imprimir( {}scanf(\"%d\",{});{} )\n".format(bcolors.BOLD, tipo_teste['lexema'], bcolors.BOLD))
							arq_obj.close()
						elif tipo_teste['tipo'] == 'real':
							arq_obj = open('rascunho.c', 'a+')
							while count_tab < qnt_tabs:
								arq_obj.write('\t')
								count_tab+=1
							arq_obj.write('scanf(\"%lf\",&'+tipo_teste['lexema']+');\n')
							print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
							print("[*] Imprimir( {}scanf(\"%lf\",{});{} )\n".format(bcolors.BOLD, tipo_teste['lexema'], bcolors.END))
							arq_obj.close()
						else:
							flag_sintatico = 1
							print('Erro semântico: Variável '+ identificador['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')

					else:
						flag_sintatico = 1
						print('Erro semântico: Variável '+ identificador['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
				elif num_semantico == 12:
					a_repetido = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					argumento = pilha_semantico.desempilha()
					escreva = pilha_semantico.desempilha()
					arq_obj = open('rascunho.c', 'a+')
					count_tab = 0
					while count_tab < qnt_tabs:
						arq_obj.write('\t')
						count_tab+=1
					if '\"' in argumento['lexema']:
						arq_obj.write('printf('+argumento['lexema']+');\n')
						print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
						print("[*] Imprimir( {}printf({});{} )\n".format(bcolors.BOLD, argumento['lexema'], bcolors.END))
					else:
						tipo_teste = tabela_simbolos.get_symbol(argumento['lexema'],argumento['token'])
						if type(tipo_teste) is not bool:
							if tipo_teste['tipo'] == 'lit':
								arq_obj.write('printf(\"%s\",'+argumento['lexema']+');\n')
								print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
								print("[*] Imprimir( {}printf(\"%s\",{});{} )\n".format(bcolors.BOLD, argumento['lexema'], bcolors.END))
							elif tipo_teste['tipo'] == 'real':
								arq_obj.write('printf(\"%lf\",'+argumento['lexema']+');\n')
								print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
								print("[*] Imprimir( {}printf(\"%lf\",{});{} )\n".format(bcolors.BOLD, argumento['lexema'], bcolors.END))
							elif tipo_teste['tipo'] == 'inteiro':
								arq_obj.write('printf(\"%d\",'+argumento['lexema']+');\n')
								print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
								print("[*] Imprimir( {}printf(\"%lf\",{});{} )\n".format(bcolors.BOLD, argumento['lexema'], bcolors.END))
							else:
								flag_sintatico = 1
								print('Erro semântico: Variável '+ argumento['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
					arq_obj.close()
					val_semantico = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(val_semantico)
				elif num_semantico == 13:
					a_repetido = pilha_semantico.desempilha()
					literal = pilha_semantico.desempilha()
					argumento = {'lexema':literal['lexema'], 'token':literal['token'],'tipo':literal['tipo']}
					pilha_semantico.empilha(argumento)
				elif num_semantico == 14:
					a_repetido = pilha_semantico.desempilha()
					num = pilha_semantico.desempilha()
					argumento = {'lexema':num['lexema'], 'token':num['token'],'tipo':num['tipo']}
					pilha_semantico.empilha(argumento)
				elif num_semantico == 15:
					a_repetido = pilha_semantico.desempilha()
					identificador = pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])
					if type(tipo_teste) is not bool:
						if tipo_teste['tipo'] == 'lit' or tipo_teste['tipo'] == 'real' or tipo_teste['tipo'] == 'inteiro':
							argumento = {'lexema':tipo_teste['lexema'], 'token':tipo_teste['token'],'tipo':tipo_teste['tipo']}
							pilha_semantico.empilha(tipo_teste)
						else:
							flag_sintatico = 1
							print('Erro semântico: Variável '+ identificador['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
							tipo_erro = {'lexema':'', 'token':'','tipo':''}
							pilha_semantico.empilha(tipo_erro)
				elif num_semantico == 17:
					a_repetido = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					LD = pilha_semantico.desempilha()
					rcb = pilha_semantico.desempilha()
					identificador = pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])

					if type(tipo_teste) is not bool:
						print("Semântico: {}tabela de símbolos{}".format(bcolors.BLUE, bcolors.END))
						print("[!] Verificar: {} declarado ({}.tipo = {})\n".format(identificador['lexema'], identificador['token'], tipo_teste['tipo']))
						if tipo_teste['tipo'] == 'lit' or tipo_teste['tipo'] == 'real' or tipo_teste['tipo'] == 'inteiro':
							if LD['tipo'] == tipo_teste['tipo']:
								arq_obj = open('rascunho.c', 'a+')
								count_tab = 0
								while count_tab < qnt_tabs:
									arq_obj.write('\t')
									count_tab+=1
								arq_obj.write(identificador['lexema']+' '+rcb['tipo']+' '+LD['lexema']+';\n')
								print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
								print("[*] Imprimir( {}{} {} {};{} )\n".format(bcolors.BOLD, identificador['lexema'], rcb['tipo'], LD['lexema'], bcolors.END))
								LD = {'lexema':'', 'token':'','tipo':''}
								pilha_semantico.empilha(LD)
								arq_obj.close()
							elif LD['tipo'] == '':
								flag_sintatico = 1
								if LD['lexema'] == '':
									print('Erro semântico: Tentando atribuir expressao invalida. ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
								else:
									print('Erro semântico: Variável '+ LD['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
								LD = {'lexema':'', 'token':'','tipo':''}
								pilha_semantico.empilha(LD)
							elif tipo_teste['tipo'] == '':
								flag_sintatico = 1
								if tipo_teste['lexema']:
									print('Erro semântico: Tentando atribuir à variavel invalida. ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
								else:
									print('Erro semântico: Variável '+ tipo_teste['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
								LD = {'lexema':'', 'token':'','tipo':''}
								pilha_semantico.empilha(LD)
							else:
								flag_sintatico = 1
								print('Erro semântico: Tipos diferentes para atribuição. '+ LD['tipo']+' e '+tipo_teste['tipo']+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
								tipo_erro = {'lexema':'', 'token':'','tipo':''}
								pilha_semantico.empilha(tipo_erro)
						elif LD['tipo'] == '':
							flag_sintatico = 1
							if LD['lexema'] == '':
								print('Erro semântico: Tentando atribuir expressao invalida. ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
							else:
								print('Erro semântico: Variável '+ LD['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
							LD = {'lexema':'', 'token':'','tipo':''}
							pilha_semantico.empilha(LD)
						elif tipo_teste['tipo'] == '':
							flag_sintatico = 1
							if tipo_teste['lexema']:
								print('Erro semântico: Tentando atribuir à variável invalida. ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
							else:
								print('Erro semântico: Variável '+ tipo_teste['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
							LD = {'lexema':'', 'token':'','tipo':''}
							pilha_semantico.empilha(LD)
						else:
							print('Erro semântico: Variável '+ tipo_teste['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
							tipo_erro = {'lexema':'', 'token':'','tipo':''}
							pilha_semantico.empilha(tipo_erro)
				elif num_semantico == 18:
					a_repetido = pilha_semantico.desempilha()
					OPRD2 = pilha_semantico.desempilha()
					opm = pilha_semantico.desempilha()
					OPRD1 = pilha_semantico.desempilha()

					if OPRD1['tipo'] != 'lit' and ((OPRD2['tipo'] == OPRD1['tipo'])):
						var_temp+=1
						while_temp = {'expressao':'T'+str(var_temp),'operacao': OPRD1['lexema']+opm['tipo']+OPRD2['lexema']+';\n'}
						expressao_while.append(while_temp)
						LD = {'lexema':'T'+str(var_temp), 'token':'','tipo':OPRD2['tipo']}
						var_temp_tipo.append({'num': var_temp, 'tipo':OPRD2['tipo']})
						pilha_semantico.empilha(LD)
						arq_obj = open('rascunho.c', 'a+')
						count_tab = 0
						while count_tab < qnt_tabs:
							arq_obj.write('\t')
							count_tab+=1
						arq_obj.write('T'+str(var_temp)+'='+OPRD1['lexema']+opm['tipo']+OPRD2['lexema']+';\n')
						print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
						print("[*] Imprimir( {}T{} = {}{}{};{} )\n".format(bcolors.BOLD, var_temp, OPRD1['lexema'],opm['tipo'], OPRD2['lexema'], bcolors.END))
						arq_obj.close()
					elif OPRD1['tipo'] == 'lit' or OPRD2['tipo'] == 'lit':
						flag_sintatico = 1
						print('Erro semântico: Não é possível atribuicao de tipo lit ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						LD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
					elif OPRD2['tipo'] == '':
						flag_sintatico=1
						if OPRD2['lexema'] == '':
							print('Erro semântico: Tentando utilizar variavel invalida na expressao ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						else:
							print('Erro semântico: Variável '+ OPRD2['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						LD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
					elif OPRD1['tipo'] == '':
						flag_sintatico=1
						if OPRD1['lexema'] == '':
							print('Erro semântico: Tentando utilizar variavel invalida na expressao ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						else:
							print('Erro semântico: Variável '+ OPRD2['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						LD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
					else:
						flag_sintatico = 1
						print('Erro semântico: Tipos diferentes para atribuição. '+ OPRD1['tipo']+' e '+OPRD2['tipo']+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						LD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
				elif num_semantico == 19:
					a_repetido = pilha_semantico.desempilha()
					OPRD = pilha_semantico.desempilha()
					LD = {'lexema':OPRD['lexema'], 'token':OPRD['token'],'tipo':OPRD['tipo']}
					pilha_semantico.empilha(LD)
				elif num_semantico == 20:
					a_repetido = pilha_semantico.desempilha()
					identificador = pilha_semantico.desempilha()
					tipo_teste = tabela_simbolos.get_symbol(identificador['lexema'],identificador['token'])
					if type(tipo_teste) is not bool:
						if tipo_teste['tipo'] == 'lit' or tipo_teste['tipo'] == 'real' or tipo_teste['tipo'] == 'inteiro':
							OPRD = {'lexema':tipo_teste['lexema'], 'token':tipo_teste['token'],'tipo':tipo_teste['tipo']}
							pilha_semantico.empilha(OPRD)
						else:
							flag_sintatico = 1
							print('Erro semântico: Variável '+ identificador['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
							OPRD = {'lexema':'', 'token':'','tipo':''}
							pilha_semantico.empilha(OPRD)
				elif num_semantico == 21:
					a_repetido = pilha_semantico.desempilha()
					num = pilha_semantico.desempilha()
					OPRD = {'lexema':num['lexema'], 'token':num['token'],'tipo':num['tipo']}
					pilha_semantico.empilha(OPRD)
				elif num_semantico == 23:
					a_repetido = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					COND = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(COND)
					arq_obj = open('rascunho.c', 'a+')
					qnt_tabs-=1
					count_tab = 0
					while count_tab < qnt_tabs:
						arq_obj.write('\t')
						count_tab+=1
					arq_obj.write('}\n')
					print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
					print("[*] Imprimir( {}{}{} )\n".format(bcolors.BOLD, '}',bcolors.END))
					arq_obj.close()
				elif num_semantico == 24:
					a_repetido = pilha_semantico.desempilha()
					entao = pilha_semantico.desempilha()
					fechap = pilha_semantico.desempilha()
					expressao = pilha_semantico.desempilha()
					abrep = pilha_semantico.desempilha()
					se = pilha_semantico.desempilha()
					arq_obj = open('rascunho.c', 'a+')
					count_tab = 0
					while count_tab < qnt_tabs:
						arq_obj.write('\t')
						count_tab+=1
					arq_obj.write('if('+expressao['lexema']+'){\n')
					print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
					print("[*] Imprimir( {}if({}){}{} )\n".format(bcolors.BOLD, expressao['lexema'], '{',  bcolors.END))
					arq_obj.close()
					cabecalho = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(cabecalho)
					qnt_tabs+=1
				elif num_semantico == 25:
					a_repetido = pilha_semantico.desempilha()
					OPRD2 = pilha_semantico.desempilha()
					opr = pilha_semantico.desempilha()
					OPRD1 = pilha_semantico.desempilha()
					if OPRD1['tipo'] != 'lit' and (OPRD2['tipo'] == OPRD1['tipo']):
						var_temp+=1
						while_temp = {'expressao':'T'+str(var_temp),'operacao':OPRD1['lexema']+opr['tipo']+OPRD2['lexema']+';\n'}
						expressao_while.append(while_temp)
						EXP = {'lexema':'T'+str(var_temp), 'token':'','tipo':OPRD1['tipo']}
						var_temp_tipo.append({'num': var_temp, 'tipo':OPRD1['tipo']})
						pilha_semantico.empilha(EXP)
						arq_obj = open('rascunho.c', 'a+')
						count_tab = 0
						while count_tab < qnt_tabs:
							arq_obj.write('\t')
							count_tab+=1
						arq_obj.write('T'+str(var_temp)+'='+OPRD1['lexema']+opr['tipo']+OPRD2['lexema']+';\n')
						print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
						print("[*] Imprimir( {}T{} = {}{}{};{} )\n".format(bcolors.BOLD, var_temp, OPRD1['lexema'],opr['tipo'], OPRD2['lexema'], bcolors.END))
						arq_obj.close()
					elif OPRD1['tipo'] == 'lit' or OPRD2['tipo'] == 'lit':
						flag_sintatico = 1
						print('Erro semântico: Tipo lit não permitido em expressoes ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						EXP = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(EXP)
					elif OPRD2['tipo'] == '':
						flag_sintatico=1
						if OPRD2['lexema'] == '':
							print('Erro semântico: Tentando utilizar variavel invalida na expressao ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						else:
							print('Erro semântico: Variável '+ OPRD2['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						LD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
					elif OPRD1['tipo'] == '':
						flag_sintatico=1
						if OPRD2['lexema'] == '':
							print('Erro semântico: Tentando utilizar variavel invalida na expressao ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						else:
							print('Erro semântico: Variável '+ OPRD2['lexema']+' não declarada ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						LD = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(LD)
					else:
						flag_sintatico = 1
						print('Erro semântico: Tipos diferentes para atribuição. '+ OPRD1['tipo']+' e '+OPRD2['tipo']+' ('+ bcolors.GREEN + bcolors.BOLD +'linha: '+ bcolors.END +str(linha_s0)+ bcolors.GREEN + bcolors.BOLD+ ' coluna: '+bcolors.END+ str(coluna_s0)+')')
						EXP = {'lexema':'', 'token':'','tipo':''}
						pilha_semantico.empilha(EXP)
				elif num_semantico == 33:
					a_repetido = pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					pilha_semantico.desempilha()
					REP = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(REP)
					arq_obj = open('rascunho.c', 'a+')
					qnt_tabs-=1
					count_tab = 0
					var_temp_while = var_while.desempilha()
					for line in expressao_while:
						if line['expressao'] == var_temp_while:
							while count_tab < (qnt_tabs+1):
								arq_obj.write('\t')
								count_tab+=1
							arq_obj.write(line['expressao']+'='+line['operacao']);
							print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
							print("[*] Imprimir( {}{}={}{} )\n".format(bcolors.BOLD, line['expressao'],line['operacao'], bcolors.END))
					count_tab = 0
					while count_tab < qnt_tabs:
						arq_obj.write('\t')
						count_tab+=1
					arq_obj.write('}\n')
					print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
					print("[*] Imprimir( {}{}{} )\n".format(bcolors.BOLD, '}',bcolors.END))
					arq_obj.close()
				elif num_semantico == 34:
					a_repetido = pilha_semantico.desempilha()
					faca = pilha_semantico.desempilha()
					fechap = pilha_semantico.desempilha()
					expressao = pilha_semantico.desempilha()
					abrep = pilha_semantico.desempilha()
					enquanto = pilha_semantico.desempilha()
					arq_obj = open('rascunho.c', 'a+')
					count_tab = 0
					var_while.empilha('T'+str(var_temp))
					while count_tab < qnt_tabs:
						arq_obj.write('\t')
						count_tab+=1
					arq_obj.write('while('+expressao['lexema']+'){\n')
					print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
					print("[*] Imprimir( {}while({}){}{} )\n".format(bcolors.BOLD, expressao['lexema'], '{', bcolors.END))
					arq_obj.close()
					w = {'lexema':'', 'token':'','tipo':''}
					pilha_semantico.empilha(w)
					qnt_tabs+=1
				pilha_semantico.empilha(a_repetido)
				############################SEMANTICO############################
		elif 'acc' in tabela_acoes.loc[s][a[2]]: #aceita o arquivo
			if flag_sintatico == 0:
				print("Semântico: {}arquivo objeto{}".format(bcolors.BLUE, bcolors.END))
				print("[*] Arquivo objeto finalizado \n")
				print('Analise sintatica e semantica realizadas. Codigo correto.')
				tabela_simbolos.print_table()
				############################SEMANTICO############################
				arq_obj_final = open('programa.c', 'a+')
				arq_obj_final.write('#include<stdio.h>\ntypedef char literal[256];\nvoid main (void)\n{\n\t/*----Variaveis temporarias----*/\n')
				arq_obj.close()
				count_var = 0
				temp = {}
				while (count_var <= var_temp):
					for line in var_temp_tipo:
						if line['num'] == count_var:
							temp = line
					if temp['tipo'] == 'inteiro':
						arq_obj_final.write('\tint T'+str(count_var)+';\n')
					elif temp['tipo'] == 'real':
						arq_obj_final.write('\tdouble T'+str(count_var)+';\n')
					elif temp['tipo'] == 'lit':
						arq_obj_final.write('\tliteral T'+str(count_var)+';\n')
					count_var += 1
				arq_obj_final.write('\t/*------------------------------*/\n')
				arq_obj = open('rascunho.c', 'r')
				for line in arq_obj:
					arq_obj_final.write(line)
				arq_obj_final.write('}')
				arq_obj_final.close()
				arq_obj.close()
				os.remove("rascunho.c")
				############################SEMANTICO############################
			else:
				print('Analise sintatica e semantica realizadas. Codigo incorreto.') #deveria ser aceito, mas como teve erro sintatico/lexico não aceita
				os.remove("rascunho.c")
				os.remove('programa.c')
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
									if accept[2] == 'rcb':
										val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'='}
									elif accept[2] == 'opr':
										if accept[1] == '<>':
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'!='}
										elif accept[1] == '=':
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'=='}
										else:
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[1]}
									elif accept[2] == 'num':
										if '.' in accept[1]:
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'real'}
										else:
											val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':'inteiro'}
									else:
										val_semantico = {'lexema':accept[1],'token':accept[2],'tipo':accept[1]}

									pilha_semantico.empilha(val_semantico)
									flag_a_novo = 1
									#print('struct Semantico: {}'.format(val_semantico['lexema']))

							else:
								print('Erro lexico: {}'.format(accept[1]))
						else:
							a[2] = '$'

					except TypeError:
						a[2] = '$'
						break
