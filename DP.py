import tracemalloc
import time
import random
from memory_profiler import memory_usage


def is_tautology(clause):
    for lit in clause:
        if -lit in clause:
            return True
    return False


def find_pure_literal(clauses):
    literal_polarities = {}
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in literal_polarities:
                literal_polarities[var] = {'pos': False, 'neg': False}
            if lit > 0:
                literal_polarities[var]['pos'] = True
            else:
                literal_polarities[var]['neg'] = True

    for var in literal_polarities:
        if literal_polarities[var]['pos'] and not literal_polarities[var]['neg']:
            return var
        elif literal_polarities[var]['neg'] and not literal_polarities[var]['pos']:
            return -var
    return None


def find_unit_clause(clauses):
    for clause in clauses:
        if len(clause) == 1:
            return next(iter(clause))
    return None


def unit_propagate(clauses, unit_lit):
    new_clauses = []
    for clause in clauses:
        if unit_lit in clause:
            continue
        if -unit_lit in clause:
            new_clause = set(clause)
            new_clause.remove(-unit_lit)
            if not new_clause:
                return [frozenset()]  # Empty clause
            new_clauses.append(frozenset(new_clause))
        else:
            new_clauses.append(clause)
    return new_clauses


def select_variable(clauses):
    variables = set()
    for clause in clauses:
        for lit in clause:
            variables.add(abs(lit))
    return next(iter(variables)) if variables else None


def eliminate_variable(clauses, var):
    pos_clauses = []
    neg_clauses = []
    for clause in clauses:
        if var in clause:
            pos_clauses.append(clause)
        if -var in clause:
            neg_clauses.append(clause)

    resolvents = []
    for p_clause in pos_clauses:
        for n_clause in neg_clauses:
            resolvent = set(p_clause)
            resolvent.discard(var)
            resolvent.update(n_clause)
            resolvent.discard(-var)
            resolvent = frozenset(resolvent)
            if not is_tautology(resolvent):
                resolvents.append(resolvent)

    remaining_clauses = [
        clause for clause in clauses
        if var not in clause and -var not in clause
    ]
    remaining_clauses.extend(resolvents)
    return remaining_clauses


def davis_putnam(clauses):
    while True:
        # Controlam daca nu avem vreo clauza vida
        if any(len(c) == 0 for c in clauses):
            return False

        # Controlăm dacă avem o mulțime vidă de clauze
        if not clauses:
            return True

        # aplicam literalul pur
        pure_lit = find_pure_literal(clauses)
        if pure_lit is not None:
            clauses = [c for c in clauses if pure_lit not in c]
            continue

        # Propagarea unitatii
        unit_lit = find_unit_clause(clauses)
        if unit_lit is not None:
            clauses = unit_propagate(clauses, unit_lit)
            continue
        # Stergem variabilele
        var = select_variable(clauses)
        if var is None:
            return True
        clauses = eliminate_variable(clauses, var)

def generate_large_fnc(numar_literali, numar_de_clauze, marimea_clauzelor=3):
    fnc = []
    for _ in range(numar_de_clauze):
        vars_in_clause = random.sample(range(1, numar_literali + 1), k=min(marimea_clauzelor, numar_literali))
        clause = [v if random.choice([True, False]) else -v for v in vars_in_clause]
        fnc.append(clause)
    return fnc
def main():
    num_vars = 1000
    clause_size = 2
    num_clauses = 4000

    clauses = generate_large_fnc(num_vars, num_clauses, clause_size)

    start_time = time.time()
    max_mem, result = memory_usage((davis_putnam, (clauses,)), interval=0.01, max_usage=True, retval=True)
    elapsed_time = time.time() - start_time

    print(f"\nResult: {'UNSAT' if not result else 'SAT'}")
    print(f"Numarul de clauze: {len(clauses)}")
    print(f"Timp: {elapsed_time:.4f} seconds")
    print(f"Utilizare memorie RAM: {max_mem:.2f} MB")
if __name__ == "__main__":
    main()