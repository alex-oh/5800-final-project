# Function to return the index of the person with the minimum net amount
def findMinIndex(net_amounts):
    min_index = 0
    for i in range(len(net_amounts)):
        if net_amounts[i] < net_amounts[min_index]:
            min_index = i
    return min_index

# Function to return the index of the person with the maximum net amount
def findMaxIndex(net_amounts):
    max_index = 0
    for i in range(len(net_amounts)):
        if net_amounts[i] > net_amounts[max_index]:
            max_index = i
    return max_index

# Utility function to return the smaller of two values
def minOfTwo(x, y):
    return x if x < y else y

# Recursive function to settle debts
def settleDebts(net_amounts, min_transactions_needed):
    max_credit_index = findMaxIndex(net_amounts)
    max_debit_index = findMinIndex(net_amounts)

    # Termination condition: all amounts are settled
    if net_amounts[max_credit_index] == 0 and net_amounts[max_debit_index] == 0:
        return min_transactions_needed

    # Find the smaller of two amounts
    settlement_amount = minOfTwo(-net_amounts[max_debit_index], net_amounts[max_credit_index])
    net_amounts[max_credit_index] -= settlement_amount
    net_amounts[max_debit_index] += settlement_amount
    
    min_transactions_needed += 1

    # Recurse for the remaining amounts
    return settleDebts(net_amounts, min_transactions_needed)

# Main function to calculate and print the minimum cash flow
def calculateMinCashFlow(transactions):
    # Determine the total number of persons
    persons = set()
    for transaction in transactions:
        persons.add(transaction[0])
        persons.add(transaction[1])
    
    num_persons = len(persons)

    net_amounts = [0] * num_persons

    # Calculate the net amount for each person
    for transaction in transactions:
        from_person, to_person, amount = transaction
        net_amounts[from_person] -= amount
        net_amounts[to_person] += amount

    min_transaction = settleDebts(net_amounts, 0)
    print(min_transaction)

def main():
    transactions = [
        (0, 1, 1000),
        (0, 2, 500),
        (0, 3, 2000),
        (1, 2, 2000),
        (2, 3, 1000),
        (3, 1, 500)
    ]

    calculateMinCashFlow(transactions)

if __name__ == "__main__":
    main()