#SEPA library

This library allows you to build SEPA XML's using Python

With this library you can build:

* ISO 20022 - pain.008.001.02 (Direct debit, no B2B)
* ISO 20022 - pain.001.001.03 (Credit transfer)

##Dependencies

* [libComXML](https://github.com/gisce/libComXML)

##Usage

```python
from sepa.helpers import DirectDebitMessage

# Creditor information
creditor_name = 'YOUR COMPANY NAME'
creditor_iban = 'FR123456789012345678901234'
creditor_bic = 'SWIFTCODE'
creditor_identifier = 'FR12ZZZ123456'

# Instantiate the message
direct_debit_message = DirectDebitMessage(
    creditor_name,
    'REF1234', # Reference of your choice
)

# Add a FRST transactions batch
batch = direct_debit_message.add_batch(
    'FRST1234', # Reference of your choice
    'FRST',
    creditor_name,
    creditor_iban,
    creditor_bic,
    creditor_identifier)

# Debtor information
debtor_name = 'John Doe'
debtor_bic = 'SWIFTCODE'
debtor_iban = 'FR123456789012345678909876'

# Insert a FRST transaction
operation = batch.add_operation(
    100,
    'REF2345', # Internal transaction reference
    '++SEPA.REF1234567890',
    datetime.date('2014', '04', '30'),
    debtor_name,
    debtor_bic,
    debtor_iban)

# Display the XML message
print direct_debit_message.get_xml()
```
