from dataclasses import dataclass
from typing import Optional, Literal

from dlocal.models.base import PayoutRequest, BankCode


@dataclass
class ChinaPayout(PayoutRequest):
    bank_branch: str
    phone: str
    country: Literal["CN"] = "CN"
    currency: Literal["CNY", "USD"]
    document_type: Literal["PASS", "TAXID"]
    purpose: Literal["EPBTOB"] = "EPBTOB"
    account_type: Optional[Literal["C", "S"]] = None

    @property
    def valid_bank_acct(self):
        return 9 <= len(self.bank_account) <= 25

    @property
    def valid_bank_card(self):
        return 15 <= len(self.bank_account) <= 18

    @property
    def valid_han_beneficiary_name(self):
        return all("\u4e00" <= char <= "\u9fff" for char in self.beneficiary_name)

    def validate_china_specific_fields(self):
        if len(self.phone) > 100:
            raise ValueError("phone must be 100 chars or less")

        if not self.valid_bank_acct:
            raise ValueError("bank_account must be between 9 and 25 digits")

        if self.currency not in ["CNY", "USD"]:
            raise ValueError("currency must be either 'CNY' or 'USD'")

        if self.country != "CN":
            raise ValueError("country must be 'CN'")

        if not self.valid_bank_card and self.account_type not in ["C", "S"]:
            raise ValueError("account_type must be 'C' or 'S' for non-card accounts")

        if self.document_type not in ["PASS", "TAXID"]:
            raise ValueError("document_type must be either 'PASS' or 'TAXID'")

        if self.purpose != "EPBTOB":
            raise ValueError("purpose must be 'EPBTOB' for B2B transactions")

        if self.document_type != "PASS" and not self.valid_han_beneficiary_name:
            raise ValueError(
                "beneficiary_name must contain only Han characters when document_type is not PASS"
            )

        if self.document_type == "TAXID":
            if len(self.document_id) > 18:
                raise ValueError("document_id for TAXID must be 18 chars or less")
        elif len(self.document_id) > 100:
            raise ValueError("document_id must be 100 chars or less")

        if self.currency == "USD":
            if len(self.bank_branch) not in [8, 11]:
                raise ValueError(
                    "bank_branch (SWIFT code) must be 8 or 11 characters for USD transactions"
                )
            if not (self.bank_branch.isupper() and self.bank_branch.isalnum()):
                raise ValueError(
                    "bank_branch (SWIFT code) must be alphanumeric and uppercase"
                )

    def __post_init__(self):
        super().__post_init__()
        self.validate_china_specific_fields()

    def to_dict(self):
        base_dict = super().to_dict()
        china_specific = {
            "bank_branch": self.bank_branch,
            "account_type": self.account_type,
            "phone": self.phone,
        }
        return {**base_dict, **china_specific}


bank_codes = [
    BankCode("Agricultural Bank of China", "ABC", "103"),
    BankCode("Bank of Beijing", "BCCB", "792"),
    BankCode("Bank of China", "BOC", "001"),
    BankCode("Bank of Communications", "BOCOM", "301"),
    BankCode("Bank of Jiangsu", "JSCB", "795"),
    BankCode("Bank of Ningbo", "NBCB", "791"),
    BankCode("Bank of Shanghai", "BOS", "794"),
    BankCode("China Bohai Bank", "CBHB", "318"),
    BankCode("China CITIC Bank", "CITIC", "302"),
    BankCode("China Construction Bank", "CCB", "105"),
    BankCode("China Everbright Bank", "CEB", "303"),
    BankCode("China Guangfa Bank", "GDB", "789"),
    BankCode("China Merchants Bank", "CMB", "308"),
    BankCode("China Minsheng Bank", "CMBC", "305"),
    BankCode("China Zheshang Bank", "CZB", "316"),
    BankCode("Hengfeng Bank Co.", "HFB", "793"),
    BankCode("HSBC Bank", "HXB", "790"),
    BankCode("Industrial and Commercial Bank of China", "ICBC", "102"),
    BankCode("Industrial Bank Co., Ltd", "CIB", "309"),
    BankCode("Ping An Bank", "PINGAN", "788"),
    BankCode("Postal Savings Bank of China", "PSBC", "403"),
    BankCode("Shanghai Pudong Development Bank", "SPDB", "310"),
]
