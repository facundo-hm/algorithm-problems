'''
You are in charge of the cake for a child's birthday.
You have decided the cake will have one candle for each
year of their total age. They will only be able to blow
out the tallest of the candles. Count how many candles
are tallest.

Example
candles = [4, 4, 1, 3]

The maximum height candles are 4 units high.
There are 2 of them, so return 2.
'''

def birthday_cake_candles(candles):
    tallest_candles = 0
    tallest_value = candles[0]

    for candle in candles:
        if candle > tallest_value:
            tallest_candles = 1
            tallest_value = candle
            continue

        if candle == tallest_value:
            tallest_candles += 1

    return tallest_candles
