from code_base_EP1 import *

def cria_lista_unicos(lista):
	resultado = []
	for elemento in lista:
		if not elemento in resultado:
			resultado.append(elemento)
	return resultado

class Marcada():
	def __init__(self, valor: bool, formula): 
		self.valor = valor
		if isinstance(formula, str):
			self.formula = converter_formula(formula)
		else:
			self.formula = formula
		self.children = self.formula.children

	def __str__(self):
		return f"[T] {self.formula}" if self.valor else f"[F] {self.formula}"

	def __repr__(self):
		return f"[T] {self.formula}" if self.valor else f"[F] {self.formula}"

	def __invert__(self):
		return Marcada(not self.valor, self.formula)

	def __eq__(self, marcada):
		return self.valor == marcada.valor and self.formula == marcada.formula

<<<<<<< Updated upstream
=======
	@staticmethod
	def converter_formula(formula: str) -> Proposition:
		termos = " ><|&~()"
		dic_variaveis = formula.maketrans(termos," "*len(termos))	# retira 'termos' de formula e guarda convesoes em dicionario 
		variaveis = set(formula.translate(dic_variaveis).split())	# 'traduz' formula usando dicionario anterior, e retorna um set com variaveis
		for variavel in variaveis:
			exec(f"{variavel} = para_variavel('{variavel}')")	# associamos cada variavel ao seu respectivo nome com exec
		return eval(formula)	# retornamos a expressao convertida usando eval()
>>>>>>> Stashed changes

	def obtem_tamanho(self) -> int:
		return len(self.children) + 1

	def eh_saturada(self) -> bool:
		return len(self.children) == 0

	def obtem_expansao(self) -> bool:
		"""
		Avalia se expansao em objeto marcado eh alfa ou beta, retornando 0 para alfa e 1 para beta e -1 para quando a expressao n tem expansao(saturada). 
		"""
		if self.eh_saturada():
			return -1
		if self.valor:
			if isinstance(self.formula, And) or isinstance(self.formula, Not): return 0
			if isinstance(self.formula, Or) or isinstance(self.formula, Implies): return 1
		else:
			if isinstance(self.formula, And) or isinstance(self.formula, Not): return 1
			if isinstance(self.formula, Or) or isinstance(self.formula, Implies): return 0

<<<<<<< Updated upstream

def para_variavel(variavel: str) -> Variable:
	return Variable(variavel)

def converter_formula(formula: str) -> Proposition:
	"""
	Recebe de input uma formula em formato de string e a retorna em um objeto Proposition
	"""
	termos = " ><|&~()"
	dic_variaveis = formula.maketrans(termos," "*len(termos))	# retira 'termos' de formula e guarda convesoes em dicionario 
	variaveis = set(formula.translate(dic_variaveis).split())	# 'traduz' formula usando dicionario anterior, e retorna um set com variaveis
	for variavel in variaveis:
		exec(f"{variavel} = para_variavel('{variavel}')")	# associamos cada variavel ao seu respectivo nome com exec
	return eval(formula)	# retornamos a expressao convertida usando eval()

def converter_tableaux(formula: str) -> list:
	"""
	Recebe de input um tableaux em formato de sting e retorna uma lista de formulas marcadas
	"""
	marcadas = []
=======
class Ramo():
	def __init__(self, marcadas, marcas = None):
		if isinstance(marcadas, str):
			self.marcadas = self.converter_tableaux(marcadas)
		else:
			self.marcadas = marcadas
		self.marcas = marcas
		if self.marcas == None:
			self.marcas = []
			for m in self.marcadas:
				self.marcas.append(m.obtem_expansao())
		self.tamanho = sum([marcada.obtem_tamanho() for marcada in self.marcadas])

	def __add__(self, marcada):
		return Ramo(self.marcadas+[marcada], marcas = self.marcas + [marcada.obtem_expansao()])

	def __str__(self):
		return f"{self.marcadas}"

	@staticmethod
	def aplicar_alfas(ramo):
		for i,marcada in enumerate(ramo.marcadas): 
			if ramo.marcas[i] == 0:
				# print(len(ramo.marcas))
				if marcada.valor:
					if isinstance(marcada.formula, And):
						for elemento in marcada.children:
							ramo = ramo + Marcada(True, elemento)
					if isinstance(marcada.formula, Not):
						ramo = ramo + Marcada(False, marcada.children[0])
				else:
					if isinstance(marcada.formula, Or):
						for elemento in marcada.children:
							ramo = ramo + Marcada(False, elemento)
					if isinstance(marcada.formula, Implies):
						ramo = ramo + Marcada(True, marcada.children[0])
						ramo = ramo + Marcada(False, marcada.children[1])
				
				ramo.marcas[i] = -1
		return ramo
	
	def obter_saturacoes(self):
		resultado = []
		for marcada in self.marcadas:
			if marcada.eh_saturada():
				resultado.append(marcada)
		return cria_lista_unicos(resultado)
	
	def verificar_se_fechado(self):
		atomos = self.obter_saturacoes()
		for atomo in atomos:
			if ~atomo in atomos:
				return True
		return False
	
	@staticmethod
	def converter_tableaux(formula: str) -> list:
		"""
		Recebe de input um tableaux em formato de sting e retorna uma lista de formulas marcadas
		"""
		marcadas = []
>>>>>>> Stashed changes

		formulas = formula.split(",")
		temp = formulas.pop().split("#")
		
		for f in temp:
			formulas.append(f)
		formulas = [Marcada.converter_formula(f) for f in formulas]
		for i,f in enumerate(formulas):
			if (i == len(formulas) - 1):
				marcadas.append(Marcada(False, f))
				continue
			marcadas.append(Marcada(True, f))


<<<<<<< Updated upstream
	return marcadas
=======
		return marcadas

	@staticmethod
	def extrair_beta(ramo):
		try:
			local = ramo.marcas[::-1].index(1)
		except ValueError:
			return False

		local = len(ramo.marcas) - local - 1

		marcada = ramo.marcadas[local]
		retorno = []
		if marcada.valor:
			if isinstance(marcada.formula, Or):
				for elemento in marcada.children:
					retorno.append(Marcada(True, elemento))
			if isinstance(marcada.formula, Implies):
				retorno.append(Marcada(False, marcada.children[0]))
				retorno.append(Marcada(True, marcada.children[1]))
		else:
			if isinstance(marcada.formula, And):
				for elemento in marcada.children:
					retorno.append(Marcada(False, elemento))
			if isinstance(marcada.formula, Not):
				retorno.append(Marcada(True, marcada.children[0]))
		ramo.marcas[local] = -1
		return (retorno, ramo)
			

	@staticmethod
	def provar_validade(ramo):
		ramo = Ramo.aplicar_alfas(ramo)
		# print(ramo.marcadas)
		if ramo.verificar_se_fechado():
			return True
		# print(ramo.marcas)
		operacao = Ramo.extrair_beta(ramo)
		# print(operacao)
		if operacao == False:
			return ramo.obter_saturacoes()
		betas, ramo = operacao
		for beta in betas:
			retorno = Ramo.provar_validade(ramo + beta)
			if isinstance(retorno, list): return retorno

		return True

def para_variavel(variavel: str) -> Variable:
	return Variable(variavel)
>>>>>>> Stashed changes

def eh_ramo_fechado(ramo: list) -> bool:
	"""
	Verifica em ramo(lista de marcas) se o mesmo esta fechado.
	"""
	expressoes_saturadas = []
	for marcada in ramo:
		if marcada.eh_saturada():
			for saturada in expressoes_saturadas:
				if saturada == ~marcada:
					return True
			expressoes_saturadas.append(marcada)
	return False

def aplicar_beta(marcada: Marcada) -> tuple:
	"""
	Expande expressao marcada com expressao beta.
	"""	
	if marcada.valor:
		if isinstance(marcada.formula, Or):
			return (Marcada(True,marcada.children[0]), Marcada(True,marcada.children[1])) 
		if isinstance(marcada.formula, Implies):
			return (Marcada(False,marcada.children[0]), Marcada(True,marcada.children[1]))
	else:
		if isinstance(marcada.formula, And):
			return (Marcada(False,marcada.children[0]), Marcada(False,marcada.children[1])) 
		if isinstance(marcada.formula, Not):
			return (Marcada(True,marcada.children[0]))
	return -1

def main():
	# formula1 = converter_formula("(P >> ~(Q >> R) & (Q >> (P|~R)))")
	
	# marcada = Marcada(False, formula1)
	# if marcada.obtem_expansao():
	# 	print("ALFA!")
	# else:
	# 	print("BETA!")
	# print(marcada.children)

	# marcadas = converter_tableaux("P >> Q, Q >> R # P >> R")
	# valores = []
	# tamanho_final = 0
	# for m in marcadas:
	# 	valores.append("ALFA") if m.obtem_expansao() else valores.append("BETA")
	# 	tamanho_final += m.obtem_tamanho()
	# print(f"tamanho final: {tamanho_final}")
	# print(valores)
	# print(marcadas)

	# ramo_exemplo = [Marcada(True, "P >> Q"), Marcada(True, "Q >> R"), Marcada(False, "P >> R"), Marcada(True, "P"), Marcada(False, "R"), Marcada(False, "Q")]
	# print(ramo_exemplo)
	# print(f"Eh ramo fechado?: {eh_ramo_fechado(ramo_exemplo)}")
	# ramo_exemplo.append(Marcada(False, "P"))
	# print(ramo_exemplo)
	# print(f"Eh ramo fechado?: {eh_ramo_fechado(ramo_exemplo)}")
	
	# ramo_ex_2 = [Marcada(True,"A & (B&C)"), Marcada(False, "(D & E) >> B")]

	# aplicar_alfa_iter(ramo_ex_2)
	# print(eh_ramo_fechado(ramo_ex_2))
 
	formula = Ramo("~(P | Q) >> ~P & ~Q")
	print(Ramo.provar_validade(formula))


if __name__=="__main__":
	main()
