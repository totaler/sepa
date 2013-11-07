# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField


class OtherLegalEntity(XmlModel):
    _sort_order = ('other', 'identification', 'scheme_name', 'issuer')

    def __init__(self):
        self.other = XmlField('Othr')
        self.identification = XmlField('Id')
        self.shceme_name = SchemeName()
        self.issuer = XmlField('Issr')
        super(OtherLegalEntity, self).__init__('Othr', 'other')


class DateAndPlaceOfBirth(XmlModel):
    _sort_order = ('date_and_place_of_birth', 'date', 'province', 'city',
                   'country', 'other')
        
    def __init__(self):
        self.date_and_place_of_birth = XmlField('DtAndPlcOfBirth')
        self.date = XmlField('BirthDt')
        self.province = XmlField('PrvcOfBirth')
        self.city = XmlField('CityOfBirth')
        self.country = XmlField('CtryOfBirth')
        self.other = OtherLegalEntity()
        super(DateAndPlaceOfBirth, self).__init__('DtAndPlcOfBirth',
                                                  'date_and_place_of_birth')

class SchemeName(XmlModel):
    _sort_order = ('scheme_name', 'code', 'propietary')
    
    def __init__(self):
        self.scheme_name = XmlField('SchmeNm')
        self.code = XmlField('Cd')
        self.propietary = XmlField('Prtry')
        super(SchemeName, self).__init__('SchmeNm', 'scheme_name')


class PhysicalPerson(XmlModel):
    _sort_order = ('physical_person', 'date_and_place_of_birth', 'other')

    def __init__(self):
        self.physical_person = XmlField('PrvtId')
        self.date_and_place_of_birth = DateAndPlaceOfBirth()
        self.other = OtherLegalEntity()
        super(PhysicalPerson, self).__init__('PrvtId', 'physical_person')

class LegalEntity(XmlModel):
    _sort_order = ('legal_entity', 'bic_or_bei', 'other')

    def __init__(self):
        self.legal_entity = XmlField('OrgId')
        self.bic_or_bei = XmlField('BICOrBEI')
        self.other = OtherLegalEntity()
        super(LegalEntity, self).__init__('OrgId', 'legal_entity')
        

class InitiationPartIdentification(XmlModel):
    _sort_order = ('identification', 'legal_entity', 'physical_person')
    
    def __init__(self):
        self.identification = XmlField('Id')
        self.legal_entity = LegalEntity()
        self.physical_person = PhysicalPerson()
        super(InitiationPartIdentification, self).__init__('Id',
                                                           'identification')


class InitiationPart(XmlModel):
    _sort_order = ('initiation_part', 'name', 'identification')
    
    def __init__(self):
        self.initiation_part = XmlField('InitgPty')
        self.name = XmlField('Nm')
        self.identification = InitiationPartIdentification()
        super(InitiationPart, self).__init__('InitgPty', 'initiation_part')


class SepaHeader(XmlModel):
    _sort_order = ('sepa_header', 'message_id', 'creation_date_time',
                   'number_of_operations', 'checksum', 'initiation_part')
    
    def __init__(self):
        self.sepa_header = XmlField('GrpHrd')
        self.message_id = XmlField('MsgId')
        self.creation_date_time = XmlField('CreDtTm')
        self.number_of_operations = XmlField('NbOfTxs')
        self.checksum = XmlField('CtrlSum')
        self.initiation_part = InitiationPart()
        super(SepaHeader, self).__init__('GrpHrd', 'sepa_header')


class ServiceLevel():
    pass


class LocalInstrument():
    pass


class CategoryPurpose():
    pass


class PaymentTypeInfo(XmlModel):
    _sort_order = ('payment_type_info', 'service_level', 'local_insturment',
                   'sequence_type', 'category_purpouse')
    
    def __init__(self):
        self.payment_type_info = XmlField('PmtpInf')
        self.service_level = ServiceLevel()
        self.local_insturment = LocalInstrument()
        self.sequence_type = XmlField('SeqTp')
        self.category_purpouse = CategoryPurpose()
        super(PaymentTypeInfo, self).__init__('PmtTpInf', 'payment_type_info')


class CreditorAccount(XmlModel):
    pass


class UltimateCreditor(XmlModel):
    pass


class CreditorIdentifier(XmlModel):
    pass


class DirectDebitOperationInfo(XmlModel):
    pass


class PaymentInformation(XmlModel):
    _sort_order = ('payment_information', 'payment_info_identifier',
                   'payment_method', 'batchbook', 'number_of_operations',
                   'checksum', 'payment_type_info', 'collection_date',
                   'creditor_account', 'ultimate_creditor', 'charge_clausule',
                   'creditor_identifier', 'direct_debit_operation_info')
    
    def __init__(self):
        self.payment_information = XmlField('PmtInf')
        self.payment_info_identifier = XmlField('PmtInfId')
        self.payment_method = XmlField('PmntMtd')
        self.batchbook = XmlField('BtchBookg')
        self.number_of_operations = XmlField('NbOfTxs')
        self.checksum = XmlField('CtrlSum')
        self.payment_type_info = PaymentTypeInfo()
        self.collection_date = XmlField('ReqdColltnDt')
        self.creditor_account = CreditorAccount()
        self.ultimate_creditor = UltimateCreditor()
        self.charge_clausule = XmlField('ChrgBr')
        self.creditor_identifier = CreditorIdentifier()
        self.direct_debit_operation_info = DirectDebitOperationInfo()        
        super(PaymentInformation, self).__init__('PmtInf',
                                                 'payment_information')

class DirectDebitInitMessage(XmlModel):
    _sort_order = ('root', 'sepa_header', 'payment_information')
    
    def __init__(self):
        self.root = XmlField('CstmrDrctDbtInitn')
        self.sepa_header = SepaHeader()
        self.payment_information = PaymentInformation()
        super(DirectDebitInitMessage, self).__init__('CstmrDrctDbtInitn', 'root')