from edc_form_validators import FormValidator


class VendorJustificationFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            'rejected',
            field='status',
            field_required='comment')
