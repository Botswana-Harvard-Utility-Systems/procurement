from edc_identifier.simple_identifier import SimpleSequentialIdentifier
from edc_identifier.simple_identifier import SimpleUniqueIdentifier


class PurchaseOrderIdentifier(SimpleSequentialIdentifier):
    prefix = 'BHP'


class PurchaseRequisitionIdentifier(SimpleUniqueIdentifier):
    random_string_length = 8
    identifier_type = 'prfid'
    template = 'PRF{device_id}{random_string}'
