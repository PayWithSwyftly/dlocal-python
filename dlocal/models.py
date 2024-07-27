from dataclasses import dataclass
from typing import Dict, Literal, Optional


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


@dataclass
class ChinaPayout(PayoutRequest):
    account_type: Optional[Literal["C", "S"]] = None
    country: Literal["CN"] = "CN"
    currency: Literal["CNY", "USD"]
    document_type: Optional[Literal["PASS", "TAXID"]] = None
    purpose: Optional[Literal["EPBTOB", "EPREMT"]] = None

    @property
    def valid_bank_acct(self):
        return len(self.bank_account) < 9 or len(self.bank_account) > 25

    @property
    def valid_bank_card(self):
        return len(self.bank_account) < 15 or len(self.bank_account) > 18

    @property
    def valid_han_beneficiary_name(self):
        return all("\u4e00" <= char <= "\u9fff" for char in self.beneficiary_name)

    def validate_required_fields(self):
        required_fields = [
            "login",
            "password",
            "external_id",
            "beneficiary_name",
            "country",
            "bank_branch",
            "bank_account",
            "currency",
            "amount",
            "phone",
            "document_id",
        ]

        for field in required_fields:
            value = getattr(self, field)
            if value is None or value == "":
                raise ValueError(f"{field} is required and cannot be empty")

        if len(self.bank_account) < 9 or len(self.bank_account) > 25:
            raise ValueError("bank_account must be between 9 and 25 digits")

        if self.currency not in ["CNY", "USD"]:
            raise ValueError("currency must be either 'CNY' or 'USD'")

        if self.country != "CN":
            raise ValueError("country must be 'CN'")

        if self.valid_bank_acct and self.account_type not in ["C", "S"]:
            raise ValueError("account_type must be 'C' or 'S' for non-card accounts")

        if self.document_type in ["PASS", "TAXID"] and not self.document_type:
            raise ValueError(
                "document_type is required when document type is PASS or TAXID"
            )

        if self.purpose in ["EPBTOB", "EPREMT"] and not self.purpose:
            raise ValueError(
                "purpose is required for Business to Business (B2B) and Remittance (P2P)"
            )

        if self.document_type != "PASS" and not self.valid_han_beneficiary_name:
            raise ValueError(
                "beneficiary_name must contain only Han characters when document_type is not PASS"
            )
