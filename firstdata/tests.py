import firstdata
import unittest
import os


class FirstDataTests(unittest.TestCase):
    def test_p(self):
        #
        # Purchase
        #
        sale = self.purchase()
        self.assertEquals(sale['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(sale['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(sale['transaction_error'], 0, "Transaction had an error.")

    def test_r(self):
        #
        # Refund
        #
        refund = self.refund()
        self.assertEquals(refund['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(refund['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(refund['transaction_error'], 0, "Transaction had an error.")

    def test_pa_tv(self):
        #
        # Pre-Authorization
        # Tagged-Void
        #
        sale = self.pre_authorization()
        self.assertEquals(sale['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(sale['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(sale['transaction_error'], 0, "Transaction had an error.")

        # Pre-Authorzation Completion
        void = self.tagged_void(sale)
        self.assertEquals(void['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(void['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(void['transaction_error'], 0, "Transaction had an error.")

    def test_pa_pac_ptr(self):
        #
        # Pre-Authorization
        # Pre-Authorzation Completion
        # Tagged-Refund - Parial
        #
        sale = self.pre_authorization()
        self.assertEquals(sale['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(sale['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(sale['transaction_error'], 0, "Transaction had an error.")

        # Pre-Authorzation Completion
        tagcomp = self.tagged_pre_authorization_complete(sale)
        self.assertEquals(tagcomp['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(tagcomp['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(tagcomp['transaction_error'], 0, "Transaction had an error.")

        # Tagged-Refund
        refund = self.tagged_refund(tagcomp, amount="5.00")
        self.assertEquals(refund['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(refund['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(refund['transaction_error'], 0, "Transaction had an error.")

    def test_pa_tip_pac(self):
        #
        # Pre-Authorization
        # Pre-Authorzation Completion + $1.00 Tip
        #
        sale = self.pre_authorization()
        self.assertEquals(sale['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(sale['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(sale['transaction_error'], 0, "Transaction had an error.")

        # Pre-Authorzation Completion
        tagcomp = self.tagged_pre_authorization_complete(sale, amount="11.00")
        self.assertEquals(tagcomp['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(tagcomp['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(tagcomp['transaction_error'], 0, "Transaction had an error.")

    def test_pa_void_pap_v(self):
        #
        # Pre-Authorization
        # Void w/ TransArmor
        # Purchase w/ TransArmor
        # Refund w/ Transarmor
        #
        sale = self.pre_authorization()
        self.assertEquals(sale['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(sale['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(sale['transaction_error'], 0, "Transaction had an error.")

        # Void
        void = self.void_transarmor(sale)
        self.assertEquals(void['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(void['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(void['transaction_error'], 0, "Transaction had an error.")

        # Purchase w/ TransArmor
        purchase = self.purchase_transarmor(void or sale, amount="15.00")
        self.assertEquals(purchase['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(purchase['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(purchase['transaction_error'], 0, "Transaction had an error.")

        # Refund
        refund = self.refund_transarmor(purchase)
        self.assertEquals(refund['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(refund['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(refund['transaction_error'], 0, "Transaction had an error.")

    def test_pa_void_pat_patc(self):
        #
        # Pre-Authorization
        # Void w/ TransArmor
        # Pre-Authorization w/ TransArmor
        # Pre-Authorization Complete w/ TransArmor
        #
        sale = self.pre_authorization()
        self.assertEquals(sale['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(sale['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(sale['transaction_error'], 0, "Transaction had an error.")

        # Void
        void = self.void_transarmor(sale)
        self.assertEquals(void['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(void['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(void['transaction_error'], 0, "Transaction had an error.")

        # Pre-Authorization w/ TransArmor
        purchase = self.pre_authorization_transarmor(sale, amount="15.00")
        self.assertEquals(purchase['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(purchase['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(purchase['transaction_error'], 0, "Transaction had an error.")

        # Pre-Authorization Complete w/ TransArmor
        comp = self.tagged_pre_authorization_complete_transarmor(purchase)
        self.assertEquals(comp['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(comp['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(comp['transaction_error'], 0, "Transaction had an error.")

    def test_pa_void_pat_tv(self):
        #
        # Pre-Authorization
        # Void w/ TransArmor
        # Pre-Authorization w/ TransArmor
        # Tagged Void
        #
        sale = self.pre_authorization()
        self.assertEquals(sale['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(sale['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(sale['transaction_error'], 0, "Transaction had an error.")

        # Void
        void = self.void_transarmor(sale)
        self.assertEquals(void['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(void['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(void['transaction_error'], 0, "Transaction had an error.")

        # Pre-Authorization w/ TransArmor
        purchase = self.pre_authorization_transarmor(sale, amount="15.00")
        self.assertEquals(purchase['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(purchase['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(purchase['transaction_error'], 0, "Transaction had an error.")

        # Tagged Void
        void = self.tagged_void(purchase)
        self.assertEquals(void['exact_resp_code'], "00", "Transaction had an error.")
        self.assertEquals(void['transaction_approved'], 1, "Transaction had an error.")
        self.assertEquals(void['transaction_error'], 0, "Transaction had an error.")

    def pre_authorization(self, **kwargs):
        #
        # Pre-Authorization
        #
        print "--------> Pre-Authorization"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="01",
                        cardholder_name="Daffy Duck",
                        amount="10.00",
                        cc_number="4111111111111111",
                        cc_expiry="1215")
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def tagged_pre_authorization_complete(self, sale, **kwargs):
        #
        # Tagged Pre-Authorization Completion
        #
        print "--------> Tagged Pre-Authorization Completion"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="32",
                        authorization_num=sale['authorization_num'],
                        transaction_tag=sale['transaction_tag'],
                        amount=sale['amount'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def purchase_transarmor(self, sale, **kwargs):
        #
        # Purchase w/ TransArmor
        #
        print "--------> Purchase w/ TransArmor"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="00",
                        cardholder_name="Daffy Duck",
                        transarmor_token=sale['transarmor_token'],
                        amount=sale['amount'],
                        credit_card_type=sale['credit_card_type'],
                        cc_expiry=sale['cc_expiry'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def void_transarmor(self, sale, **kwargs):
        #
        # Tip > 15% => Void
        #
        print "--------> Void w/ TransArmor"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="33",
                        amount="10.00",
                        transarmor_token=sale['transarmor_token'],
                        cc_expiry=sale['cc_expiry'],
                        credit_card_type=sale['credit_card_type'],
                        authorization_num=sale['authorization_num'],
                        transaction_tag=sale['transaction_tag'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def pre_authorization_transarmor(self, sale, **kwargs):
        #
        # Pre-Authoization w/ TransArmor Token for $15.00
        #
        print "--------> Pre-Authorization w/ TransArmor"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="01",
                        transarmor_token=sale['transarmor_token'],
                        cardholder_name="Daffy Duck",
                        amount="15.00",
                        credit_card_type=sale['credit_card_type'],
                        cc_expiry=sale['cc_expiry'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def tagged_pre_authorization_complete_transarmor(self, sale, **kwargs):
        #
        # Tagged Pre-Authorization Completion w/ TransArmor
        #
        print "--------> Tagged Pre-Authorization Completion w/ TransArmor"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="32",
                        cardholder_name=sale['cardholder_name'],
                        transarmor_token=sale['transarmor_token'],
                        amount=sale['amount'],
                        credit_card_type=sale['credit_card_type'],
                        authorization_num=sale['authorization_num'],
                        transaction_tag=sale['transaction_tag'],
                        cc_expiry=sale['cc_expiry'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def void_pre_authorization_transarmor(self, armorsale, **kwargs):
        #
        # Void a Pre-Authorization w/ TransArmor
        #
        print "--------> Void - Pre-Authorization w/ TransArmor"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="13",
                        transarmor_token=armorsale['transarmor_token'],
                        cardholder_name="Daffy Duck",
                        amount="15.00",
                        authorization_num=armorsale['authorization_num'],
                        credit_card_type=armorsale['credit_card_type'],
                        cc_expiry=armorsale['cc_expiry'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def purchase(self, **kwargs):
        #
        # Purchase
        #
        print "--------> Purchase"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="00",
                        cardholder_name="Daffy Duck",
                        cc_number="4111111111111111",
                        amount="10.00",
                        cc_expiry="1215")
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def refund(self, **kwargs):
        #
        # Refund
        #
        print "--------> Refund"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="04",
                        cardholder_name="Daffy Duck",
                        cc_number="4111111111111111",
                        amount="10.00",
                        cc_expiry="1215")
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def tagged_refund(self, sale, **kwargs):
        #
        # Tagged Refund
        #
        print "--------> Tagged Refund"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="34",
                        transaction_tag=sale['transaction_tag'],
                        amount="10.00",
                        authorization_num=sale['authorization_num'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def tagged_void(self, sale, **kwargs):
        #
        # Tagged Void
        #
        print "--------> Tagged Void"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="33",
                        transaction_tag=sale['transaction_tag'],
                        amount=sale['amount'],
                        authorization_num=sale['authorization_num'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)

    def refund_transarmor(self, transarmor, **kwargs):
        #
        # Refund w/ TransArmor
        #
        print "--------> Refund w/ TransArmor"
        defaults = dict(gateway_id=os.environ.get('FD_GATEWAY_ID'),
                        password=os.environ.get('FD_PASSWORD'),
                        transaction_type="04",
                        cardholder_name="Daffy Duck",
                        transarmor_token=transarmor['transarmor_token'],
                        amount=transarmor['amount'],
                        credit_card_type=transarmor['credit_card_type'],
                        cc_expiry=transarmor['cc_expiry'])
        defaults.update(kwargs)
        return firstdata.FirstData(os.environ.get('FD_KEY'), os.environ.get('FD_SECRET'), **defaults).process(test=True)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
