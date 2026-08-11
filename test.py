string = "1,2,3,4 23  23" 
string += " "

start, end = 0, None
parsed = []
non_int = 0

digit = ""


for char in string:
    if char.isdigit():
        digit += char
    elif digit:
        print(char, digit)
        parsed.append(int(digit))
        digit = ""
        
if digit:
    parsed.append(int(digit))

        
         
        
print(parsed)

import re

reparsed = [int(match) for match in re.findall(r'\d+', string)]

print(reparsed)