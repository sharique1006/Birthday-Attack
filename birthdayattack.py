import sys
import random
import hashlib
import matplotlib.pyplot as plt

def get_hash(s):
	return hashlib.sha3_256(str(s).encode()).hexdigest()[:d]

def hex_to_bin(s):
	res = ''.join(format(ord(i), 'b') for i in s)
	return res

def birthday_attack(d):
    log_dict = dict()
    hash_num = 0
    attempt_count = 0
    while True:
        hash_num += random.random()
        digest = hashlib.sha3_256(str(hash_num).encode()).hexdigest()[:6]
        bin_digest = hex_to_bin(digest)[:d]
        if bin_digest in log_dict and len(str(hash_num)) == len(str(log_dict[bin_digest])):
            s1 = str(hash_num)
            s2 = str(log_dict[bin_digest])
            h1 = get_hash(hash_num)
            h2 = get_hash(log_dict[bin_digest])
            bin_h1 = hex_to_bin(h1)[:d]
            bin_h2 = hex_to_bin(h2)[:d]
            return (attempt_count, s1, s2, h1, h2, bin_h1, bin_h2, sys.getsizeof(log_dict))
        log_dict[bin_digest] = str(hash_num)
        attempt_count += 1

A = []
D = []
M = []

for d in range(1, 25):
    attempts, s1, s2, h1, h2, bin_h1, bin_h2, mem = birthday_attack(d)
    A.append(attempts)
    D.append(d)
    M.append(mem)
    print('d =', d)
    print('s1 = {}, s2 = {}'.format(s1, s2))
    print('h1 = {}, d bits of h1 = {}'.format(h1, bin_h1))
    print('h2 = {}, d bits of h2 = {}'.format(h2, bin_h2))
    print('m = {} KB'.format(mem))
    print('n = {} Attempts'.format(attempts))
    print()

plt.figure()
plt.plot(D, A)
plt.title('Number of attempts vs length of hash output')
plt.xlabel('d = Length of Hash Output')
plt.ylabel('n = Number of Attempts')
plt.savefig('attempts.png')
plt.show()
plt.close()

plt.figure()
plt.plot(D, M)
plt.title('Memory Used vs length of hash output')
plt.xlabel('Length of Hash Output')
plt.ylabel('Memory Used (KB)')
plt.savefig('memory.png')
plt.show()
plt.close()

