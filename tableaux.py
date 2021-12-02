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
			self.formula = self.converter_formula(formula)
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

	@staticmethod
	def converter_formula(formula: str) -> Proposition:
		termos = " ><|&~()"
		dic_variaveis = formula.maketrans(termos," "*len(termos))	# retira 'termos' de formula e guarda convesoes em dicionario 
		variaveis = set(formula.translate(dic_variaveis).split())	# 'traduz' formula usando dicionario anterior, e retorna um set com variaveis
		for variavel in variaveis:
			exec(f"{variavel} = para_variavel('{variavel}')")	# associamos cada variavel ao seu respectivo nome com exec
		return eval(formula)	# retornamos a expressao convertida usando eval()

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

class Ramo():
	
	expansoes = []

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

	def __add__(self, marcada):
		return Ramo(self.marcadas+[marcada], marcas = self.marcas + [marcada.obtem_expansao()])

	def __str__(self):
		return f"{self.marcadas}"

	@staticmethod
	def aplicar_alfas(ramo):
		inf = 0
		sup = len(ramo.marcadas)
		while inf < sup:
			ramo = Ramo.aplicar_alfas_aux(ramo, inf, sup)
			inf = sup
			sup = len(ramo.marcadas) 
		return ramo

	@staticmethod
	def aplicar_alfas_aux(ramo, inf, sup):
		for i in range(inf,sup):
			if ramo.marcas[i] == 0:
				if ramo.marcadas[i].valor:
					if isinstance(ramo.marcadas[i].formula, And):
						Ramo.expansoes.append(("Alfa And",ramo.marcadas[i]))
						for elemento in ramo.marcadas[i].children:
							ramo = ramo + Marcada(True, elemento)
					if isinstance(ramo.marcadas[i].formula, Not):
						Ramo.expansoes.append(("Alfa Not",ramo.marcadas[i]))
						ramo = ramo + Marcada(False, ramo.marcadas[i].children[0])
				else:
					if isinstance(ramo.marcadas[i].formula, Or):
						Ramo.expansoes.append(("Alfa Or",ramo.marcadas[i]))
						for elemento in ramo.marcadas[i].children:
							ramo = ramo + Marcada(False, elemento)
					if isinstance(ramo.marcadas[i].formula, Implies):
						Ramo.expansoes.append(("Alfa Implies",ramo.marcadas[i]))
						ramo = ramo + Marcada(True, ramo.marcadas[i].children[0])
						ramo = ramo + Marcada(False, ramo.marcadas[i].children[1])
				
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
		Recebe de input um tableaux em formato de string e retorna uma lista de formulas marcadas
		"""
		marcadas = []
		
		if not "#" in formula:
			raise SyntaxError

		f1, f2 = formula.split('#')

		f1 = f1.split(",")
		f2 = f2.split(",")

		formulas_verdadeiro = []
		formulas_falso = []

		for f in f1:
			if f == "":
				continue
			formulas_verdadeiro.append(Marcada.converter_formula(f))

		for f in f2:
			if f == "":
				continue
			formulas_falso.append(Marcada.converter_formula(f))

		for formula in formulas_verdadeiro:
			marcadas.append(Marcada(True, formula))
		for formula in formulas_falso:
			marcadas.append(Marcada(False, formula))	

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
				Ramo.expansoes.append(("Beta Or",marcada))
				for elemento in marcada.children:
					retorno.append(Marcada(True, elemento))
			if isinstance(marcada.formula, Implies):
				Ramo.expansoes.append(("Beta Implies",marcada))
				retorno.append(Marcada(False, marcada.children[0]))
				retorno.append(Marcada(True, marcada.children[1]))
		else:
			if isinstance(marcada.formula, And):
				Ramo.expansoes.append(("Beta And",marcada))
				for elemento in marcada.children:
					retorno.append(Marcada(False, elemento))
			if isinstance(marcada.formula, Not):
				Ramo.expansoes.append(("Beta Not",marcada))	
				retorno.append(Marcada(True, marcada.children[0]))
		ramo.marcas[local] = -1
		return (retorno, ramo)
			

	@staticmethod
	def provar_validade(ramo):
		ramo = Ramo.aplicar_alfas(ramo)
		if ramo.verificar_se_fechado():
			return True
		operacao = Ramo.extrair_beta(ramo)
		if operacao == False:
			return ramo.obter_saturacoes()
		betas, ramo = operacao
		for beta in betas:
			retorno = Ramo.provar_validade(ramo + beta)
			if isinstance(retorno, list): return retorno

		return True

def para_variavel(variavel: str) -> Variable:
	return Variable(variavel)

def imprime_operacoes():
	for i in Ramo.expansoes:
		tipo, operacao = i[0].split(" ")
		print(f"Tipo de expansão: {tipo}		Operação: {operacao}")
		print(f"+ {i[1]}")
		print()

def main():
	print("[Tableau] Digite o sequente abaixo (Utilize # para consequência lógica):")
	entrada = input("+ ")
	formula = Ramo(entrada)
	resultado = Ramo.provar_validade(formula)
	if isinstance(resultado, list):
		print("[Tableau] Sequente inválido! Segue o contra-exemplo abaixo:")
		print(resultado)
		print()
		print("[Tableau] Sequencia de operacoes utilizada: ")
		imprime_operacoes()
	else:
		print("[Tableau] Sequente válido!")
		print()
		print("[Tableau] Sequencia de operacoes utilizada: ")
		imprime_operacoes()
		

	
if __name__=="__main__":
	main()

