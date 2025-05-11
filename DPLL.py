import random
import time
from memory_profiler import memory_usage


def dpll(fnc, atribuire):
    # Aplică propagarea unității
    fnc, atribuire = propagarea_unitatii(fnc, atribuire)
    if fnc is None:
        return None
    # Aplică eliminarea literalelor puri
    fnc, atribuire = regula_literalului_pur(fnc, atribuire)
    if not fnc:
        return atribuire
    # Verifică dacă există clauză vidă (nesatisfiabil)
    if any(len(clause) == 0 for clause in fnc):
        return None
    # Verifică dacă toate variabilele au fost atribuite (satisfiabil)
    unassigned_vars = {abs(lit) for clause in fnc for lit in clause} - set(atribuire.keys())
    if not unassigned_vars:
        return atribuire
    # Alege o variabilă neatribuită
    var = next(iter(unassigned_vars))
    #SPLIT pentru True
    result = dpll(simplify(fnc, var, True), {**atribuire, var: True})
    if result is not None:
        return result
    # SPLIT pentru False
    result = dpll(simplify(fnc, var, False), {**atribuire, var: False})
    return result


def propagarea_unitatii(fnc, assignment):
    """
    Efectuează propagarea unității pentru a simplifica FNC-ul.
    Returnează: (fnc,assignment) sau (None, None) dacă se detectează un conflict.
    """
    changed = True
    while changed:
        changed = False
        unit_clauses = [c[0] for c in fnc if len(c) == 1]
        for literal in unit_clauses:
            var = abs(literal)
            value = literal > 0
            if var in assignment:
                if assignment[var] != value:
                    return None, None  # Conflict detectat
            else:
                assignment[var] = value
                fnc = simplify(fnc, var, value)
                changed = True
    return fnc, assignment


def simplify(fnc, var, value):
    """
    Simplifică CNF-ul pe baza unei atribuiri a unei variabile.
    Argumente:
        var: Variabila de atribuit (întreg pozitiv).
        value: Atribuire True/False.
    Returnează: Un nou CNF cu clauzele satisfăcute eliminate și literalii opuși eliminați.
    """
    new_fnc = []
    for clause in fnc:
        if (var if value else -var) in clause:
            continue
        new_clause = [lit for lit in clause if lit != (-var if value else var)]
        new_fnc.append(new_clause)
    return new_fnc


def regula_literalului_pur(fnc, assignment):
    """

    Returnează: (nou_cnf, noua_atribuire) sau (None, None) dacă se detectează un conflict
    """
    counts = {}
    for clause in fnc:
        for literal in clause:
            counts[literal] = counts.get(literal, 0) + 1
    literali_puri = {lit for lit in counts if -lit not in counts}

    new_assignment = assignment.copy()
    for lit in literali_puri:
        var = abs(lit)
        value = lit > 0
        if var in new_assignment:
            if new_assignment[var] != value:
                return None, None  # Conflict detectat
        else:
            new_assignment[var] = value
            fnc = simplify(fnc, var, value)
    return fnc, new_assignment


def generator_de_clauze(numar_literali, numar_de_clauze, marimea_clauzelor=3):
    """
    Generează o formulă FNC aleatoare.
    Returnează: Listă de clauze.
    """
    fnc = []
    for _ in range(numar_de_clauze):
        # Selectează aleatoriu variabile distincte
        vars_in_clause = random.sample(range(1, numar_literali + 1), k=min(marimea_clauzelor, numar_literali))
        # Atribuie aleatoriu semne (pozitiv sau negativ)
        clause = [v if random.choice([True, False]) else -v for v in vars_in_clause]
        fnc.append(clause)
    return fnc


def run_dpll_with_metrics(fnc, assignment):
    def dpll_wrapper():
        return dpll(fnc, assignment.copy())
    start_time = time.time()
    mem_usage = memory_usage(dpll_wrapper, interval=0.01, max_usage=True)
    solution = dpll_wrapper() #rezultatul
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Timp de rulare: {runtime:.4f} secunde")
    print(f"Consum de memorie: {mem_usage:.2f} MB")
    if solution:
        print("SAT")
    else:
        print("UNSAT")

    return solution


if __name__ == '__main__':
    fnc_random = generator_de_clauze(numar_literali=1000, numar_de_clauze=4000, marimea_clauzelor=2)
    assignment = {}
    solution = run_dpll_with_metrics(fnc_random, assignment)
