from .api_interface import ApiInterface


class Rehive:

    def __init__(self, token=None, connection_pool_size=0):
        # Leave token blank if logging in
        self.api = ApiInterface(token, connection_pool_size)

    # Get all endpoints
    def get_all_endpoints(self):
        response = self.api.get('')
        return self.api.get('')

    # AUTH CALL SECTION
    def register(self, data):
        response = self.api.post('auth/register/', data)
        return response

    def resgister_company(self, data):
        response = self.api.post('auth/company/register/', data)
        return response

    def login(self, data):
        response = self.api.post('auth/login/', data)
        return response

    def logout(self, data):
        response = self.api.post('auth/logout/', data)
        return response

    def logout_all(self, data):
        response = self.api.post('auth/logout/', data)
        return response

    def change_password(self, data):
        response = self.api.post('auth/password/change/', data)
        return response

    def reset_password(self, data):
        response = self.api.post('auth/password/reset/', data)
        return response

    def reset_password_confirm(self, data):
        response = self.api.post('auth/password/reset/confirm/', data)
        return response

    def resend_email_verification(self, data):
        response = self.api.post('/auth/email/verify/resend/', data)
        return response

    def resend_mobile_verification(self, data):
        response = self.api.post('/auth/mobile/verify/resend/', data)
        return response

    def verify_email(self, data):
        response = self.api.post('/auth/email/verify/', data)
        return response

    def verify_mobile(self, data):
        response = self.api.post('/auth/email/verify/', data)
        return response

    def get_tokens(self):
        response = self.api.get('/auth/tokens/')
        return response

    def create_permanent_token(self, data):
        response = self.api.post('/auth/tokens/', data)
        return response

    # ADMIN CALL SECTION

    def admin_get_transactions(self):
        response = self.api.get('/api/3/admin/transactions/')
        return response

    def admin_get_transactions_totals(self):
        response = self.api.get('/api/3/admin/transactions/totals/')
        return response

    def admin_create_admin_credit_transaction(self, data):
        response = self.api.post('/api/3/admin/transactions/credit/', data)
        return response

    def admin_create_admin_debit_transaction(self, data):
        response = self.api.post('/api/3/admin/transactions/debit/', data)
        return response

    def admin_create_admin_transfer_transaction(self, data):
        response = self.api.post('/api/3/admin/transactions/transfer/', data)
        return response

    def get_current_user(self):
        response = self.api.get('user/')
        return response
