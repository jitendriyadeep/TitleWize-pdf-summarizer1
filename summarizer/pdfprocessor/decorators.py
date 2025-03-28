# pdfprocessor/decorators.py
from django.contrib.auth.decorators import user_passes_test

def partner_required(view_func):
    return user_passes_test(
        lambda u: hasattr(u, 'legaluserprofile') and u.legaluserprofile.role == 'PARTNER',
        login_url='/accounts/login/'
    )(view_func)

def legal_staff_required(view_func):
    return user_passes_test(
        lambda u: hasattr(u, 'legaluserprofile') and u.legaluserprofile.role in ['PARTNER', 'ASSOCIATE'],
        login_url='/accounts/login/'
    )(view_func)