# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField

""" Classes ar sorted by:
" - Indentation level of its *first* reference in documentation
" - Order of reference in documentation
"""

############################### Level 7 ######################################


class CodeOrPropietary(XmlModel):
    _sort_order = ('code_or_propietary', 'code')
    
    def __init__(self):
        self.code_or_propietary = XmlField('CdOrPrtry')
        self.code = XmlField('Cd')
        super(CodeOrPropietary, self).__init__('CdOrPrtry', 'code_or_propietary')


############################### Level 6 ######################################


class SchemeName(XmlModel):
    _sort_order = ('scheme_name', 'code', 'propietary')
    
    def __init__(self):
        self.scheme_name = XmlField('SchmeNm')
        self.code = XmlField('Cd')
        self.propietary = XmlField('Prtry')
        super(SchemeName, self).__init__('SchmeNm', 'scheme_name')


class OriginalDebiterAgent(XmlModel):
    _sort_order = ('original_debiter_agent', 'agent_identifier')
    
    def __init__(self):
        self.original_debiter_agent = XmlField('OrgnlDbtrAgt')
        self.agent_identifier = PhysicalLegalEntity('FinInstnId')
        super(OriginalDebiterAgent, self).__init__('OrgnlDbtrAgt',
                                                   'original_debiter_agent')


class ReferenceType(XmlModel):
    _sort_order = ('reference_type', 'code_or_propietary', 'issuer')

    def __init__(self):
        self.reference_type = XmlField('Tp')
        self.code_or_propietary = CodeOrPropietary()
        self.issuer = XmlField('Issr')
        super(ReferenceType, self).__init__('Tp', 'reference_type')


############################### Level 5 ######################################


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
        
        
class ModificationDetails(XmlModel):
    _sort_order = ('modification_details', 'original_mandate_id',
                   'original_creditor_id', 'original_debiter_account',
                   'original_debiter_agent')

    def __init__(self):
        self.modification_details = XmlField('AmdmntInfDtls')
        self.original_mandate_id = XmlField('OrgnlMndtId')
        self.original_creditor_id = GenericPhysicalLegalEntity('OrgnlMndtId')
        self.original_debiter_account = BankAccount('OrgnlDbtrAcct')
        self.original_debiter_agent = OriginalDebiterAgent()
        super(ModificationDetails, self).__init__('AmdmntInfDtls',
                                                  'modification_details')

class CreditorGivenReference(XmlModel):
    _sort_order = ('creditor_reference', 'reference_type', 'reference')
    
    def __init__(self):
        self.creditor_reference = XmlField('CdtrRefInf')
        self.reference_type = ReferenceType()
        self.reference = XmlField('Ref')
        super(CreditorGivenReference, self).__init__('CdtrRefInf',
                                                     'creditor_reference')


############################### Level 4 ######################################
        
        
class PhysicalLegalEntity(XmlModel):
    _sort_order = ('legal_entity', 'date_and_place_of_birth', 'bic_or_bei',
                   'other')

    def __init__(self, tag):
        self.legal_entity = XmlField(tag)
        self.date_and_place_of_birth = DateAndPlaceOfBirth()
        self.bic_or_bei = XmlField('BICOrBEI')
        self.other = OtherLegalEntity()
        super(PhysicalLegalEntity, self).__init__(tag, 'legal_entity')
        
        
class MandateInformation(XmlModel):
    _sort_order = ('mandate_information', 'mandate_identifier', 'date_of_sign',
                   'modification_indicator', 'modification_details',
                   'electronic_signature')
    
    def __init__(self):
        self.mandate_information = XmlField('MndtRltdInf')
        self.mandate_identifier = XmlField('MndId')
        self.date_of_sign = XmlField('DtOfSgntr')
        self.modification_indicator = XmlField('AdmmntInd')
        self.modification_details = ModificationDetails()
        self.electronic_signature = XmlField('ElctrncSgntr')
        super(MandateInformation, self).__init__('MndtRltdInf',
                                                 'mandate_information')
        

class RegulatoryInformationDetails(XmlModel):
    _sort_order = ('regulatory_information_details', 'code', 'amount',
                   'information')

    def __init__(self):
        self.regulatory_information_details = XmlField('Dtls')
        self.code = XmlField('Cd')
        self.amount = XmlField('Amt')
        self.information = XmlField('Inf')
        super(RegulatoryInformationDetails,
              self).__init__('Dtls', 'regulatory_information_details')


class StructuredConcept(XmlModel):
    _sort_order = ('strcuctured_concept', 'creditor_reference')
    
    def __init__(self):
        self.strcuctured_concept = XmlField('Strd')
        self.creditor_reference = CreditorGivenReference()
        super(StructuredConcept, self).__init__('CdtrRefInf',
                                                'strcuctured_concept')


############################### Level 3 ######################################


class GenericPhysicalLegalEntityId(XmlModel):
    _sort_order = ('identification', 'legal_entity', 'physical_person')

    def __init__(self):
        self.identification = XmlField('Id')
        self.legal_entity = PhysicalLegalEntity('OrgId')
        self.physical_person = PhysicalLegalEntity('PrvtId')
        super(GenericPhysicalLegalEntityId, self).__init__('Id',
                                                           'identification')


class ServiceLevel(XmlModel):
    _sort_order = ('service_level', 'code')

    def __init__(self):
        self.service_level = XmlField('SvcLvl')
        self.code = XmlField('Cd')
        super(ServiceLevel, self).__init__('SvcLvl', 'service_level')


class LocalInstrument(XmlModel):
    _sort_order = ('local_insturment', 'code')

    def __init__(self):
        self.local_insturment = XmlField('LclInstrm')
        self.code = XmlField('Cd')
        super(LocalInstrument, self).__init__('LclInstrm', 'local_insturment')

 
class CategoryPurpose(XmlModel):
    _sort_order = ('category_purpose', 'code')

    def __init__(self):
        self.category_purpose = XmlField('CtgyPurp')
        self.code = XmlField('Cd')
        self.propietary = XmlField('Prtry')
        super(CategoryPurpose, self).__init__('CtgyPurp', 'category_purpose')


class PostalAddress(XmlModel):
    _sort_order = ('postal_address', 'country', 'address_line')

    def __init__(self):
        self.postal_address = XmlField('PstlAdr')
        self.country = XmlField('Ctry')
        self.address_line = XmlField('AdrLine')
        super(PostalAddress, self).__init__('PstlAdr', 'postal_address')


class AccountIdentification(XmlModel):
    _sort_order = ('account_identification', 'iban')

    def __init__(self):
        self.account_identification = XmlField('Id')
        self.iban = XmlField('IBAN')
        super(AccountIdentification, self).__init__('Id',
                                                    'account_identification')


class AgentIdentifier(XmlModel):
    _sort_order = ('agent_identifier', 'bic')

    def __init__(self):
        self.agent_identifier = XmlField('FinInstnId')
        self.bic = XmlField('BIC')
        super(AgentIdentifier, self).__init__('FinInstnId', 'agent_identifier')


class PaymentIdentifier(XmlModel):
    _sort_order = ('payment_identifier', 'instrucction_identifier',
                   'end_to_end_identifier')

    def __init__(self):
        self.payment_identifier = XmlField('PmtId')
        self.instrucction_identifier = XmlField('InstrId')
        self.end_to_end_identifier = XmlField('EndToEndId')
        super(PaymentIdentifier, self).__init__('PmtId', 'payment_identifier')


class DirectDebitOperation(XmlModel):
    _sort_order = ('direct_debit_operation', 'mantade_information',
                   'creditor_identifier')

    def __init__(self):
        self.direct_debit_operation = XmlField('DrctDbtTx')
        self.mantade_information = MandateInformation()
        self.creditor_identifier = GenericPhysicalLegalEntity('CdtrSchmeId')
        super(DirectDebitOperation, self).__init__('DrctDbtTx',
                                                   'direct_debit_operation')


class Purpose(XmlModel):
    _sort_order = ('purpose', 'code')
    
    def __init__(self):
        self.purpose = XmlField('Purp')
        self.code = XmlField('Cd')
        super(Purpose, self).__init__('Purp', 'purpose')
         

class RegulatoryInformation(XmlModel):
    _sort_order = ('regulatory_information', 'information_range',
                   'information_details')
    
    def __init__(self):
        self.regulatory_information = XmlField('RgltryRptg')
        self.information_range = XmlField('DbtCdtRptgInd')
        self.information_details = RegulatoryInformationDetails()
        super(RegulatoryInformation, self).__init__('RegulatoryInformation',
                                                    'regulatory_information')

    
class Concept(XmlModel):
    _sort_order = ('concept', 'unstructured', 'structured')
    
    def __init__(self):
        self.concept = XmlField('RmtInf')
        self.unstructured = XmlField('Ustrd')
        self.structured = StructuredConcept()
        super(Concept, self).__init__('RmtInf', 'concept')


############################### Level 2 ######################################


class GenericPhysicalLegalEntity(XmlModel):
    _sort_order = ('main_tag', 'entity_name', 'PostalAddress', 'identification')
    
    def __init__(self, tag):
        self.main_tag = XmlField(tag)
        self.entity_name = XmlField('Nm')
        self.postal_address = PostalAddress()
        self.identification = GenericPhysicalLegalEntityId()
        super(GenericPhysicalLegalEntity, self).__init__(tag, 'main_tag')


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


class NameAndAddress(XmlModel):
    _sort_order = ('creditor', 'name', 'postal_address')
    
    def __init__(self, tag):
        self.main_tag = XmlField(tag)
        self.name = XmlField('Nm')
        self.postal_address = PostalAddress()
        super(NameAndAddress, self).__init__(tag, 'main_tag')


class BankAccount(XmlModel):
    _sort_order = ('creditor_account', 'account_identification', 'currency')
    
    def __init__(self, tag):
        self.bank_account = XmlField(tag)
        self.account_identification = AccountIdentification()
        self.currency = XmlField('Ccy')
        super(BankAccount, self).__init__(tag, 'bank_account')


class BankAgent(XmlModel):
    _sort_order = ('bank_agent', 'agent_identifier')
    
    def __init__(self, tag):
        self.bank_agent = XmlField(tag)
        self.agent_identifier = AgentIdentifier()
        super(BankAgent, self).__init__('CdtrAgt', 'bank_agent')
        
        
class DirectDebitOperationInfo(XmlModel):
    _sort_order = ('')

    def __init__(self):
        self.direct_debit_operation_info = XmlField('DrctDbtTxInf')
        self.payment_identifier = PaymentIdentifier()
        self.ordered_amount = XmlField('InstdAmt')
        self.charge_clausule = XmlField('ChrgBr')
        self.direct_debit_operation = DirectDebitOperation()
        self.ultimate_creditor = GenericPhysicalLegalEntity('UltmtCdtr')
        self.debiter_agent = BankAgent('DbtrAgt')
        self.debiter = GenericPhysicalLegalEntity('Dbtr')
        self.debiter_account = BankAccount('DbtrAcct')
        self.ultimate_debiter = GenericPhysicalLegalEntity('UltmDbtr')
        self.purpose = Purpose()
        self.regulatory_reglament = RegulatoryInformation()
        self.concept = Concept()
        super(DirectDebitOperationInfo,
              self).__init__('DrctDbtTxInf', 'direct_debit_operation_info')
        

############################### Level 1 ######################################


class SepaHeader(XmlModel):
    _sort_order = ('sepa_header', 'message_id', 'creation_date_time',
                   'number_of_operations', 'checksum', 'initiating_party')
    
    def __init__(self):
        self.sepa_header = XmlField('GrpHrd')
        self.message_id = XmlField('MsgId')
        self.creation_date_time = XmlField('CreDtTm')
        self.number_of_operations = XmlField('NbOfTxs')
        self.checksum = XmlField('CtrlSum')
        self.initiating_party = GenericPhysicalLegalEntity('InitgPty')
        super(SepaHeader, self).__init__('GrpHrd', 'sepa_header')


class PaymentInformation(XmlModel):
    _sort_order = ('payment_information', 'payment_info_identifier',
                   'payment_method', 'batchbook', 'number_of_operations',
                   'checksum', 'payment_type_info', 'collection_date',
                   'creditor_account', 'creditor_agent', 'ultimate_creditor',
                   'charge_clausule', 'creditor_identifier',
                   'direct_debit_operation_info')
    
    def __init__(self):
        self.payment_information = XmlField('PmtInf')
        self.payment_info_identifier = XmlField('PmtInfId')
        self.payment_method = XmlField('PmntMtd')
        self.batchbook = XmlField('BtchBookg')
        self.number_of_operations = XmlField('NbOfTxs')
        self.checksum = XmlField('CtrlSum')
        self.payment_type_info = PaymentTypeInfo()
        self.collection_date = XmlField('ReqdColltnDt')
        self.creditor = NameAndAddress('Crdtr')
        self.creditor_account = BankAccount('CdtrAcct')
        self.creditor_agent = BankAgent('CdtrAgt')
        self.ultimate_creditor = GenericPhysicalLegalEntity('UltmtCdtr')
        self.charge_clausule = XmlField('ChrgBr')
        self.creditor_identifier = GenericPhysicalLegalEntity('CdtrSchmeId')
        self.direct_debit_operation_info = DirectDebitOperationInfo()        
        super(PaymentInformation, self).__init__('PmtInf',
                                                 'payment_information')


############################### Level 0 ######################################


class DirectDebitInitMessage(XmlModel):
    _sort_order = ('root', 'sepa_header', 'payment_information')
    
    def __init__(self):
        self.root = XmlField('CstmrDrctDbtInitn')
        self.sepa_header = SepaHeader()
        self.payment_information = PaymentInformation()
        super(DirectDebitInitMessage, self).__init__('CstmrDrctDbtInitn', 'root')
