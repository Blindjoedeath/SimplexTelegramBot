from pulp import *

def solve(consumptions):
    resourceNames = set(map(lambda x: x.resource.name, consumptions))
    productNames = set(map(lambda x: x.product.name, consumptions))

    # lpConstraint object with resource name as key
    combinationDict = dict.fromkeys(resourceNames)
    problem = LpProblem("problem", LpMaximize)

    # price of lpVariable
    varsAndPrise = {}

    for productName in productNames:
        # grouped by product name
        prodConsumptions = [c for c in consumptions if c.product.name == productName]
        lpVar = LpVariable(productName, 0)
        varsAndPrise[lpVar] = prodConsumptions[0].product.price
        for cons in prodConsumptions:
            combinationDict[cons.resource.name] += lpVar * cons.resNorm

    for resName, combination in combinationDict.items():
        problem += combination <= list(filter(lambda x: x.resource.name == resName, consumptions))[0].resource.count

    # objective func
    problem += sum([x * varsAndPrise[x] for x in varsAndPrise])
    problem.solve()

    for var in varsAndPrise.keys():
        print(var.name + " : " + str(var.value()))

