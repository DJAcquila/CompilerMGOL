import hashlib
import string
# Tokens
TOKEN = lambda x:x
TOKEN.num = hashlib.md5(b'num')
TOKEN.literal = hashlib.md5(b'literal')
TOKEN.id = hashlib.md5(b'id')
TOKEN.noToken = hashlib.md5(b'noToken')
TOKEN.eof = hashlib.md5(b'eof')
TOKEN.opr = hashlib.md5(b'opr')
TOKEN.rcb = hashlib.md5(b'rcb')
TOKEN.opm = hashlib.md5(b'opm')
TOKEN.ab_p = hashlib.md5(b'ab_p')
TOKEN.fc_p = hashlib.md5(b'fc_p')
TOKEN.pt_v = hashlib.md5(b'pt_v')
TOKEN.erro = hashlib.md5(b'erro')

class bcolors:
    BOLD = '\033[1m'
    END = '\033[0m'

'''		
Traduzir o token para string
'''
def token_def(token):
	global TOKEN

	TOK = TOKEN
	if token == TOK.num:
		return 'num'
	elif token == TOK.literal:
		return 'literal'
	elif token == TOK.id:
		return 'id'
	elif token == TOK.noToken: 
		return ' '
	elif token == TOK.eof:
		return 'eof'
	elif token == TOK.opr:
		return 'opr'
	elif token == TOK.rcb:
		return 'rcb'
	elif token == TOK.opm:
		return 'opm'
	elif token == TOK.ab_p:
		return 'ab_p'
	elif token == TOK.fc_p:
		return 'fc_p'
	elif token == TOK.pt_v:
		return 'pt_v'
	elif token == TOK.erro:
		return 'erro'

def impressao_bonita(id, acumulated = 0, token = ''):
	if id == 'titulo':
		print(bcolors.BOLD +"|%-10s LEXEMA %-11s| %-10s TOKEN %-10s |" % (' ', ' ', ' ', ' ') + bcolors.END )
	elif id == 'linha':
		print("+"+repeat_to_length('.', 29)+"+"+repeat_to_length('.', 29) + "+")
	else:
		print("|%-2s  %-25s| %-10s  %-10s %-5s|" % (' ', acumulated, ' ', token_def(token), ' '))


# Classe que define o dfa
class DFA():
		def __init__(self, statesNum = 22):
			global TOKEN
			T = TOKEN
			self.statesNum = statesNum # Pode estar errado
			self.transitions = [{} for i in range(statesNum)]
			self.acceptStates = [False] * self.statesNum
			self.statesToken = [T.noToken] * self.statesNum

		def set_DFA(self, src_state, char, target_state):
			self.transitions[src_state][char] = target_state

		def set_acceptState(self, state, token):
			self.acceptStates[state] = True
			self.statesToken[state] = token

		def accept(self, input_line):
			state = 0
			token = self.statesToken[state]
			stop = ''
			acumulated = ''
			cont = 0
			try:
				for c in input_line:
					
					#print ("Caracter lido: " + c)
					cont+=1
					state = self.transitions[state][c]
					
					token = self.statesToken[state]

					stop = c
					acumulated += c

				impressao_bonita('corpo', acumulated, token)

				return self.acceptStates[state], token_def(self.statesToken[state])

			except KeyError:

				impressao_bonita('corpo', acumulated, token)
				#first, st = input_line.split(input_line[input_line.find(stop)], 1)
				st = input_line[cont-1:]
				#print ("\tSplit: {}".format(st))

				return False, st

# Construção do automato para o analisador léxico
class LEX_DFA():

	def __init__(self):
		self.dfa = DFA(22)
		self.load_DFA()
		
	'''
		COnstroi o DFA
	'''
	def load_DFA(self):
		global TOKEN
		T = TOKEN 
		# num
		self.dfa.set_DFA(0, ' ', 0)
		self.dfa.set_DFA(0, '\n', 0)
		self.dfa.set_DFA(0, '\t', 0)
		self.dfa.set_DFA(1, '.', 2)
		for digit in range(10):
			self.dfa.set_DFA(0, str(digit), 1)
			self.dfa.set_DFA(2, str(digit), 3)
			self.dfa.set_DFA(5, str(digit), 3)
			self.dfa.set_DFA(4, str(digit), 3)
			self.dfa.set_DFA(3, str(digit), 3)
			self.dfa.set_DFA(1, str(digit), 1)

		self.dfa.set_DFA(1, 'E', 4)
		self.dfa.set_DFA(1, 'e', 4)
		self.dfa.set_DFA(4, '-', 5)
		self.dfa.set_DFA(4, '+', 5)
		self.dfa.set_DFA(3, 'E', 4)
		self.dfa.set_DFA(3, 'e', 4)
		
		self.dfa.set_acceptState(1, T.num)
		self.dfa.set_acceptState(3, T.num)

		# Literal -Dando errado
		self.dfa.set_DFA(0, '"', 6)
		for st in string.printable:
			self.dfa.set_DFA(6, st, 7) # Não é só o L
			self.dfa.set_DFA(7, st, 7)
		self.dfa.set_DFA(7, '"', 8)

		self.dfa.set_acceptState(8, T.literal)

		#Id
		normalString = string.ascii_lowercase + string.ascii_uppercase
		for st in normalString:
			self.dfa.set_DFA(0, st, 9)
			self.dfa.set_DFA(9, st, 9)
		for digit in range(10):
			self.dfa.set_DFA(9, str(digit), 9)

		self.dfa.set_DFA(9, '_', 9)
		self.dfa.set_acceptState(9, T.id)

		#comentario
		self.dfa.set_DFA(0, "{", 10)
		for st in string.printable:
			self.dfa.set_DFA(10, st, 11)
			self.dfa.set_DFA(11, st, 11)
		self.dfa.set_DFA(11, "}", 12)
		self.dfa.set_acceptState(12, T.noToken)		

		self.dfa.set_DFA(0, "eof", 13)
		self.dfa.set_acceptState(13, T.eof)

		self.dfa.set_DFA(0, '<', 14)
		self.dfa.set_DFA(14, '-', 15)
		self.dfa.set_acceptState(15, T.rcb)

		self.dfa.set_DFA(14, '>', 16)
		self.dfa.set_DFA(14, '=', 16)
		self.dfa.set_DFA(0, '=', 16)
		self.dfa.set_DFA(0, '>', 17)
		self.dfa.set_DFA(17, '=', 16)
		self.dfa.set_acceptState(14, T.opr)
		self.dfa.set_acceptState(16, T.opr)
		self.dfa.set_acceptState(17, T.opr)

		self.dfa.set_DFA(0, '+', 18)
		self.dfa.set_DFA(0, '-', 18)
		self.dfa.set_DFA(0, '*', 18)
		self.dfa.set_DFA(0, '/', 18)
		self.dfa.set_acceptState(18, T.opm)

		self.dfa.set_DFA(0, ')', 19)
		self.dfa.set_DFA(0, '(', 20)
		self.dfa.set_DFA(0, ';', 21)

		self.dfa.set_acceptState(19, T.fc_p)
		self.dfa.set_acceptState(20, T.ab_p)
		self.dfa.set_acceptState(21, T.pt_v)


def preset_print(accept, tok):

	if accept:
		token = tok
		if token != ' ':
			print ("Token: " + token)

	if not accept:
		print ("Erro")

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

if __name__ == "__main__":

	lex = LEX_DFA()

	_input = open('fonte.alg', 'r')
	
	contents = _input.read()
	contents = contents.replace('\n', ' ')
	
	impressao_bonita('linha')
	impressao_bonita('titulo')
	impressao_bonita('linha')
	#contents = input("Input a string ")
	#print ("\nEntrada: " +  _input)
	accept, tok = lex.dfa.accept(contents)
	while(accept == False):
		new_input = tok
		if new_input == ' ':
			break
		#print ("\nEntrada: " +  new_input)
		accept, tok = lex.dfa.accept(new_input)
	impressao_bonita('linha')
	#preset_print(accept, tok)