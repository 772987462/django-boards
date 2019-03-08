from django.test import TestCase
from ..forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form=SignUpForm()
        expected=['username','email','passward1','passward2',]
        actual=list(form.fields)
        self.assertSequenceEqual(expected,actual)