from code_base_EP1 import *

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

	formulas = formula.split(",")
	temp = formulas.pop().split("#")
	
	for f in temp:
		formulas.append(f)
	formulas = [converter_formula(f) for f in formulas]
	for i,f in enumerate(formulas):
		if (i == len(formulas) - 1):
			marcadas.append(Marcada(False, f))
			continue
		marcadas.append(Marcada(True, f))


	return marcadas

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
			
def aplicar_alfa_ramo(ramo: list, lo: int, hi: int):
	"""
	Expande todas expressoes alfa em ramo, adicionando elementos encontrados ao ramo
	"""
	ramo_utilizado = ramo[lo:hi]

	for marcada in ramo_utilizado:

		if marcada.obtem_expansao() == 0:
			if marcada.valor:
				if isinstance(marcada.formula, And):
					for children in marcada.children:
						ramo.append(Marcada(True,children))
				if isinstance(marcada.formula, Not):
					ramo.append(Marcada(False,marcada.children[0]))
			else:
				if isinstance(marcada.formula, Or):
					for children in marcada.children:
						ramo.append(Marcada(False,children))
				if isinstance(marcada.formula, Implies):
					ramo.append(Marcada(True,marcada.children[0]))
					ramo.append(Marcada(False,marcada.children[1]))

def aplicar_alfa_iter(ramo: list):
	n = 0
	new_n = len(ramo)
	while (new_n != n):
		aplicar_alfa_ramo(ramo, n, new_n)
		n = len(ramo)
		aplicar_alfa_ramo(ramo, new_n, n)
		new_n = len(ramo)

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

def cria_marcacao_beta(ramo: list) -> list:
	betas = []
	for marcada in ramo:
		if marcada.eh_saturada():
			betas.append(False)
			continue
		betas.append(not marcada.obtem_expansao())
	return betas

def provar_validade(ramo: list) -> bool:
	pilha = []
	while True:
		aplicar_alfa_ramo(ramo)
		betas = cria_marcacao_beta(ramo)
		if eh_ramo_fechado(ramo):
			print("Valido!")
			return True
	return False


def main():
	formula1 = converter_formula("(P >> ~(Q >> R) & (Q >> (P|~R)))")
	
	marcada = Marcada(False, formula1)
	if marcada.obtem_expansao():
		print("ALFA!")
	else:
		print("BETA!")
	print(marcada.children)

	marcadas = converter_tableaux("P >> Q, Q >> R # P >> R")
	valores = []
	tamanho_final = 0
	for m in marcadas:
		valores.append("ALFA") if m.obtem_expansao() else valores.append("BETA")
		tamanho_final += m.obtem_tamanho()
	print(f"tamanho final: {tamanho_final}")
	print(valores)
	print(marcadas)

	ramo_exemplo = [Marcada(True, "P >> Q"), Marcada(True, "Q >> R"), Marcada(False, "P >> R"), Marcada(True, "P"), Marcada(False, "R"), Marcada(False, "Q")]
	print(ramo_exemplo)
	print(f"Eh ramo fechado?: {eh_ramo_fechado(ramo_exemplo)}")
	ramo_exemplo.append(Marcada(False, "P"))
	print(ramo_exemplo)
	print(f"Eh ramo fechado?: {eh_ramo_fechado(ramo_exemplo)}")
	
	ramo_ex_2 = [Marcada(True,"A & (B&C)"), Marcada(False, "(D & E) >> B")]

	aplicar_alfa_iter(ramo_ex_2)
	print(eh_ramo_fechado(ramo_ex_2))


if __name__=="__main__":
	main()
