# finaTSE/client.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, Optional
from .exceptions import SymbolNotFoundError, NetworkError
from .utils import clean_number

TSETMC_SEARCH_URL = "http://tsetmc.com/tsev2/data/search.aspx?skey={symbol}"
TSETMC_HISTORY_URL = "http://tsetmc.com/tsev2/data/Export-txt.aspx?a=InsTrade&InsCode={ins_code}"
TSETMC_INFO_URL = "http://tsetmc.com/Loader.aspx?ParTree=151311&i={ins_code}"


class TSEClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "finaTSE/0.1 (https://github.com/mza/finaTSE)"
        })

    def _get_ins_code(self, symbol: str) -> str:
        """Get instrument code from symbol (e.g., 'فملی' or 'فولاد')."""
        url = TSETMC_SEARCH_URL.format(symbol=symbol.upper())
        try:
            resp = self.session.get(url, timeout=10)
        except requests.RequestException as e:
            raise NetworkError(f"Network error while searching symbol '{symbol}': {e}")

        if resp.status_code != 200:
            raise SymbolNotFoundError(f"Symbol '{symbol}' not found (HTTP {resp.status_code})")

        lines = resp.text.strip().split(";")
        if not lines[0]:
            raise SymbolNotFoundError(f"Symbol '{symbol}' not found in TSETMC database")

        parts = lines[0].split(",")
        if len(parts) < 3:
            raise SymbolNotFoundError(f"Invalid response format for symbol '{symbol}'")
        return parts[2]  # Instrument code

    def get_realtime(self, symbol: str) -> Dict:
        """Get real-time market data for a TSE symbol."""
        ins_code = self._get_ins_code(symbol)
        url = TSETMC_INFO_URL.format(ins_code=ins_code)

        try:
            resp = self.session.get(url, timeout=10)
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch real-time data for '{symbol}': {e}")

        if resp.status_code != 200:
            raise SymbolNotFoundError(f"Failed to load real-time page for '{symbol}'")

        soup = BeautifulSoup(resp.text, "html.parser")
        scripts = soup.find_all("script")
        data_vars = {}

        for script in scripts:
            if script.string and "var" in script.string and "InstrumentID" in script.string:
                lines = script.string.split(";")
                for line in lines:
                    if "var " in line and "=" in line:
                        try:
                            key, val = line.split("=", 1)
                            key = key.replace("var ", "").strip()
                            val = val.strip().strip('"')
                            data_vars[key] = val
                        except ValueError:
                            continue
                break

        last = clean_number(data_vars.get("PDrCotVal", "0"))
        close = clean_number(data_vars.get("PClosing", "0"))

        return {
            "symbol": symbol,
            "name": data_vars.get("LVal18AFC", ""),
            "last_price": last,
            "close_price": close,
            "open_price": clean_number(data_vars.get("POpen", "0")),
            "high_price": clean_number(data_vars.get("PHigh", "0")),
            "low_price": clean_number(data_vars.get("PLow", "0")),
            "volume": int(clean_number(data_vars.get("QTotTran5J", "0"))),
            "value": clean_number(data_vars.get("QTotCap", "0")),
            "change": last - close,
            "change_percent": ((last - close) / close * 100) if close != 0 else 0.0,
        }

    def get_history(self, symbol: str, days: Optional[int] = None) -> pd.DataFrame:
        """Get historical OHLCV data as a pandas DataFrame."""
        ins_code = self._get_ins_code(symbol)
        url = TSETMC_HISTORY_URL.format(ins_code=ins_code)

        try:
            resp = self.session.get(url, timeout=10)
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch history for '{symbol}': {e}")

        if resp.status_code != 200:
            raise SymbolNotFoundError(f"Failed to load historical data for '{symbol}'")

        lines = resp.text.strip().split("\n")
        records = []
        for line in lines[1:]:
            if not line.strip():
                continue
            cols = line.split(",")
            if len(cols) < 8:
                continue
            try:
                records.append({
                    "date": cols[0],
                    "high": clean_number(cols[1]),
                    "low": clean_number(cols[2]),
                    "open": clean_number(cols[3]),
                    "close": clean_number(cols[4]),
                    "volume": int(clean_number(cols[5])),
                    "value": clean_number(cols[6]),
                    "trades": int(cols[7]),
                })
            except (ValueError, IndexError):
                continue

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
        df = df.sort_values("date").reset_index(drop=True)

        if days and len(df) > days:
            df = df.tail(days)

        return df
