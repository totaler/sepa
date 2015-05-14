# -*- coding: utf-8 -*-

import datetime
import sepa19


DEFAULT_CURRENCY = 'EUR'


class _DirectDebitOperationMessage(object):

    def __init__(self, amount, end_to_end_identifier, mandate_identifier,
        mandate_date_of_sign, debtor_name, debtor_bic, debtor_iban, ccy=None,
        old_debtor_bic=None, old_debtor_iban=None):
        self.amount = amount
        self.end_to_end_identifier = end_to_end_identifier
        self.mandate_identifier = mandate_identifier
        self.mandate_date_of_sign = mandate_date_of_sign
        self.debtor_name = debtor_name
        self.debtor_bic = debtor_bic
        self.debtor_iban = debtor_iban
        self.ccy = ccy or DEFAULT_CURRENCY
        self.old_debtor_bic = old_debtor_bic
        self.old_debtor_iban = old_debtor_iban

    def has_mandate_modification(self):
        """
        If available, old_debtor_* attributes determines whether or not something
        has changed about the bank account.
        """
        return (
            self.old_debtor_bic and self.old_debtor_bic != self.debtor_bic
        ) or (
            self.old_debtor_iban and self.old_debtor_iban != self.debtor_iban
        )

    def get_xml_node(self):
        direct_debit_operation_info = sepa19.DirectDebitOperationInfo()
        direct_debit_operation_info.instructed_amount.value = self.amount
        direct_debit_operation_info.instructed_amount.attributes = {'Ccy': self.ccy}
        direct_debit_operation_info.payment_identifier.feed({
            'end_to_end_identifier': self.end_to_end_identifier,
        })

        mandate_information = {
            'mandate_identifier': self.mandate_identifier,
            'date_of_sign': self.mandate_date_of_sign.isoformat(),
        }

        # Manage a bank account change
        if self.has_mandate_modification():
            mandate_information['modification_indicator'] = 'true'
            modification_details = sepa19.ModificationDetails()
            # Did the bank change (based on BIC code)
            if self.old_debtor_bic[:4] != self.debtor_bic[:4]:
                modification_details.original_debtor_agent.agent_identifier.other.feed({
                    'identification': 'SMNDA',
                })
            else:
                modification_details.original_debtor_account.account_identification.feed({
                    'iban': self.old_debtor_iban,
                })
            mandate_information['modification_details'] = modification_details

        direct_debit_operation_info.direct_debit_operation.mandate_information.feed(mandate_information)

        direct_debit_operation_info.debtor_agent.agent_identifier.feed({
            'bic': self.debtor_bic,
        })
        direct_debit_operation_info.debtor.feed({
            'entity_name': self.debtor_name,
        })
        direct_debit_operation_info.debtor_account.account_identification.feed({
            'iban': self.debtor_iban,
        })
        return direct_debit_operation_info


class _DirectDebitBatchMessage(object):

    def __init__(self, payment_info_identifier, sequence_type, creditor_name,
        creditor_iban, creditor_bic, creditor_identifier):
        self.operations = []
        self.payment_info_identifier = payment_info_identifier
        self.creditor_name = creditor_name
        self.sequence_type = sequence_type
        self.creditor_iban = creditor_iban
        self.creditor_bic = creditor_bic
        self.creditor_identifier = creditor_identifier

    def get_checksum(self):
        return sum([operation.amount for operation in self.operations])

    def get_number_of_operations(self):
        return len(self.operations)

    def add_operation(self, amount, end_to_end_identifier, mandate_identifier,
        mandate_date_of_sign, debtor_name, debtor_bic, debtor_iban, ccy=None,
        old_debtor_bic=None, old_debtor_iban=None):
        operation = _DirectDebitOperationMessage(
            amount,
            end_to_end_identifier,
            mandate_identifier,
            mandate_date_of_sign,
            debtor_name,
            debtor_bic,
            debtor_iban,
            ccy,
            old_debtor_bic,
            old_debtor_iban)
        self.operations.append(operation)
        return operation

    def get_xml_node(self):

        if self.get_number_of_operations() == 0:
            return

        now = datetime.datetime.now()
        payment_information = sepa19.PaymentInformation()
        payment_information.feed({
            'payment_info_identifier': self.payment_info_identifier,
            'payment_method': 'DD',
            'number_of_operations': self.get_number_of_operations(),
            'checksum': self.get_checksum(),
            'collection_date': now.date().isoformat(), #BAD
        })
        payment_information.creditor.feed({
            'name_name': self.creditor_name,
        })
        payment_information.payment_type_info.feed({
            'sequence_type': self.sequence_type,
        })
        payment_information.payment_type_info.service_level.feed({
            'code': 'SEPA',
        })
        payment_information.payment_type_info.local_instrument.feed({
            'code': 'CORE',
        })
        payment_information.creditor_account.account_identification.feed({
            'iban': self.creditor_iban,
        })
        payment_information.creditor_agent.agent_identifier.feed({
            'bic': self.creditor_bic,
        })
        payment_information.creditor_identifier.identification.physical_person.other.feed({
            'identification': self.creditor_identifier,
        })
        payment_information.creditor_identifier.identification.physical_person.other.scheme_name.feed({
            'proprietary': 'SEPA',
        })

        for operation in self.operations:
            payment_information.direct_debit_operation_info.append(
                operation.get_xml_node())

        return payment_information


class DirectDebitMessage(object):
    """
    Use this class to generate a SEPA message for direct debits.
    """

    def __init__(self, entity_name, message_id):
        self.batches = []
        self.entity_name = entity_name
        self.message_id = message_id

    def get_checksum(self):
        return sum([batch.get_checksum() for batch in self.batches])

    def get_number_of_operations(self):
        return sum([batch.get_number_of_operations() for batch in self.batches])

    def add_batch(self, payment_info_identifier, sequence_type, creditor_name,
        creditor_iban, creditor_bic, creditor_identifier):
        batch = _DirectDebitBatchMessage(
            payment_info_identifier,
            sequence_type,
            creditor_name,
            creditor_iban,
            creditor_bic,
            creditor_identifier)
        self.batches.append(batch)
        return batch

    def get_xml(self):

        now = datetime.datetime.now()
        xml = sepa19.DirectDebitInitDocument()
        direct_debit = sepa19.DirectDebitInitMessage()

        # Header
        initiating_party = sepa19.GenericPhysicalLegalEntity('InitgPty')
        initiating_party.feed({'entity_name': self.entity_name})
        header = sepa19.SepaHeader()
        header_fields = {
            'message_id': self.message_id,
            'creation_date_time': now.isoformat(),
            'number_of_operations': self.get_number_of_operations(),
            'checksum': self.get_checksum(),
            'initiating_party': initiating_party,
        }
        header.feed(header_fields)
        direct_debit.feed({
            'sepa_header': header,
        })

        # Batch nodes
        for batch in self.batches:
            payment_information = batch.get_xml_node()
            direct_debit.payment_information.append(payment_information)

        xml.feed({
            'customer_direct_debit': direct_debit
        })
        xml.build_tree()
        return str(xml)
