from edc_identifier.simple_identifier import SimpleSequentialIdentifier
from edc_identifier.simple_identifier import SimpleUniqueIdentifier


class PurchaseOrderIdentifier(SimpleSequentialIdentifier):
    prefix = 'BHP'


class CreditCardPurchaseIdentifier(SimpleUniqueIdentifier):

    random_string_length = 5
    identifier_type = 'ccpid'
    template = 'CCP{device_id}{random_string}'


class PurchaseRequisitionIdentifier(SimpleUniqueIdentifier):
    random_string_length = 5
    identifier_type = 'prfid'
    template = 'PRF{device_id}{random_string}'


class VendorJustificationIdentifier(SimpleUniqueIdentifier):
    random_string_length = 4
    identifier_type = 'vjid'
    template = 'VJ{device_id}{random_string}'
