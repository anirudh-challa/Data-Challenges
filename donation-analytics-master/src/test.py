
import unittest




class TestRecordisValid(unittest.TestCase):

    def record_is_valid(self, cmte_id, name, zipcode, transaction_date, transaction_amt, other):
        if len(cmte_id) == 0 or len(name) == 0 or len(zipcode) < 5 or len(transaction_date)!=8 \
        or len(transaction_amt) == 0 or len(other) > 0:
            return False
        return True
  
    def test_ecord_is_valid(self):
       self.assertFalse (self.record_is_valid('C00629618', 'PEREZ, JOHN A', '90017', '01032017', '40', 'H6CA34245'), False)
       self.assertTrue (self.record_is_valid('C00629618', 'PEREZ, JOHN A', '90017', '01032017', '40', '') ,True)

if __name__ == '__main__':
    unittest.main()