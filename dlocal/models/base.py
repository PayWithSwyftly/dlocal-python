from dataclasses import dataclass
from dataclasses import field as f
from typing import Dict, Optional


@dataclass
class BankCode:
    bank_name: str
    abbreviation: str
    bank_code: int


@dataclass
class PayoutRequest:
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
    extra_info: Optional[Dict[str, any]] = f(default_factory=dict)

    def validate_base_fields(self):
        if len(self.login) > 32:
            raise ValueError("login must be 32 chars or less")

        if len(self.password) > 32:
            raise ValueError("password must be 32 chars or less")

        if len(self.external_id) > 100:
            raise ValueError("external_id must be 100 chars or less")

        if len(self.beneficiary_name) > 50:
            raise ValueError("beneficiary_name must be 50 chars or less")

        amount_parts = self.amount.split(".")
        if len(amount_parts) == 2 and len(amount_parts[1]) > 2:
            raise ValueError("amount can have max 2 decimal places")

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

    def __post_init__(self):
        self.validate_base_fields()
