import mmh3
import math

from bitarray import bitarray

LN2 = math.log(2)


def mmh3_hash(key, seed):
    # map 32-bit hash value to an unsigned integer
    return mmh3.hash(key, seed) & 0xffffffff


class BloomFilter(object):
    def __init__(self, capacity, error_rate=0.01):
        self.error_rate = error_rate
        self.capacity = capacity
        self.hash_count = BloomFilter.estimate_hash_count(error_rate)
        self.bits_per_hash = BloomFilter.estimate_bits_per_hash(self.hash_count, capacity, error_rate)
        self.num_bits = self.hash_count * self.bits_per_hash
        self.bit_array = bitarray(self.num_bits)
        self.bit_array.setall(0)

    def add(self, key):
        offset = 0
        for seed in xrange(self.hash_count):
            result = mmh3_hash(key, seed) % self.bits_per_hash
            self.bit_array[offset + result] = 1
            offset += self.bits_per_hash

    def __contains__(self, key):
        offset = 0
        for seed in xrange(self.hash_count):
            result = mmh3_hash(key, seed) % self.bits_per_hash
            if self.bit_array[offset + result] == 0:
                return False
            offset += self.bits_per_hash
        return True

    def copy(self):
        clone =BloomFilter(self.capacity, self.error_rate)
        clone.bit_array = self.bit_array.copy()
        return clone

    def intersection(self, other):
        if self.capacity != other.capacity or self.error_rate != other.error_rate:
            raise ValueError("Both bloom filters should have equal capacity and error rate")

        intersect = self.copy()
        intersect.bit_array = intersect.bit_array & other.bit_array
        return intersect

    def union(self, other):
        if self.capacity != other.capacity or self.error_rate != other.error_rate:
            raise ValueError("Both bloom filters should have equal capacity and error rate")

        uni = self.copy()
        uni.bit_array = uni.bit_array | other.bit_array
        return uni

    @staticmethod
    def estimate_bits_per_hash(hash_count, capacity, error_rate):
        return int(math.ceil(-capacity * math.log(error_rate) / (hash_count * (LN2 * LN2))))

    @staticmethod
    def estimate_hash_count(error_rate):
        return int(math.ceil(math.log(1.0 / error_rate, 2)))
