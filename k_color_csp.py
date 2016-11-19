
from cspbase import *
import itertools
import math
import sys
from cspbase import *
from propagators import *
import itertools
import orderings as stu_orderings

# V is a list of vertices
# E is a list of tuples (v1, v2) which represent edges from v1 to v2
# k ia a number of colouring
def kColoring(V, E, k):
    integrityCheck(V, E)
    k_color_csp = CSP("kColoring")
    # This is the colours, we use integer to label a colour
    domain = [i for i in range(k)]
    # A list of 2-tuples that will be used for add_satisfying tuples
    sat_tuples = generateSatisfyingTuples(domain)
    # Each vertex in V is a variable
    for v in V:
        new_var = Variable("Vertex "+v, domain)
        k_color_csp.add_var(new_var)

    # Now create constraints
    # For each edge = (v1, v2), the colour of v1 and v2 must be different
    for e in E:
        v1 = findVariable(e[0], k_color_csp)
        v2 = findVariable(e[1], k_color_csp)
        new_constraint = Constraint("Constraint "+ e[0] + " " + e[1], [v1, v2])
        new_constraint.add_satisfying_tuples(sat_tuples)
        k_color_csp.add_constraint(new_constraint)

    return k_color_csp, k_color_csp.get_all_vars()

# ============Helper function =================

# Given a name of a vertex, and a csp
# Return a variable object that has a name of name
def findVariable(name, csp):
    name = "Vertex "+ name
    for var in csp.get_all_vars():
        if var.name == name:
            return var
    raise Exception('Cannot find a variable with name = ' + name)

# Given a domain
# Generate a list of 2-tuples that represent all possible colour combination between 2 vertices
# No tuple t where t[0] = t[1]
# eg. domain = [0, 1, 2] -> output = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)]
def generateSatisfyingTuples(domain):
    iter_result = itertools.permutations(domain, 2)

    result = [t for t in iter_result]

    return result

# Check if V and E are alright
def integrityCheck(V, E):
    # Check if all v in V are unique
    if len(V) != len(set(V)):
        print("There are duplicates in V please go check")
        sys.exit(1)
    # Check if all e in E are unique
    if len(E) != len(set(E)):
        print("There are duplicates in E please go check")
        sys.exit(1)

    # Check if both e1 and e2 are in V for all e = (v1, v2)
    for e in E:
        if (e[0] not in V) or (e[1] not in V):
            print("The edge " + str(e) + " is not valid")
            sys.exit(1)            


def main():
    # Let's try a simple 3-colouring
    print("================Test 1 =====================")
    V = ['A', 'B', 'C', 'D', 'E', 'F']
    E = [('A', 'B'), ('A', 'C'), ('B', 'F'), ('B', 'C'), ('C', 'D'), ('C', 'E'), ('C', 'F'), ('E', 'F')]
    k = 3
    csp, var_array = kColoring(V, E, k)
    solver = BT(csp)
    solver.bt_search(prop_BT, stu_orderings.ord_dh, stu_orderings.val_arbitrary)
    # Let's try the example from the CSP lecture slide 60
    print("=================Test 2=====================")
    V = ["Western Australia", "Northern Territory", "South Australia", "Queensland", "New South Wales", "Victoria", "Tasmania"]
    E = [("Western Australia", "Northern Territory"), ("Western Australia", "South Australia"), ("Northern Territory", "South Australia"), ("Northern Territory", "Queensland"), ("South Australia", "Queensland"), ("South Australia", "New South Wales"), ("South Australia", "Victoria"), ("Victoria", "New South Wales")]
    k = 3
    csp, var_array = kColoring(V, E, k)
    solver = BT(csp)
    solver.bt_search(prop_BT, stu_orderings.ord_dh, stu_orderings.val_arbitrary)


if __name__=="__main__":
    main()