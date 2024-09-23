'''
https://www.hackerrank.com/challenges/coin-change/problem

Given an amount and the denominations of coins available,
determine how many ways change can be made for amount.
There is a limitless supply of each coin type.

Example
n = 3
c = [8, 3, 1, 2]
There are 3 ways to make change for n = 3: {1, 1, 1},
{1, 2}, and 3.
'''

def getWays(n, c):
    memo = dict()

    for cent in c:
        current_c_value = cent        
        current_c_memo = {**memo}

        while current_c_value <= n:          
            for memo_key in memo:
                new_memo_key = memo_key + current_c_value

                if new_memo_key > n:
                    continue

                current_c_memo[new_memo_key] = (
                    current_c_memo.get(new_memo_key, 0)
                    + memo.get(memo_key, 0))

            current_c_memo[current_c_value] = (
                current_c_memo.get(current_c_value, 0) + 1)
            current_c_value += cent

        memo.update(current_c_memo)

    return memo.get(n, 0)
