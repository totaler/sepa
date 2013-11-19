# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField
from sepa19 import SepaHeader, GenericPhysicalLegalEntity, PaymentTypeInfo
from sepa19 import BankAccount, BankAgent, PaymentIdentifier, Purpose
from sepa19 import RegulatoryInformation, Concept


class Amount(XmlModel):
    _sort_order = ('amount', 'instructed_amount')
    
    def __init__(self):
        self.amount = XmlField('Amt')
        self.instructed_amount = XmlField('InstdAmt', attributes={'Ccy': ''})
        super(Amount, self).__init__('Amt', 'amount')
        
############################### Level 2 ######################################


class CreditTransferInfo(XmlModel):
    _sort_order = ('credit_transfer_info', 'payment_identifier',
                   'payment_type_info', 'amount', 'charge_clausule',
                   'ultimate_debtor', 'creditor_agent', 'creditor',
                   'creditor_account', 'ultimate_creditor', 'purpose',
                   'regulatory_reglament', 'concept')
    
    def __init__(self):
        self.credit_transfer_info = XmlField('CdtTrfTxInf')
        self.payment_identifier = PaymentIdentifier()
        self.payment_type_info = PaymentTypeInfo()
        self.amount = Amount()
        self.charge_clausule = XmlField('ChrgBr')
        self.ultimate_debtor = GenericPhysicalLegalEntity('UltmDbtr')
        self.creditor_agent = BankAgent('CdtrAgt')
        self.creditor = GenericPhysicalLegalEntity('Cdtr')
        self.creditor_account = BankAccount('CdtrAcct')
        self.ultimate_creditor = GenericPhysicalLegalEntity('UltmCdtr')
        self.purpose = Purpose()
        self.regulatory_reglament = RegulatoryInformation()
        self.concept = Concept()
        super(CreditTransferInfo, self).__init__('CdtTrfTxInf',
                                                 'credit_transfer_info')
            
############################### Level 1 ######################################


class PaymentInformation(XmlModel):
    _sort_order = ('payment_information', 'payment_info_identifier',
                   'payment_method', 'batchbook', 'number_of_operations',
                   'checksum', 'payment_type_info', 'collection_date',
                   'debtor', 'debtor_account', 'ultimate_debtor', 'charge_br',
                   'credit_transfer_info')
    
    def __init__(self):
        self.payment_information = XmlField('PmtInf')
        self.payment_info_identifier = XmlField('PmtInfId')
        self.payment_method = XmlField('PmntMtd')
        self.batchbook = XmlField('BtchBookg')
        self.number_of_operations = XmlField('NbOfTxs')
        self.checksum = XmlField('CtrlSum')
        self.payment_type_info = PaymentTypeInfo()
        self.collection_date = XmlField('ReqdColltnDt')
        self.debtor = GenericPhysicalLegalEntity('Dbtr')
        self.debtor_account = BankAccount('DbtrAcct')
        self.debtor_agent = BankAgent('DbtrAgt')
        self.ultimate_debtor = GenericPhysicalLegalEntity('UltmtDbtr')
        self.charge_clausule = XmlField('ChrgBr')
        self.credit_transfer_info = [] # CreditTransferInfo
        super(PaymentInformation, self).__init__('PmtInf',
                                                'payment_information')


############################### Level 0 ######################################


class CustomerCreditTransfer(XmlModel):
    _sort_order = ('root', 'sepa_header', 'payment_information')
    
    def __init__(self):
        self.root = XmlField('CstmrCdtTrfInitn')
        self.sepa_header = SepaHeader()
        self.payment_information = [] # PaymentInformation
        super(CustomerCreditTransfer, self).__init__('CstmrCdtTrfInitn',
                                                     'root')