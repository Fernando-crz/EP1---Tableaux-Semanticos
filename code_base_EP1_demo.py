#import code_base as CB

from code_base_EP1 import *

# fórmulas
# todos os átomos que serão utilizados nas fórmulas precisam ser declarados
P,Q,R,S = vars('P', 'Q', 'R', 'S')


#declaracao da formula
formula1 = (P >> (Q >> R)| (Q >> (P|~R)))

print(formula1.children)
teste = "(P >> (Q >> R)| (Q >> (P|~R)))"

ok = cast_to_proposition(teste)

print(type(formula1))
print(str(formula1))
#gera a arvore de subformulas da formula
print("Árvore:")
print(formula1.to_tree())
print("\n")

print("Nós:")
#lista de nos da arvore de subformulas
nodes = get_nodes(formula1)
for i,node in enumerate(nodes):
  print(f"Node {i}: {node}")
  print(f"tipo: {type(node)}")

print("\n")
#para um no especifico, podemos realizar quaisquer operacoes com formulas
node1 = nodes[1]
print("Pra um nó específico: Nó 1")
print(node1)
print("Tabela verdade")
node1.print_truth_table()
print("Variáveis")
print(node1.variables())
print("Valorações")
print(truth_table_rows(node1.variables()))

# sequentes
#para os sequentes, devemos ter um conjunto de permissas (antecedentes) e uma conclusão (consequente)
#aqui seguem alguns exemplos de uso
#veja que os átomos para as fórmulas seguintes já foram declarados anteriormente

# valid argument forms
modus_ponens = ArgumentForm(
  P, P >> Q,    #premises
  conclusion = Q
)
print("\n")
print("Modus_Ponens")
print("Premissas")
print(modus_ponens.premises)
print("Conclusão")
print(modus_ponens.conclusion)
print("Tabela Verdade")
modus_ponens.print_truth_table()
print("É válido? - método Tabela Verdade") #validade calculada via tabela verdade
print(modus_ponens.is_valid_truth_table())
#
modus_tollens = ArgumentForm(
  P >> Q, ~Q,   #premises
  conclusion = ~P
)
#
disjunctive_syllogism = ArgumentForm(
  P | Q, ~P,    #premises
  conclusion = Q
)
#
hypothetical_syllogism = ArgumentForm(
  P >> Q, Q >> R,   #premises
  conclusion = R
)

# invalid argument forms
non_sequitur = ArgumentForm(
  P,        #premises
  conclusion = Q
)
print("\n")
print("non_sequitur")
print("Premissas")
print(non_sequitur.premises)
print("Conclusão")
print(non_sequitur.conclusion)
print("Tabela Verdade")
non_sequitur.print_truth_table()
print("É válido? - método Tabela Verdade") #validade calculada via tabela verdade
print(non_sequitur.is_valid_truth_table())
#
affirming_the_consequent = ArgumentForm(
  P >> Q, Q,    #premises
  conclusion = P
)
print("\n")
print("affirming_the_consequent")
print("Premissas")
print(affirming_the_consequent.premises)
print("Conclusão")
print(affirming_the_consequent.conclusion)
print("Tabela Verdade")
affirming_the_consequent.print_truth_table()
print("É válido? - método Tabela Verdade") #validade calculada via tabela verdade
print(affirming_the_consequent.is_valid_truth_table())
#
denying_the_antecedent = ArgumentForm(
  P >> Q, ~P,   #premises
  conclusion = ~Q
)
#
fallacy_of_the_excluded_middle = ArgumentForm(
  P | Q, P,   #premises
  conclusion = ~Q
)
#