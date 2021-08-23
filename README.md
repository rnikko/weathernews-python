# Weathernews Python Library

This library provides convenient access to Weathernews.jp data in Python

### Requirements

-   Python 3.8

## Usage

### Fetching forecast data

Forecast can be fetched by using a Location object or a string. Use a string to skip the Location search step.

```python
import weathernews

s = weathernews.Location.search("tokyo")
weathernews.Forecast.fetch(s[0])

weathernews.Forecast.fetch("tokyo")
```

### Location search

Location search is performed by entering a location name and a result is returned if found in Weathernews database.

```python
import weathernews

s = weathernews.Location.search("tokyo")
s[0]

# Location(lat=35.691667, lon=139.75, loc='東京', dist=0.415, v='7568ec9017b1ee619b719b2e27bb2222ff3533c3d047419f40d2980258c0a799', s=130, url='/onebox/35.691667/139.750000/q=%E6%9D%B1%E4%BA%AC&v=7568ec9017b1ee619b719b2e27bb2222ff3533c3d047419f40d2980258c0a799')
```
