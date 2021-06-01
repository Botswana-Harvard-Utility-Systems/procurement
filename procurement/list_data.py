from edc_constants.constants import OTHER
from edc_list_data import PreloadData

list_data = {
    'procurement.costanalysis': [
        ('compares_favorable',
         ('The quoted price compares favorably to previous prices paid')),
        ('incorporates_discounts',
         ('The quoted price incorporate discounts')),
        (OTHER, 'Other (i.e Cost Analysis for other considerations)')
    ],
}

preload_data = PreloadData(
    list_data=list_data)
