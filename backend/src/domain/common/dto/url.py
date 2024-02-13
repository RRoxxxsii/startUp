from dataclasses import dataclass
from urllib.parse import urlencode


@dataclass
class UrlPathDTO:
    domain: str
    scheme: str = None
    path: str = ""
    query_params: dict = None

    @property
    def base_url(self) -> str:
        url = self.domain.rstrip("/")
        if self.path:
            url += f"{self.path}"
        return url

    @property
    def full_url(self) -> str:
        url = self.domain
        if self.query_params:
            query_string = urlencode(self.query_params)
            url += f"?{query_string}"
        return url
