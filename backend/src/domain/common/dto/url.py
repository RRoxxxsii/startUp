from dataclasses import dataclass
from urllib.parse import urlencode


@dataclass(frozen=True)
class UrlPathDTO:
    domain: str
    scheme: str = None
    path: str = None
    query_params: dict = None

    @property
    def full_url(self) -> str:
        url = self.domain
        if self.query_params:
            query_string = urlencode(self.query_params)
            url += f'?{query_string}'
        return url
