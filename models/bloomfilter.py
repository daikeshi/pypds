import mmh3
import math

from bitarray import bitarray


LN2 = math.log(2)


class BloomFilter:
    def __init__(self, size=10, hash_count=2):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, key):
        for seed in xrange(self.hash_count):
            result = hash(key, seed) % self.size
            self.bit_array[result] = 1

    def __contains__(self, key):
        for seed in xrange(self.hash_count):
            result = hash(key, seed) % self.size
            if self.bit_array[result] == 0:
                return False
        return True

    @staticmethod
    def make_hash(key, seed):
        # map 32-bit hash value to an unsigned integer
        return mmh3.hash(key, seed) & 0xffffffff


def estimate_size(capacity, error_rate):
    return -capacity * math.log(error_rate) / (LN2 * LN2)


def estimate_hash_count(capacity, hash_size):
    return hash_size * LN2 / float(capacity)


def estimate_parameters(capacity, error_rate):
    m = estimate_size(capacity, error_rate)
    k = estimate_hash_count(capacity, m)
    return m, k
