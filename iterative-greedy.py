# Python3 program to find optimized cash flow among a set of persons
import time


def print_credit_transaction(credit_entry, debit_entry):
    '''Function that prints transactions that use the full credit amount'''
    # prints a transaction between a creditor and and a debitor
    # structure of credit/debit entry: [net_amount, person_index]
    # Print transaction
    print(
        f"Person {credit_entry[1]} pays {-1 * credit_entry[0]} to Person {debit_entry[1]}")


def print_debit_transaction(credit_entry, debit_entry):
    '''Function that prints transactions that use the full debit amount'''
    print(
        f"Person {credit_entry[1]} pays {debit_entry[0]} to Person {debit_entry[1]}")


def resolve_debts(credits, debits):
    '''
    Function that finds the fewest transactions to resolve debts
    Parameters: credits, debits - arrays of node net values representing who owes money and who will get money
    Returns: edges - number of transactions calculated
    '''
    edges = 0
    # (The following steps are executed O(n^2) times)
    # 3. Arrange the nodes from greatest absolute amount to least absolute amount.
    credits.sort()
    debits.sort(reverse=True)

    credit_entry = 0
    while credit_entry < len(credits):
        old_edge = edges # track whether an edge has changed in the previous loop
        debit_entry = 0
        while debit_entry < len(debits):
            # find a node on the debit side that has the equivalent value such that the
            # net flow credit node + net flow debit node = 0.
            if credits[credit_entry][0] + debits[debit_entry][0] == 0:
                # record transaction in edges
                edges += 1
                print_credit_transaction(credits[credit_entry], debits[debit_entry])

                # remove the credit and debit entries from the lists since that transaction has happened
                credits.pop(credit_entry)
                debits.pop(debit_entry)
                break
            else:
                debit_entry += 1
        
        # if no transaction has been recorded on this credit entry comparison, move to next credit entry
        if edges == old_edge:  
            credit_entry += 1

    # Balance out the remaining credit/debit nodes
    credit_entry = 0 # credits list index
    debit_entry = 0 # debits list index

    while len(credits) > 0 and len(debits) > 0:
        # Starting from largest credit node, connect an edge to the largest debit node and adjust node values
        sum = credits[credit_entry][0] + debits[debit_entry][0]
        # Record the edge formed by doing this transaction
        edges += 1
        if sum >= 0:
            print_credit_transaction(
                credits[credit_entry], debits[debit_entry])
        else:
            print_debit_transaction(credits[credit_entry], debits[debit_entry])

        # Check result of transaction
        # Debit still exists
        if sum > 0:  
            # subtract credit entry amt from debit entry amount and remove credit entry
            debits[debit_entry][0] += credits.pop(credit_entry)[0]
            debits.sort(reverse=True)
        # Credit still exists
        elif sum < 0:  
            # Subtract debit entry amt from credit entry amount and remove debit entry
            credits[credit_entry][0] += debits.pop(debit_entry)[0]
            credits.sort()
        # sum == 0, so we remove both the credit and debit transactions
        else:  
            credits.pop(credit_entry)
            debits.pop(debit_entry)

    return edges


def calculateMinCashFlow(transactions):
    '''Main function to calculate and print the minimum cash flow'''
    # Determine the total number of persons
    persons = set()
    for transaction in transactions:
        persons.add(transaction[0])
        persons.add(transaction[1])

    num_persons = len(persons)

    net_amounts = [0] * num_persons

    # Figure out the net flow at each node.
    # This value must stay the same at all times since this
    # represents the total amount of money a person is moving.
    # O(n*(n-1)) n nodes, n-1 edges attached to n nodes

    # Calculate net amount for each person
    for transaction in transactions:
        from_person, to_person, amount = transaction
        net_amounts[from_person] -= amount
        net_amounts[to_person] += amount

    print(net_amounts)

    # Split the nodes into two groups: 
    # - credit (owing money overall, net flow < 0)
    # - debit (receiving money overall, net flow > 0). 
    # Discard any nodes that have net flow == 0. 
    # 
    # The credit group owes money to the debit group. It should also be noted 
    # that the total amount of money the credit group owes is equal to the total
    # amount of money the debit group should receive.
    credits = []  # people who lose money, element structure: [net amount, person number]
    debits = []  # people who will gain money

    # Sort people into credits or debits group based on net_amounts value
    for person_num in range(len(net_amounts)):
        net_amt = net_amounts[person_num]
        if net_amt > 0:
            # add to debit
            debits.append([net_amt, person_num])
        elif net_amt < 0:
            # add to credit
            credits.append([net_amt, person_num])
        # else the amount is 0, and this person has no debts or credits.

    edges = resolve_debts(credits, debits)
    print(f"Transactions: {edges}")
    return edges

def main():
    transactions1 = [
        (0, 1, 1000),
        (0, 2, 500),
        (0, 3, 2000),
        (1, 2, 2000),
        (2, 3, 1000),
        (3, 1, 500)
    ]

    transactions2 = [
        (0, 1, 1000),
        (0, 2, 500),
        (0, 3, 2000),
        (1, 2, 500),
        (2, 3, 1000),
        (3, 1, 2000)
    ]

    transactions3 = [
        (0, 1, 1000),
        (0, 2, 500),
        (1, 2, 2000),
        (2, 3, 1000),
        (3, 1, 500),
        (3, 0, 2000)
    ]

    transactions4 = [(8, 0, 1524), (3, 2, 1913), (6, 4, 986), (8, 5, 1669),
                     (0, 3, 401), (4, 7, 799), (3, 8, 1633), (1, 9, 679), (7, 1, 1886)]
    # track the execution time
    start_time = time.time()

    print("Pseudo-flow")
    print("Transaction 1")
    calculateMinCashFlow(transactions1)

    print("Transaction 2")
    calculateMinCashFlow(transactions2)

    print("Transaction 3")
    calculateMinCashFlow(transactions3)

    print("Transaction 4")
    calculateMinCashFlow(transactions4)

    # log program runtime
    print("--- Executed in %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
