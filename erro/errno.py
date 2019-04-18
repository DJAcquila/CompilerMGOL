class bcolors:
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


class Error():
	def __init__(self, num, v_erros):
		self.num = num
		self.v_erros = v_erros
		
	def printLexErro(self):
		def repeat_to_length(string_to_expand, length):
			return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

		def impressao_bonita(id, acumulated = 0, token = ''):
			if id == 'linha':
				print("+"+repeat_to_length('.', 29)+"+"+repeat_to_length('.', 29) + "+"+repeat_to_length('.', 29) + "+")
			else:
				print("%-3s %-3s %-3s ERRO! %-5s Caracter: %-24s  %-43s" % (' ', bcolors.RED , bcolors.BOLD, bcolors.END, acumulated,' '))

		print("Foram encontrados "+ str(self.num)+ bcolors.RED + bcolors.BOLD + " erros" + bcolors.END + " na análise léxica!")
		impressao_bonita('linha')
		for err in self.v_erros:
			impressao_bonita('erro', err['acumulated'], err['token'])
		impressao_bonita('linha')

	#def printSintaxErro(self):