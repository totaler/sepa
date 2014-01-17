#SEPA library

This library allows you to build SEPA XML's using python objects

With this library you can build:

* ISO 20022 - pain.008.001.02 (Direct debit, no B2B)
* ISO 20022 - pain.001.001.03 (Credit transfer)

It depends on [libComXML](https://github.com/gisce/libComXML)

Below you can find a little example on how you should use this library

```python

	from sepa import sepa19

    def _sepa_header(self):
        
        header = sepa19.SepaHeader()
        header_fields = {
            'message_id': message_id,
            'creation_date_time': iso_today,
            'number_of_operations': num_operations,
            'checksum': total,
            'initiating_party': initiating_party
        }
        header.feed(header_fields)
        return header

	def _payments_info(self):
		'''builds payments info'''
		return payments_info

	def build_xml(self):

	    xml = sepa19.DirectDebitInitDocument()
	    direct_debit = sepa19.DirectDebitInitMessage()
	            
	    header = self._sepa_header()
	    payments_info = self._payments_info()
	            
	    direct_debit.feed({
	        'sepa_header': header,
	        'payment_information': payments_info
	    })
	    xml.feed({
	        'customer_direct_debit': direct_debit
	    })
	    
	    xml.pretty_print = True
	    xml.build_tree()
	    return str(xml)
```

