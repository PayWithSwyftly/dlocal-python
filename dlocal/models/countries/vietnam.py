from dataclasses import dataclass
from typing import Optional, Literal

from dlocal.models.base import PayoutRequest


@dataclass
class VietnamPayout(PayoutRequest):
    beneficiary_lastname: str
    country: Literal["VN"] = "VN"
    currency: Literal["VND", "USD"]
    bank_code: Optional[str] = None

    # Fields for wallet transfer
    account_type: Optional[Literal["MOMO", "VNPAY", "VNPT"]] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    def validate_vietnam_specific_fields(self):
        if len(self.beneficiary_name) > 50:
            raise ValueError("beneficiary_name must be 50 chars or less")

        if len(self.beneficiary_lastname) > 50:
            raise ValueError("beneficiary_lastname must be 50 chars or less")

        if self.currency not in ["VND", "USD"]:
            raise ValueError("currency must be either 'VND' or 'USD'")

        if self.country != "VN":
            raise ValueError("country must be 'VN'")

        # Validate bank transfer specific fields
        if self.bank_code:
            if len(self.bank_account) > 45:
                raise ValueError(
                    "bank_account must be 45 chars or less for bank transfers"
                )

        # Validate wallet transfer specific fields
        elif self.account_type:
            if self.account_type not in ["MOMO", "VNPAY", "VNPT"]:
                raise ValueError(
                    "account_type must be 'MOMO', 'VNPAY', or 'VNPT' for wallet transfers"
                )

            if not self.phone or len(self.phone) > 15:
                raise ValueError(
                    "phone is required and must be 15 chars or less for wallet transfers"
                )

            if not self.address or len(self.address) > 200:
                raise ValueError(
                    "address is required and must be 200 chars or less for wallet transfers"
                )

        else:
            raise ValueError("Either bank_code or account_type must be provided")

    def __post_init__(self):
        super().__post_init__()  # Call the base class validation
        self.validate_vietnam_specific_fields()

    def to_dict(self):
        base_dict = super().to_dict()
        vietnam_specific = {
            "beneficiary_lastname": self.beneficiary_lastname,
            "bank_code": self.bank_code,
            "account_type": self.account_type,
            "phone": self.phone,
            "address": self.address,
            "purpose": self.purpose,
        }
        return {**base_dict, **vietnam_specific}
