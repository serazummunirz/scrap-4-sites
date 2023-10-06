string = "Ge;ek * s:fo ! r;Ge * e*k:s !"
 
test_str = ''.join(letter for letter in string if letter.isalnum())
print(test_str)