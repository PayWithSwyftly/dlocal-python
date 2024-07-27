from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class CashoutRequest:
    version: str
    purpose: str
    external_id: str
    document_id: str
    document_type: str
    beneficiary_name: str
    beneficiary_lastname: str
    country: str
    bank_name: str
    bank_account: str
    amount: str
    address: str
    currency: str
    email: str
    notification_url: str
    login: str
    password: str
    extra_info: Optional[Dict[str, any]] = None

    def to_dict(self):
        return {
            "version": self.version,
            "purpose": self.purpose,
            "external_id": self.external_id,
            "document_id": self.document_id,
            "document_type": self.document_type,
            "beneficiary_name": self.beneficiary_name,
            "beneficiary_lastname": self.beneficiary_lastname,
            "country": self.country,
            "bank_name": self.bank_name,
            "bank_account": self.bank_account,
            "amount": self.amount,
            "address": self.address,
            "currency": self.currency,
            "email": self.email,
            "notification_url": self.notification_url,
            "login": self.login,
            "pass": self.password,
            "extra_info": self.extra_info,
        }
