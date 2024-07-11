
def knapsack_topdown(w, v, c):
    n = len(w)
    memo = {}
    def knapsack_aux(i, rc):
        if i < 0 or rc <= 0:   #rc:capacite_restante dans le sac a dos
            return 0, []

        if (i, rc) in memo:
            return memo[(i, rc)]

        if w[i] > rc:    # Ignorons l'élément si son poids dépasse la capacité restante
            memo[(i, rc)] = knapsack_aux(i - 1, rc)
            return memo[(i, rc)]
        
        # Considérer les deux cas : inclure l'élément et exclure l'élément.on choisi celui qui porte le plus 
        in_val, in_list = knapsack_aux(i - 1, rc - w[i])
        in_val += v[i]
        in_list = in_list + [i] if i not in in_list else in_list
        ex_val, ex_list = knapsack_aux(i - 1, rc)

        if in_val > ex_val:
            memo[(i, rc)] = (in_val, in_list)
            return in_val, in_list
        else:
            memo[(i, rc)] = (ex_val, ex_list)
            return ex_val, ex_list

    return knapsack_aux(n - 1, c)

# Bottom-up approach
def knapsack_bottomup(w, v, c):
    n = len(w)
    dp = [[0] * (c + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, c + 1):
            if w[i - 1] <= j:
                dp[i][j] = max(v[i - 1] + dp[i - 1][j - w[i - 1]], dp[i - 1][j])
            else:
                dp[i][j] = dp[i - 1][j]

    # Retrouvons les éléments sélectionnés
    selected_items = []
    total_val = dp[n][c]
    j = c
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected_items.append(i - 1)
            j -= w[i - 1]

    return total_val, selected_items

# Example:
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5

# Utilisons la top-down approach
total_val, selected_items = knapsack_topdown(weights, values, capacity)
print("Total value:", total_val)
print("Selected items:", selected_items)

# Utilisons la bottom-up approach
total_val, selected_items = knapsack_bottomup(weights, values, capacity)
print("Total value:", total_val)
print("Selected items:", selected_items)
