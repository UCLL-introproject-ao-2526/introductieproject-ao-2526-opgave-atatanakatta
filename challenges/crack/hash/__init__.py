# 10ceee87f8b145ab495c3bca73b94455970159c6 op internet achterhaald het woord was BROWNIE maar 
# SHA-1 kan je niet terugrekenen, om zeker van te zijn heb ik deze nog eens gecontrolleer via de volgende.
# verficatie in git bash
# echo -n "BROWNIE" | sha1sum

# verficatie in python
import hashlib
print(hashlib.sha1(b"BROWNIE").hexdigest())

# brute force check
# import hashlib
# import itertools
# import string
# target = "10ceee87f8b145ab495c3bca73b94455970159c6"
# letters = string.ascii_uppercase  # A-Z
# for combo in itertools.product(letters, repeat=7):
#     word = "".join(combo)
#     hash_value = hashlib.sha1(word.encode()).hexdigest()
#     if hash_value == target:
#         print("FOUND:", word)
#         break