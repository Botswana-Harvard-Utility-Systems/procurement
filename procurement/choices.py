SPLIT = 'split'
SOLE = 'sole'

SUPPLIER_GROUP = (
    ('bwp_suppliers', 'BWP Suppliers'),
    ('zar_sppliers', 'ZAR Suppliers'),
    ('usd_suppliers', 'USD Suppliers'),
    ('eur_suppliers', 'EUR Suppliers')
)


CURRENCY = (
    ('zar', 'ZAR'),
    ('usd', 'USD'),
    ('eur', 'EUR')
)

DOC_STATUS = (
    ('new', 'New'),
    ('pending', 'Pending'),
    ('rejected', 'Rejected'),
    ('approved', 'Approved'),
)

NOT_LOWEST_BID = (
    ('selected_source',
     'Selected Source (alternative vendors exist, but vendor selection was based '
     'on a) technical requirements (eg. precision, reliability etc)) past performance'
     'of alternative vendors (poor service level, unavailability of parts etc).'),
    ('sole_source',
     'Sole Source (no other company is known to be capable of fully satisfying requirements)')
)

ALLOCATION_TYPE = (
    (SOLE, 'Sole'),
    (SPLIT, 'Split'),
)

REQUEST_REASON = (
    ('prf_approval', 'Purchase requisition approval'),
    ('confirm_funds', 'Confirm availability of funds'),
    ('po_auth_one', 'Purchase order authorisation (1)'),
    ('po_auth_two', 'Purchase order authorisation (2)'),
    ('invoice_auth', 'Invoice authorisation'),
)
