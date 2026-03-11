import unittest
import project1_goohs_jonathan

class Test_MIU(unittest.TestCase):
    def test_r_one(self):
        # Create an instance of the MIU class (goal is irrelevant for this test)
        miu = project1_goohs_jonathan.MIU("MIU")
        
        # Test Rule 1 with a string that ends with "I"
        result = miu.r_one("MI")
        self.assertEqual(result, {"MIU"}, "Rule 1 did not apply correctly to 'MI'")

        #Test Rule 1 with a string that has no I in it
        result2 = miu.r_one("MU")
        self.assertEqual(result2,set(),"Rule 1 did not apply correctly.")

        result3 = miu.r_one("MII")
        
    def test_r_two(self):
        miu = project1_goohs_jonathan.MIU("MUU")
        result = miu.r_two("MIIIU")
        self.assertEqual(result,{"MUU"},"Rule 2 did not apply correctly")

        miu2 = project1_goohs_jonathan.MIU("IUU")
        result2 = miu2.r_two("IIIIU")
        self.assertEqual(result2,{"UIU","IUU"},"Rule 2 did not apply correctly")

        result3 = miu2.r_two("MIIIII")
        self.assertEqual(result3,{"MUII","MIUI","MIIU"},"Rule 2 did not apply correctly")

    def test_r_three(self):
        miu = project1_goohs_jonathan.MIU("goal")
        result = miu.r_three("UU")
        self.assertEqual(result,{""},"Rule three is wrong.")

        result2 = miu.r_three("MUIU")   
        self.assertEqual(result2,set(),"Rule three is wrong.")

        result3 = miu.r_three("MUU")
        self.assertEqual(result3,{"M"},"Rule three is wrong.")

    def test_r_four(self):
        miu = project1_goohs_jonathan.MIU("goal")
        result = miu.r_four("MUU")
        self.assertEqual(result,{"MUUUU"},"Rule four is wrong.")

        result2 = miu.r_four("UUU")
        self.assertEqual(result2,{"UUU"},"Rule four is wrong.")

        result3 = miu.r_four("MI")
        self.assertEqual(result3,{"MII"},"Rule four is wrong.")

        result4 = miu.r_four("IM")
        self.assertEqual(result4,{"IM"})

    def test_derive(self):
        miu = project1_goohs_jonathan.MIU("goal")        
        result = miu.derive("MI")
        self.assertEqual(result, {("|-4", "MII"), ("|-1", "MIU")}, "Derive method failed for 'MI'")
        
        result2 = miu.derive("MIUUIIII")
        self.assertEqual(result2, {("|-1", "MIUUIIIIU"), ("|-3", "MIIIII"), ("|-2", "MIUUIU"), ("|-2", "MIUUUI"), ("|-4", "MIUUIIIIIUUIIII")}, "Derive method failed for 'MIUUIIII'")
        
        result3 = miu.derive("MIIIII")
        self.assertEqual(result3, {("|-1", "MIIIIIU"), ("|-4", "MIIIIIIIIII"), ("|-2", "MIUI"), ("|-2", "MUII"),("|-2","MIIU")}, "Derive method failed for 'MIIIII'")

    def test_checker(self):
        '''Test cases based on specifications: 1. MUIU 2. MIIIII 3. MUUUI 4. MU'''
        miu = project1_goohs_jonathan.MIU("MUIU")
        result = miu.check()
        self.assertEqual(result,True,"The checker did not work.")

        miu2 = project1_goohs_jonathan.MIU("MIIIII")
        result2 = miu2.check()
        self.assertEqual(result2,True,"the checker did not work")

        miu3 = project1_goohs_jonathan.MIU("MUUUI")
        result3 = miu3.check()
        self.assertEqual(result3,False,"the checker did not work")

        miu4 = project1_goohs_jonathan.MIU("MU")
        result2 = miu4.check()
        self.assertEqual(result3,False,"the checker did not work")

if __name__ == '__main__':
    unittest.main()

    
