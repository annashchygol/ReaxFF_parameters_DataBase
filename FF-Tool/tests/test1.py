import unittest

class LearningCase(unittest.TestCase):
    def test_starting_out(self):
        self.assertEqual(1, 1)

# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self): # <- test case;
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))

def main():
    unittest.main()

if __name__ == "__main__":
    main()