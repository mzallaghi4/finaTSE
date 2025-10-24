# finaTSE
Python package to access Tehran Stock Exchange (TSE) data


# finaTSE

> Access **Tehran Stock Exchange (TSE)** market data in Python.

⚠️ **Unofficial** — scrapes [tsetmc.com](http://tsetmc.com). 
Not affiliated with TSE.

### Installation

```bash
pip install finaTSE


### Usage Example
```bash
from finaTSE import TSEClient

client = TSEClient()

# Real-time data
data = client.get_realtime_data("فملی")
print(data)

# Historical data (last 30 days)
df = client.get_history("فملی", days=30)
print(df.head())
