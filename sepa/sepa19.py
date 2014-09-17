# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField

"""
" More info and examples at http://www.iso20022.org/message_archive.page
"""

""" Classes ar sorted by:
" - Indentation level of its *first* reference in documentation
" - Order of reference in documentation
"""

MAX_NAME = 70

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


class OriginaldebtorAgent(XmlModel):
    _sort_order = ('original_debtor_agent', 'agent_identifier')

    def __init__(self):
        self.original_debtor_agent = XmlField('OrgnlDbtrAgt')
        self.agent_identifier = PhysicalLegalEntity('FinInstnId')
        super(OriginaldebtorAgent, self).__init__('OrgnlDbtrAgt',
                                                   'original_debtor_agent')


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
        self.scheme_name = SchemeName()
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
                   'original_creditor_id', 'original_debtor_account',
                   'original_debtor_agent')

    def __init__(self):
        self.modification_details = XmlField('AmdmntInfDtls')
        self.original_mandate_id = XmlField('OrgnlMndtId')
        self.original_creditor_id = GenericPhysicalLegalEntity('OrgnlMndtId')
        self.original_debtor_account = BankAccount('OrgnlDbtrAcct')
        self.original_debtor_agent = OriginaldebtorAgent()
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
        self.mandate_identifier = XmlField('MndtId')
        self.date_of_sign = XmlField('DtOfSgntr')
        self.modification_indicator = XmlField('AmdmntInd')
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
    _sort_order = ('structured_concept', 'creditor_reference')

    def __init__(self):
        self.structured_concept = XmlField('Strd')
        self.creditor_reference = CreditorGivenReference()
        super(StructuredConcept, self).__init__('CdtrRefInf',
                                                'structured_concept')

class Amount(XmlModel):
    _sort_order = ('amount', 'insted_amount')

    def __init__(self):
        self.amount = XmlField('Amt')
        self.insted_amount = XmlField('InstdAmt')
        super(Amount, self).__init__('Amt', 'amount')


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
    _sort_order = ('local_instrument', 'code')

    def __init__(self):
        self.local_instrument = XmlField('LclInstrm')
        self.code = XmlField('Cd')
        super(LocalInstrument, self).__init__('LclInstrm', 'local_instrument')


class CategoryPurpose(XmlModel):
    _sort_order = ('category_purpose', 'code')

    def __init__(self):
        self.category_purpose = XmlField('CtgyPurp')
        self.code = XmlField('Cd')
        self.propietary = XmlField('Prtry')
        super(CategoryPurpose, self).__init__('CtgyPurp', 'category_purpose')


class PostalAddress(XmlModel):
    _sort_order = ('postal_address', 'country', 'address_line_1', 'address_line_2')

    def __init__(self):
        self.postal_address = XmlField('PstlAdr')
        self.country = XmlField('Ctry')
        self.address_line_1 = XmlField('AdrLine')
        self.address_line_2 = XmlField('AdrLine')
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
    _sort_order = ('direct_debit_operation', 'mandate_information',
                   'creditor_identifier')

    def __init__(self):
        self.direct_debit_operation = XmlField('DrctDbtTx')
        self.mandate_information = MandateInformation()
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


class Reason(XmlModel):
    _sort_order = ('reason', 'code')

    def __init__(self):
        self.reason = XmlField('Rsn')
        self.code = XmlField('Cd')
        super(Reason, self).__ini__('Rsn', 'reason')


class OriginalOperationRef(XmlModel):
    _sort_order = ('original_operation_ref', 'amount', 'collection_date',
                    'creditor_identifier', 'payment_type_info', 'mandate_info',
                    'concept', 'ultimate_debtor', 'debtor', 'debtor_account',
                    'creditor', 'ultimate_creditor')

    def __init__(self):
        self.original_operation_ref = XmlField('OrgnlTxRef')
        self.amount = Amount() # TODO Im HERE
        self.collection_date = XmlField('ReqdColltnDt')
        self.creditor_identifier = GenericPhysicalLegalEntity('CdtrSchmeId')
        self.payment_type_info = PaymentTypeInfo()
        self.mandate_info = MandateInformation()
        self.concept = Concept()
        self.ultimate_debtor = GenericPhysicalLegalEntity('UltmDbtr')
        self.debtor = GenericPhysicalLegalEntity('Dbtr')
        self.debtor_account = BankAccount('DbtrAcct')
        self.creditor = GenericPhysicalLegalEntity('Cdtr')
        self.ultimate_creditor = GenericPhysicalLegalEntity('UltmCdtr')
        super(OriginalOperationRef, self).__init__('OrgnlTxRef',
                                                   'original_operation_ref')

############################### Level 2 ######################################


class GenericPhysicalLegalEntity(XmlModel):
    _sort_order = ('main_tag', 'entity_name', 'postal_address', 'identification')

    def __init__(self, tag):
        self.main_tag = XmlField(tag)
        self.entity_name = XmlField('Nm', rep=lambda x: x[:MAX_NAME])
        self.postal_address = PostalAddress()
        self.identification = GenericPhysicalLegalEntityId()
        super(GenericPhysicalLegalEntity, self).__init__(tag, 'main_tag')


class PaymentTypeInfo(XmlModel):
    _sort_order = ('payment_type_info', 'service_level', 'local_instrument',
                   'sequence_type', 'category_purpouse')

    def __init__(self):
        self.payment_type_info = XmlField('PmtTpInf')
        self.service_level = ServiceLevel()
        self.local_instrument = LocalInstrument()
        self.sequence_type = XmlField('SeqTp')
        self.category_purpouse = CategoryPurpose()
        super(PaymentTypeInfo, self).__init__('PmtTpInf', 'payment_type_info')


class NameAndAddress(XmlModel):
    _sort_order = ('main_tag', 'name_name', 'postal_address')

    def __init__(self, tag):
        self.main_tag = XmlField(tag)
        self.name_name = XmlField('Nm', rep=lambda x: x[:MAX_NAME])
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
    _sort_order = ('direct_debit_operation_info', 'payment_identifier',
                   'instructed_amount', 'charge_clausule',
                   'direct_debit_operation', 'ultimate_creditor',
                   'ultimate_creditor', 'debtor_agent', 'debtor',
                   'debtor_account', 'ultimate_debtor', 'purpose',
                   'regulatory_reglament', 'concept')

    def __init__(self):
        self.direct_debit_operation_info = XmlField('DrctDbtTxInf')
        self.payment_identifier = PaymentIdentifier()
        self.instructed_amount = XmlField('InstdAmt', attributes={'Ccy': ''})
        self.charge_clausule = XmlField('ChrgBr')
        self.direct_debit_operation = DirectDebitOperation()
        self.ultimate_creditor = GenericPhysicalLegalEntity('UltmtCdtr')
        self.debtor_agent = BankAgent('DbtrAgt')
        self.debtor = GenericPhysicalLegalEntity('Dbtr')
        self.debtor_account = BankAccount('DbtrAcct')
        self.ultimate_debtor = GenericPhysicalLegalEntity('UltmDbtr')
        self.purpose = Purpose()
        self.regulatory_reglament = RegulatoryInformation()
        self.concept = Concept()
        super(DirectDebitOperationInfo,
              self).__init__('DrctDbtTxInf', 'direct_debit_operation_info')

    def set_currency(self, ccy):
        self.instructed_amount.attributes.update({'Ccy': ccy})


class StatusReasonInfo(XmlModel):
    _sort_order = ('status_reason_info', 'originator', 'reason')

    def __init__(self):
        self.status_reason_info = XmlField('StsRsnInf')
        self.originator = GenericPhysicalLegalEntity('Orgtr')
        self.reason = Reason()
        super(StatusReasonInfo, self).__init__('StsRsnInf',
                                                      'status_reason_info')


class OperationStatusInfo(XmlModel):
    _sort_order = ('operation_status_info', 'status_id',
                   'original_insruction_id', 'original_end_to_end_id',
                   'operation_status', 'status_reason_info',
                   'original_operation_ref')

    def __init__(self):
        self.operation_status_info = XmlField('TxInfAndSts')
        self.status_id = XmlField('StsId')
        self.original_insruction_id = XmlField('OrgnlInstrId')
        self.original_end_to_end_id = XmlField('OrgnlEndToEndId')
        self.operation_status = XmlField('TxSts')
        self.status_reason_info = [] # StatusReasonInfo
        self.original_operation_ref = OriginalOperationRef()
        super(OperationStatusInfo, self).__init__('TxInfAndSts',
                                                  'operation_status_info')


############################### Level 1 ######################################


class SepaHeader(XmlModel):
    _sort_order = ('sepa_header', 'message_id', 'creation_date_time',
                   'number_of_operations', 'checksum', 'initiating_party',
                   'creditor_agent')

    def __init__(self):
        self.sepa_header = XmlField('GrpHdr')
        self.message_id = XmlField('MsgId')
        self.creation_date_time = XmlField('CreDtTm')
        self.number_of_operations = XmlField('NbOfTxs')
        self.checksum = XmlField('CtrlSum')
        self.initiating_party = GenericPhysicalLegalEntity('InitgPty')
        self.creditor_agent = BankAgent('CdtrAgt')
        super(SepaHeader, self).__init__('GrpHdr', 'sepa_header')


class PaymentInformation(XmlModel):
    _sort_order = ('payment_information', 'payment_info_identifier',
                   'payment_method', 'batchbook', 'number_of_operations',
                   'checksum', 'payment_type_info', 'collection_date',
                   'creditor', 'creditor_account', 'creditor_agent',
                   'ultimate_creditor', 'charge_clausule',
                   'creditor_identifier', 'direct_debit_operation_info')

    def __init__(self):
        self.payment_information = XmlField('PmtInf')
        self.payment_info_identifier = XmlField('PmtInfId') # Mandatory
        self.payment_method = XmlField('PmtMtd') # Mandatory
        self.batchbook = XmlField('BtchBookg')
        self.number_of_operations = XmlField('NbOfTxs')
        self.checksum = XmlField('CtrlSum')
        self.payment_type_info = PaymentTypeInfo()
        self.collection_date = XmlField('ReqdColltnDt') # Mandatory
        self.creditor = NameAndAddress('Cdtr') # Mandatory
        self.creditor_account = BankAccount('CdtrAcct') # Mandatory
        self.creditor_agent = BankAgent('CdtrAgt') # Mandatory
        self.ultimate_creditor = GenericPhysicalLegalEntity('UltmtCdtr')
        self.charge_clausule = XmlField('ChrgBr')
        self.creditor_identifier = GenericPhysicalLegalEntity('CdtrSchmeId')
        self.direct_debit_operation_info = [] # DirectDebitOperationInfo
        super(PaymentInformation, self).__init__('PmtInf',
                                                 'payment_information')


class OriginalGroupInfo(XmlModel):
    _sort_order = ('original_group_info', 'original_msg_id',
                   'original_msg_name_id', 'original_number_of_operations',
                   'original_checksum', 'group_state', 'status_reason_info')

    def __init__(self):
        self.original_group_info = XmlField('OrgnlGrpInfAndSts')
        self.original_msg_id = XmlField('OrgnlMsgId')
        self.original_msg_name_id = XmlField('OrgnlMsgNmId')
        self.original_number_of_operations = XmlField('OrgnlNbOfTxs')
        self.original_checksum = XmlField('OrgnlCtrlSum')
        self.group_state = XmlField('GrpSts')
        self.status_reason_info = [] # StatusReasonInfo
        super(OriginalGroupInfo, self).__init__('OrgnlGrpInfAndSts',
                                                'original_group_info')


class OriginalPaymentInfo(XmlModel):
    _sort_order = ('original_payment_info', 'original_payment_id',
                   'original_number_of_operations', 'original_checksum',
                   'payment_information_status', 'status_reason_info',
                   'operation_status_info')

    def __init__(self):
        self.original_payment_info = XmlField('OrgnlPmtInfAndSts')
        self.original_payment_id = XmlField('OrgnlPmtInfId')
        self.original_number_of_operations = XmlField('OrgnlNbOfTxs')
        self.original_checksum = XmlField('OrgnlCtrlSum')
        self.payment_information_status = XmlField('PmtInfSts')
        self.status_reason_info = [] # StatusReasonInfo
        self.operation_status_info = [] # OperationStatusInfo
        super(OriginalPaymentInfo, self).__init__('OrgnlPmtInfAndSts',
                                                  'original_payment_info')


############################### Level 0 ######################################


class DirectDebitInitMessage(XmlModel):
    ''' ISO 20222 - pain.008.001.02 '''
    _sort_order = ('root', 'sepa_header', 'payment_information')

    def __init__(self):
        self.root = XmlField('CstmrDrctDbtInitn')
        self.sepa_header = SepaHeader()
        self.payment_information = [] # PaymentInformation
        super(DirectDebitInitMessage, self).__init__('CstmrDrctDbtInitn',
                                                     'root')


############################### Level -1 #####################################

class DirectDebitInitDocument(XmlModel):
    _sort_order = ('root', 'customer_direct_debit')

    def __init__(self):
        xmlns = "urn:iso:std:iso:20022:tech:xsd:pain.008.001.02"
        xsi = "http://www.w3.org/2001/XMLSchema-instance"

        self.root = XmlField('Document', attributes={'xmlns': xmlns})
        self.customer_direct_debit = DirectDebitInitMessage()
        super(DirectDebitInitDocument, self).__init__('Document', 'root')

