import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import requests
from requests import Response, Session
from requests.exceptions import HTTPError

from dlocal.utils import generate_hmac_sha256_signature


class DLocalClient:
    def __init__(self, *args, **kwargs):
        self.live_domain = "https://api.dlocal.com/"
        self.sandbox_domain = "https://sandbox.dlocal.com/"

        self.live_mode = kwargs.get("trans_key") or False
        self.login = kwargs.get("login")
        self.trans_key = kwargs.get("trans_key")
        self.secret_key = kwargs.get("secret_key")

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

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        timeout: int = 5,
    ) -> Dict[str, Any]:
        data = data or {}
        data.update(
            {
                "login": self.login,
                "pass": self.trans_key,
                "external_id": self.external_id,
            }
        )

        try:
            response: Response = self.session.request(
                method,
                url=f"{self.base_url}/{endpoint}",
                headers=self._parse_headers(data),
                json=data,
                timeout=timeout,
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Better to use logging
            raise
        except Exception as err:
            print(f"Other error occurred: {err}")  # Better to use logging
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()
