from bitarray import bitarray
import mmh3
import math

LN2 = math.log(2)


class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, key):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(key, seed) % self.size
            self.bit_array[result] = 1

    def get(self, key):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(key, seed) % self.size
            if self.bit_array[result] == 0:
                return False
        return True


def estimate_size(n, p):
    return -n * math.log(p) / (LN2 * LN2)


def estimate_hash_count(n, m):
    return m * LN2 / float(n)


def estimate_parameters(n, p):
    m = estimate_size(n, p)
    k = estimate_hash_count(n, m)
    return m, k
