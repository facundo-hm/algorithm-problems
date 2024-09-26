'''
https://leetcode.com/problems/reverse-integer

Given a signed 32-bit integer x, return x with its digits
reversed. If reversing x causes the value togo outside the
signed 32-bit integer range [-2^31, 2^31 - 1], then return 0.

Example 1:
Input: x = 123
Output: 321

Example 2:
Input: x = -123
Output: -321

Example 3:
Input: x = 120
Output: 21
'''

def reverse(x: int) -> int:
    if x != 0:
        x_abs = abs(x)
        sign = x // x_abs
        x_new = int(str(x_abs)[::-1]) * sign

        if x_new >= -2**31 and x_new <= 2**31 - 1:
            return x_new
    
    return 0
