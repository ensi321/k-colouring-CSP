#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import math

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]

    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values.

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_sequential(csp):
    return csp.get_all_unasgn_vars()[0]

def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.  var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var


def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.
    MRV returns the variable with the most constrained current domain
    (i.e., the variable with the fewest legal values).
    '''
#IMPLEMENT
    usasgn_vars = csp.get_all_unasgn_vars()
    min_remaining_value = math.inf
    result = usasgn_vars[0]

    for v in usasgn_vars:
        if v.cur_domain_size() < min_remaining_value:
            result = v
            min_remaining_value = v.cur_domain_size()


    return result


def ord_dh(csp):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node,
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''
#IMPLEMENT
    usasgn_vars = csp.get_all_unasgn_vars()
    highest_degree = -1
    result = usasgn_vars[0]
    for v in usasgn_vars:
        degree = 0
        for con in csp.get_cons_with_var(v):
            degree += con.get_n_unasgn()
        if degree > highest_degree:
            highest_degree = degree
            result = v


    return result



def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index,
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.)
    The best value, according to LCV, is the one that rules out the fewest domain values in other
    variables that share at least one constraint with var.
    '''
#IMPLEMENT
    # Dict of all possible value v of var, v:int, int is the number of domain values that rules out if pick v
    d = dict((v, 0) for v in var.cur_domain())
    cons = csp.get_cons_with_var(var)

    for value in d.keys():
        for con in cons:
            if con.has_support(var, value):
                for other_var in con.get_unasgn_vars():
                    for other_var_value in other_var.cur_domain():
                        if con.has_support(other_var, other_var_value):
                            for t in con.sup_tuples[(other_var, other_var_value)]:
                                if con.tuple_is_valid(t) and (t not in con.sup_tuples[(var, value)]):
                                    d[value] += 1


            else:
                d[value] = math.inf

    result = sorted(d, key=d.get)


    return result

def ord_custom(csp):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics
    that you have defined above.
    '''
#IMPLEMENT

    # Use MRV. If there is a tie, use DH to determine
    usasgn_vars = csp.get_all_unasgn_vars()
    min_remaining_value = math.inf
    highest_degree = 0
    result = usasgn_vars[0]

    for v in usasgn_vars:
        if v.cur_domain_size() < min_remaining_value:
            result = v
            min_remaining_value = v.cur_domain_size()
            highest_degree = 0
            for con in csp.get_cons_with_var(v):
                highest_degree += con.get_n_unasgn()

        if v.cur_domain_size() == min_remaining_value:
            v_degree = 0
            for con in csp.get_cons_with_var(v):
                v_degree += con.get_n_unasgn()

            if v_degree > highest_degree:
                result = v
                min_remaining_value = v.cur_domain_size()
                highest_degree = v_degree

    return result
