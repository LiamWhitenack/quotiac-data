from random import shuffle

ALPHABET = list("qwertyuiopasdfghjklzxcvbnm")
shuffled = ALPHABET.copy()
shuffle(shuffled)
mapper = {letter: ALPHABET.pop() for letter in shuffled}


print("".join(map(lambda x: mapper.get(x, x), "botanically, strawberries are not berries, but bananas are")))