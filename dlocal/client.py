import json
import os
from urllib import request
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from requests import Response, Session
from requests.exceptions import HTTPError

from dlocal.utils import generate_hmac_sha256_signature

load_dotenv()


class DLocalClient:
    def __init__(self, *args, **kwargs):
        self.live_domain = "https://api.dlocal.com"
        self.sandbox_domain = "https://sandbox.dlocal.com"

        self.login = os.getenv("DLOCAL_X_LOGIN") or kwargs.get("login")
        self.trans_key = os.getenv("DLOCAL_X_TRANS_KEY") or kwargs.get("trans_key")
        self.secret_key = os.getenv("DLOCAL_SECRET_KEY") or kwargs.get("secret_key")
        self.live_mode = (
            os.getenv("DLOCAL_LIVE_MODE") == "True" or kwargs.get("live_mode") or False
        )

        self.session = Session()

    @property
    def base_url(self) -> str:
        return self.live_domain if self.live_mode else self.sandbox_domain

    @property
    def external_id(self) -> str:
        return str(uuid.uuid4())

    @property
    def timestamp(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _generate_hmac_signature(self, payload: str) -> str:
        return generate_hmac_sha256_signature(payload, self.secret_key)

    def _parse_headers(self, data: Dict[str, Any]) -> Dict[str, str]:
        return {
            "X-Version": "2.1",
            "Content-Type": "application/json",
            "X-Date": self.timestamp,
            "X-Login": self.login,
            "X-Trans-Key": self.trans_key,
            "Authorization": self._generate_hmac_signature(json.dumps(data)),
        }

    def _parse_payload(self, data: dict):
        data |= {
            "login": self.login,
            "pass": self.trans_key,
            "external_id": self.external_id,
        }

        return data

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        timeout: int = 5,
    ) -> Dict[str, Any]:
        data = self._parse_payload(data) or {}

        request_params = {
            "method": method,
            "url": f"{self.base_url}/{endpoint}",
            "headers": self._parse_headers(data),
            "timeout": timeout,
        }

        if data:
            request_params["json"] = data

        try:
            response: Response = self.session.request(**request_params)
            response.raise_for_status()

            print(request_params)
            return response.json()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Better to use logging
            raise
        except Exception as err:
            print(f"Other error occurred: {err}")  # Better to use logging
            raise

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()


class DLocalExchangeRate(DLocalClient):
    def _parse_payload(self, data: dict):
        payload = super()._parse_payload(data)
        payload.pop("external_id")
        return payload

    def _parse_headers(self, data):
        return {"Content-Type": "application/json", "Accept": "application/json"}

    def get_exchange_rate(self, currency: str):
        endpoint = "api_curl/cashout_api/get_exchange_rate"
        payload = {"currency": currency}
        signature = self._generate_hmac_signature(json.dumps(payload))
        print(payload, signature)
        signed_payload = {"currency": currency, "control": signature}
        return self._make_request("POST", endpoint, signed_payload)
