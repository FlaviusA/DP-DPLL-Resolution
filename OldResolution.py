import random
import time
from memory_profiler import memory_usage


def generate_clauses(num_vars, clause_size, num_clauses):
    if clause_size > num_vars:
        raise ValueError("Marimea clauzei nu poate fi mai mare decat numarul de variabile")
    variables = list(range(1, num_vars + 1))
    clauses = []
    while len(clauses) < num_clauses:
        selected = random.sample(variables, clause_size)
        clause = []
        for var in selected:
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(-var)
        clause = frozenset(clause)
        if not is_tautology(clause):
            clauses.append(clause)
    return clauses


def is_tautology(clause):
    for lit in clause:
        if -lit in clause:
            return True
    return False


def resolve(c1, c2):
    resolvents = []
    complementary = []
    for l1 in c1:
        for l2 in c2:
            if l1 == -l2:
                complementary.append((l1, l2))
    for l1, l2 in complementary:
        res = (c1 | c2) - {l1, l2}
        resolvents.append(res)
    return resolvents


def resolution_algorithm(initial_clauses):
    S = set(initial_clauses)
    prev_added = set(initial_clauses)

    while True:
        new_clauses = set()
        for C in prev_added:
            for D in S:
                if C == D:
                    continue
                resolvents = resolve(C, D)
                for res in resolvents:
                    if len(res) == 0:
                        return False  # UNSAT
                    if is_tautology(res):
                        continue
                    if res not in S and res not in new_clauses:
                        new_clauses.add(res)
        if not new_clauses:
            return True  # SAT
        S.update(new_clauses)
        prev_added = new_clauses


def main():
    num_vars = 100
    clause_size = 2
    num_clauses = 200
    clauses = generate_clauses(num_vars, clause_size, num_clauses)

    start_time = time.time()
    max_mem, result = memory_usage(lambda: resolution_algorithm(clauses), interval=0.01, max_usage=True, retval=True)
    elapsed_time = time.time() - start_time

    print(f"\nRezultat: {'UNSAT' if not result else 'SAT'}")
    print(f"Timp: {elapsed_time:.4f} seconds")
    print(f"RAM: {max_mem:.2f} MB")


if __name__ == "__main__":
    main()