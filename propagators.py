'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
    propagator(csp, newly_instantiated_variable=None)
        ==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

Consider implementing propagators for forward cehcking or GAC as a course project!

'''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''
    PRE: csp; newVar is assigned
    POST: no unassigned otherVar related to newVar by a constraint has an inconsistent value in its domain
    '''
    if not newVar:
        # Only operate on an assigned variable
        return True, []

    constraints = csp.get_cons_with_var(newVar)
    prune = []
    for constraint in constraints:
        prune = [
            (var, val) for var in constraint.get_unasgn_vars()
                for val in var.cur_domain()
                    if not constraint.has_support(var, val)]

        for var, val in prune:
            var.prune_value(val)
            if len(var.cur_domain()) == 0:
                return False, prune

    return True, prune

def prop_GAC(csp, newVar=None):
    '''Performs GAC on a given CSP.
    Returns (has_DWO, pruned_values).'''
    if not newVar:
        queue = csp.get_all_cons()
    else:
        queue = csp.get_cons_with_var(newVar)

    prune = []
    while len(queue) > 0:
        constraint = queue.pop(0)
        # Prepare a list of variable-value tuples that need to be pruned
        var_val_t = [
            (var, val) for var in constraint.get_scope()
                for val in var.cur_domain()
                    if not constraint.has_support(var, val)]

        for var, val in var_val_t:
            prune.append((var, val))
            var.prune_value(val)
            if len(var.cur_domain()) == 0:
                # DWO, exit
                return (False, prune)
            else:
                # Continue
                queue += [other_constraint for other_constraint in csp.get_cons_with_var(var) if other_constraint not in queue]
    return (True, prune)
