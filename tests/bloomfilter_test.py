import mmh3
import unittest
from pds.bloomfilter import BloomFilter


class TestBloomFilter(unittest.TestCase):
    def test_k_and_m(self):
        bf = BloomFilter(1000000, 0.001)
        self.assertAlmostEqual(bf.hash_count, 10)
        self.assertAlmostEqual(bf.bits_per_hash, 1437759)
        self.assertAlmostEqual(bf.num_bits, 14377590)

    def test_hashing(self):
        bf = BloomFilter(10, 0.3)
        self.assertAlmostEqual(bf.hash_count, 2)
        self.assertAlmostEqual(bf.bits_per_hash, 13)

        key = 'test'
        bf.add(key)
        hash_1 = (mmh3.hash(key, 0) & 0xffffffff) % 13
        hash_2 = (mmh3.hash(key, 1) & 0xffffffff) % 13
        self.assertTrue(bf.bit_array[hash_1])
        self.assertTrue(bf.bit_array[hash_2 + 13])

        self.assertTrue(key in bf)

    def test_intersection(self):
        bf1 = BloomFilter(10, 0.3)
        bf1.add('test1')
        bf2 = BloomFilter(10, 0.3)
        bf2.add('test1')
        bf2.add('test2')
        bf3 = bf1.intersection(bf2)
        self.assertTrue('test1' in bf3)
        self.assertFalse('test2' in bf3)

        def _run():
            bf1.intersection(BloomFilter(11, 0.3))
        self.assertRaises(ValueError, _run)

    def test_union(self):
        bf1 = BloomFilter(10, 0.3)
        bf1.add('test1')
        bf2 = BloomFilter(10, 0.3)
        bf2.add('test1')
        bf2.add('test2')
        bf3 = bf1.union(bf2)
        self.assertTrue('test1' in bf3)
        self.assertTrue('test2' in bf3)

        def _run():
            bf1.union(BloomFilter(10, 0.2))
        self.assertRaises(ValueError, _run)


if __name__ == '__main__':
    unittest.main()
