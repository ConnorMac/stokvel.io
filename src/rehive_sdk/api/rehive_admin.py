from .api_base import APIList, APIEndpoint


class RehiveAdmin:

    def __init__(self, client):
        # Api Client instance
        self.client = client

        # Resources
        self.users = APIAdminUsers(self.client, 'admin/users/')
        self.currencies = APIAdminCurrencies(self.client, 'admin/currencies/')
        self.transactions = APIAdminTransactions(self.client, 'admin/transactions/')
        self.accounts = APIList(self.client, 'admin/accounts/')


class APIAdminCurrencies(APIList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminCurrencies, self).__init__(client, endpoint, filters)

    def create(self, code, description, symbol, unit, divisibility):
        data = {
            "code": code,
            "description": description,
            "symbol": symbol,
            "unit": unit,
            "divisibility": divisibility
        }
        response = self.post(data)
        return response


class APIAdminUsers(APIList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminUsers, self).__init__(client, endpoint, filters)

    def create(self, first_name, last_name, email, mobile_number):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "mobile_number": mobile_number
        }
        response = self.post(data)
        return response

    def get_emails(self):
        response = self.get('emails/')
        return response

    def create_email(self, user, email, primary, verified):
        data = {
            "user": user,
            "email": email,
            "primary": primary,
            "verified": verified
        }
        response = self.post(data, 'emails/')
        return response

    def get_mobiles(self):
        response = self.get('mobiles/')
        return response

    def create_mobile(self, user, number, primary, verified):
        data = {
            "user": user,
            "number": number,
            "primary": primary,
            "verified": verified
        }
        response = self.post(data, 'mobiles/')
        return response


class APIAdminTransactions(APIList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminTransactions, self).__init__(client, endpoint, filters)

    def get_totals(self):
        response = self.get('totals/')
        return response

    def create_credit(self, user, amount, currency, subtype, reference,
                      account, note, metadata=None,
                      confirm_on_create=False):
        data = {
            "subtype": user,
            "reference": reference,
            "amount": currency,
            "currency": currency,
            "account": amount,
            "note": note,
            "metadata": metadata,
            "user": user,
            "confirm_on_create": confirm_on_create
        }
        response = self.post(data, 'credit/')
        return response

    def create_debit(self, user, amount, currency, subtype, reference,
                     account, note, metadata=None,
                     confirm_on_create=False):
        data = {
            "subtype": subtype,
            "reference": reference,
            "amount": amount,
            "currency": currency,
            "account": amount,
            "note": note,
            "metadata": metadata,
            "user": user,
            "confirm_on_create": confirm_on_create
        }
        response = self.post(data, 'debit/')
        return response

    def create_transfer(self, user, currency, amount, recipient,
                        debit_account, debit_subtype, debit_metadata,
                        debit_note, debit_reference, credit_subtype,
                        credit_metadata, credit_note, credit_reference):
        data = {
            "debit_account": debit_account,
            "debit_subtype": debit_subtype,
            "debit_metadata": debit_metadata,
            "debit_note": debit_note,
            "debit_reference": debit_reference,
            "credit_subtype": credit_subtype,
            "credit_metadata": credit_metadata,
            "credit_note": credit_note,
            "credit_reference": credit_reference,
            "recipient": recipient,
            "amount": amount,
            "currency": currency,
            "user": user
        }
        response = self.post(data, 'transfer/')
        return response


class APIAdminCompany(APIEndpoint):
        def __init__(self, client, endpoint, filters=None):
            super(APIAdminCompany, self).__init__(client, endpoint, filters)

        def update(self, name, ):
            data = {
                "name": "",
                "description": "",
                "website": "",
                "logo": null,
                "password_reset_url": "",
                "email_confirmation_url": "",
                "default_currency": ""
            }
