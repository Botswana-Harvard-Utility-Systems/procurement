from edc_constants.constants import OTHER
from edc_list_data import PreloadData

list_data = {
    'procurement.costanalysis': [
        ('compares_favorable',
         ('The quoted price compares favorably to previous prices paid for the'
          ' same or similar items on payment voucher no. ______')),
        ('incorporates_discounts',
         ('The quoted price incorporate discounts not available to the general'
          ' public and reflect substantial savings.')),
        (OTHER, 'Other (i.e Cost Analysis for other considerations)')
    ],
}

preload_data = PreloadData(
    list_data=list_data)
