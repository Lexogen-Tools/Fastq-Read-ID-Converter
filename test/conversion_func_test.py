import unittest
from convert_readid import convert_MGI_ID

class ConversionTests(unittest.TestCase):
    def test_convert_MGI_ID(self):
        expected_id_R1 = "ID2:ID1:V350018879:4:10:1:2 1:N:0:AAAAA+TTTTT"
        new_id_R1 = convert_MGI_ID("V350018879L4C001R0020000010/1", "AAAAA", "TTTTT", "ID1", "ID2")
        self.assertEqual(new_id_R1, expected_id_R1)

        expected_id_R2 = "ID2:ID1:V350018879:4:10:1:2 2:N:0:AAAAA+TTTTT"
        new_id_R2 = convert_MGI_ID("V350018879L4C001R0020000010/2", "AAAAA", "TTTTT", "ID1", "ID2")
        self.assertEqual(new_id_R2, expected_id_R2)