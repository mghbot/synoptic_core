from expression_parser import (
    parse_expression,
    extract_variables,
    evaluate_expression
)

from itertools import product

def generate_truth_table(expression):
    ast = parse_expression(expression)
    variables = sorted(list(extract_variables(ast)))

    table = {
        "columns": variables + ["result"],
        "rows": []
    }

    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        result = evaluate_expression(ast, assignment)
        table["rows"].append(
            [str(value) for value in values] + [str(result)]
        )

    return table
