# -*- coding: utf-8 -*-
import string
from lexico.util import *
from erro.errno import Error
# Classe que define o dfa
class DFA():
		def __init__(self, statesNum, _arquivo, lines, eof):
			global TOKEN
			T = TOKEN
			self.statesNum = statesNum # Pode estar errado
			self.transitions = [{} for i in range(statesNum)]
			self.acceptStates = [False] * self.statesNum
			self.statesToken = [T.noToken] * self.statesNum

			self._arquivo = _arquivo
			self. lines = lines
			self. eof = eof

		def set_DFA(self, src_state, char, target_state):
			self.transitions[src_state][char] = target_state

		def set_acceptState(self, state, token):
			self.acceptStates[state] = True
			self.statesToken[state] = token

		def lexico(self):
			global linha 
			global coluna
			global erro
			global vetor_erros
			global tabela_simbolos
			global ponteiro
			state = 0
			token = self.statesToken[state]
			token_aceito = self.statesToken[state]
			lexema_aceito = ''
			ponteiro_aceito = ponteiro
			acumulated = ''
			aspas = 0
			colchetes = 0
			try:
				while (ponteiro < self.eof):
					
					self._arquivo.seek(ponteiro)
					c = self._arquivo.read(1)
					#print ("Caracter lido: " + c)
					ponteiro+=1
					coluna+=1
					if state == 0 and c == '"':
						aspas = 1
					if state == 0 and c == '{':
						aspas = 1	
					state = self.transitions[state][c]
					token = self.statesToken[state]
					ponteiro_aceito = ponteiro
					if state != 0:
						acumulated += c
					if c == '\n':
						linha += 1
						coluna = 0		
				acumulated = acumulated.replace('\n','\\n')
				acumulated = acumulated.replace('\t','\\t')			
				if token is 'id':
					teste1 = {'lexema':acumulated,'token':acumulated,'tipo':''}
					teste2 = {'lexema':acumulated,'token':token,'tipo':''}
					if teste1 in tabela_simbolos:
						#impressao_bonita('reservada', acumulated, acumulated)
						return self.acceptStates[state], acumulated, acumulated, ''
					elif teste2 in tabela_simbolos:
						#impressao_bonita('repetida', acumulated, token)
						return self.acceptStates[state], acumulated, token_def(self.statesToken[state]), ''
					else:
						preencher_tabela = {'lexema':acumulated,'token':token,'tipo':''}
						tabela_simbolos.append(preencher_tabela)
						#impressao_bonita('corpo', acumulated, token)
						return self.acceptStates[state], acumulated, token_def(self.statesToken[state]), ''
				elif token_def(token) is not None and token_def(token) is not ' ':
					#impressao_bonita('corpo', acumulated, token)
					return self.acceptStates[state], acumulated, token_def(self.statesToken[state]), ''
				else:
					if aspas == 1:
						acumulated_string = acumulated+': Nao fechou aspas'+ bcolors.GREEN + bcolors.BOLD +' linha: ' + bcolors.END + str(linha)+ bcolors.GREEN + bcolors.BOLD + ' coluna: '+ bcolors.END+str(coluna)
						dicionario_erro = {'acumulated': acumulated_string, 'token': token}
						vetor_erros.append(dicionario_erro)
						#impressao_bonita('erro', c+' linha: '+str(linha)+' coluna: '+str(coluna), token)
						erro+=1
						return 'erro', None, None, None
					elif colchetes == 1:
						acumulated_string = acumulated+':Nao fechou colchetes'+ bcolors.GREEN + bcolors.BOLD +' linha: ' + bcolors.END + str(linha)+ bcolors.GREEN + bcolors.BOLD + ' coluna: '+ bcolors.END+str(coluna)
						dicionario_erro = {'acumulated': acumulated_string, 'token': token}
						vetor_erros.append(dicionario_erro)
						#impressao_bonita('erro', c+' linha: '+str(linha)+' coluna: '+str(coluna), token)
						erro+=1
						return 'erro', None, None, None



				#return self.acceptStates[state], token_def(self.statesToken[state])

			except KeyError:
				#first, st = input_line.split(input_line[input_line.find(stop)], 1)
				#print("Cont: {}".format(cont))
				#print ("\tSplit: {}".format(st))
				acumulated = acumulated.replace('\n','\\n')
				acumulated = acumulated.replace('\t','\\t')
				if state != 0:
					if token is 'id':
						
						teste1 = {'lexema':acumulated,'token':acumulated,'tipo':''}
						teste2 = {'lexema':acumulated,'token':token,'tipo':''}
						if teste1 in tabela_simbolos:
							#impressao_bonita('reservada', acumulated, acumulated)
							ponteiro-=1
							coluna-=1
							return False, acumulated, acumulated, ''
						elif teste2 in tabela_simbolos:
							#impressao_bonita('repetida', acumulated, token)
							ponteiro-=1
							coluna-=1
							return False, acumulated, token_def(self.statesToken[state]), ''
						else:
							preencher_tabela = {'lexema':acumulated,'token':token,'tipo':''}
							tabela_simbolos.append(preencher_tabela)
							#impressao_bonita('corpo', acumulated, token)
							ponteiro-=1
							coluna-=1
							return False, acumulated, token_def(self.statesToken[state]), ''
					elif token_def(token) is not None and token_def(token) is not ' ':
						#impressao_bonita('corpo', acumulated, token)
						ponteiro-=1
						coluna-=1
						return False, acumulated, token_def(self.statesToken[state]), ''
					else:
						if aspas == 1:
							acumulated_string = acumulated+': Nao fechou aspas'+ bcolors.GREEN + bcolors.BOLD +' linha: ' + bcolors.END + str(linha)+ bcolors.GREEN + bcolors.BOLD + ' coluna: '+ bcolors.END+str(coluna)
							dicionario_erro = {'acumulated': acumulated_string, 'token': token}
							vetor_erros.append(dicionario_erro)
							#impressao_bonita('erro', c+' linha: '+str(linha)+' coluna: '+str(coluna), token)
							erro+=1
							return 'erro', None, None, None
						elif parenteses == 1:
							acumulated_string = acumulated+':Nao fechou parenteses'+ bcolors.GREEN + bcolors.BOLD +' linha: ' + bcolors.END + str(linha)+ bcolors.GREEN + bcolors.BOLD + ' coluna: '+ bcolors.END+str(coluna)
							dicionario_erro = {'acumulated': acumulated_string, 'token': token}
							vetor_erros.append(dicionario_erro)
							#impressao_bonita('erro', c+' linha: '+str(linha)+' coluna: '+str(coluna), token)
							erro+=1
							return 'erro', None, None, None
						elif colchetes == 1:
							acumulated_string = acumulated+':Nao fechou colchetes'+ bcolors.GREEN + bcolors.BOLD +' linha: ' + bcolors.END + str(linha)+ bcolors.GREEN + bcolors.BOLD + ' coluna: '+ bcolors.END+str(coluna)
							dicionario_erro = {'acumulated': acumulated_string, 'token': token}
							vetor_erros.append(dicionario_erro)
							#impressao_bonita('erro', c+' linha: '+str(linha)+' coluna: '+str(coluna), token)
							erro+=1
							return 'erro', None, None, None
				elif state == 0:
					acumulated_string = c+ bcolors.GREEN + bcolors.BOLD +' linha: ' + bcolors.END + str(linha)+ bcolors.GREEN + bcolors.BOLD + ' coluna: '+ bcolors.END+str(coluna)
					dicionario_erro = {'acumulated': acumulated_string, 'token': token}
					vetor_erros.append(dicionario_erro)
					#impressao_bonita('erro', c+' linha: '+str(linha)+' coluna: '+str(coluna), token)
					erro+=1
					return 'erro', None, None, None
				#st = str(ponteiro)
				#print(st)
				return 'erro', None, None, None


# Construção do automato para o analisador léxico
class LEX_DFA():

	def __init__(self, _arquivo, lines, eof):
		self.dfa = DFA(21, _arquivo, lines, eof)
		self.load_DFA()
		
	'''
		Constroi o DFA
	'''
	def load_DFA(self):
		global TOKEN
		T = TOKEN 
		#Ignora (comentario, pulo de linha e espaço)
		self.dfa.set_DFA(0, ' ', 0)
		self.dfa.set_DFA(0, '\n', 0)
		self.dfa.set_DFA(0, '\t', 0)

		# Num
		self.dfa.set_DFA(1,'.',2)
		self.dfa.set_DFA(1,'E',4)
		self.dfa.set_DFA(1,'e',4)
		self.dfa.set_DFA(3,'E',4)
		self.dfa.set_DFA(3,'e',4)
		self.dfa.set_DFA(4,'+',5)
		self.dfa.set_DFA(4,'-',5)
		for digit in range(10):
			self.dfa.set_DFA(0,str(digit),1)
			self.dfa.set_DFA(1,str(digit),1)
			self.dfa.set_DFA(2,str(digit),3)
			self.dfa.set_DFA(3,str(digit),3)
			self.dfa.set_DFA(4,str(digit),6)
			self.dfa.set_DFA(5,str(digit),6)
			self.dfa.set_DFA(6,str(digit),6)
		self.dfa.set_acceptState(1, T.num)
		self.dfa.set_acceptState(3, T.num)
		self.dfa.set_acceptState(6, T.num)

		#Ponto e vírgula
		self.dfa.set_DFA(0, ';', 7)
		self.dfa.set_acceptState(7, T.pt_v)

		# Literal
		self.dfa.set_DFA(0, '"', 8)
		for st1 in string.printable:
			self.dfa.set_DFA(8, st1, 8)
		self.dfa.set_DFA(8, '"', 9)
		self.dfa.set_acceptState(9, T.literal)

		#Fecha parênteses
		self.dfa.set_DFA(0, ')', 10)
		self.dfa.set_acceptState(10,T.fc_p)

		#Abre parênteses
		self.dfa.set_DFA(0, '(', 13)
		self.dfa.set_acceptState(13,T.ab_p)

		#Comentário
		self.dfa.set_DFA(0, '{', 11)
		for st in string.printable:
			self.dfa.set_DFA(11, st, 11)
		self.dfa.set_DFA(11,'}',12)
		self.dfa.set_acceptState(12,T.Comentario)

		#EOF (fim de arquivo)
		self.dfa.set_DFA(0, "eof", 14)
		self.dfa.set_acceptState(14, T.eof)

		#Operações relacionais / atribuição
		self.dfa.set_DFA(0, '>', 16)
		self.dfa.set_DFA(0, '<', 15)
		self.dfa.set_DFA(0, '=', 18)
		self.dfa.set_DFA(15, '>', 18)
		self.dfa.set_DFA(15, '=', 18)
		self.dfa.set_DFA(15, '-', 17)
		self.dfa.set_DFA(16, '=', 18)
		self.dfa.set_acceptState(16, T.opr)
		self.dfa.set_acceptState(15, T.opr)
		self.dfa.set_acceptState(18, T.opr)
		self.dfa.set_acceptState(17, T.rcb)

		#Operações aritméticas
		self.dfa.set_DFA(0, '+', 20)
		self.dfa.set_DFA(0, '-', 20)
		self.dfa.set_DFA(0, '*', 20)
		self.dfa.set_DFA(0, '/', 20)
		self.dfa.set_acceptState(20, T.opm)

		#Id
		normalString = string.ascii_lowercase + string.ascii_uppercase
		for st in normalString:
			self.dfa.set_DFA(0, st, 19)
			self.dfa.set_DFA(19, st, 19)
		for digit in range(10):
			self.dfa.set_DFA(19, str(digit), 19)

		self.dfa.set_DFA(19, '_', 19)
		self.dfa.set_acceptState(19, T.id)

def analisador_lexico(_arquivo, lines, eof):

	lex = LEX_DFA(_arquivo, lines, eof)
	
	try:
		accept = lex.dfa.lexico()
		if accept[0] != 'erro':
			print('\nlexema: {}\ntoken: {}\ntipo: {}\n'.format(accept[1],accept[2],accept[3]))
		while(accept[0] is not True):
			if (ponteiro < eof):
				#p = int(tok)
				accept = lex.dfa.lexico()
				if accept[0] != 'erro':
					print('\nlexema: {}\ntoken: {}\ntipo: {}\n'.format(accept[1],accept[2],accept[3]))
			else:
				break
	except TypeError:
		pass

	if (erro>0):
		err = Error(erro, vetor_erros)
		err.printLexErro()

	print(bcolors.BOLD +"|%-10s  %-10s %-10s TABELA DE SIMBOLOS %-10s  %-10s   %-10s |" % (' ', ' ', ' ', ' ',' ', ' ') + bcolors.END )
	for tab in tabela_simbolos:
		if tab['lexema'] is tab['token']:
			impressao_bonita('reservada', tab['lexema'], tab['token'])
		else:
			impressao_bonita('repetida', tab['lexema'], tab['token'])