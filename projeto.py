from code_base_EP1 import *

class Marcada():
	def __init__(self, valor: bool, formula: Proposition): 
		self.valor = valor
		self.formula = formula
		self.children = formula.children

	def __str__(self):
		return f"[T] {self.formula}" if self.valor else f"[F] {self.formula}"

	def eh_saturada(self):
		return len(self.children) == 0

	def escolhe_expansao(self):
		"""
		Avalia se expansao em objeto marcado eh alfa ou beta, retornando true para alfa e false para beta. 
		"""
		if self.valor:
			if isinstance(self.formula, And) or isinstance(self.formula, Not): return True
			if isinstance(self.formula, Or) or isinstance(self.formula, Implies): return False
		else:
			if isinstance(self.formula, And) or isinstance(self.formula, Not): return False
			if isinstance(self.formula, Or) or isinstance(self.formula, Implies): return True


def para_variavel(variavel: str) -> Variable:
	return Variable(variavel)

def converter_formula(formula: str) -> Proposition:
	termos = " ><|&~()"
	dic_variaveis = formula.maketrans(termos," "*len(termos))	# retira 'termos' de formula e guarda convesoes em dicionario 
	variaveis = set(formula.translate(dic_variaveis).split())	# 'traduz' formula usando dicionario anterior, e retorna um set com variaveis
	for variavel in variaveis:
		exec(f"{variavel} = para_variavel('{variavel}')")	# associamos cada variavel ao seu respectivo nome com exec
	return eval(formula)	# retornamos a expressao convertida usando eval()

def main():
	formula1 = converter_formula("(P >> ~(Q >> R) & (Q >> (P|~R)))")
	marcada = Marcada(False, formula1)
	if marcada.escolhe_expansao():
		print("ALFA!")
	else:
		print("BETA!")
	# nodes = get_nodes(formula1)
	# for node in nodes:
	# 	print(f"NODE: {node} , tamanho: {len(node.children)}")
	# 	print(f"TIPO: {type(node)}")
	# 	if isinstance(node, Not): print("EH NOT!!!!11!!")
	

if __name__=="__main__":
	main()
