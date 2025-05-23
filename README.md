# Real-Time Order Book Viewer for Bybit

This script connects to the Bybit WebSocket API and displays a live Level 50 order book for a user-specified asset. It uses the [`pybit`](https://github.com/verata-veratae/pybit) library to stream real-time bid/ask data and formats the output using `pandas`.

## Features

- Real-time order book data (Level 50 depth)
- Display of top 10 bids and asks
- Total USD value per order level
- Nicely formatted terminal output

## Requirements

- Python 3.7+
- `pybit`
- `pandas`

## Installation

```bash
pip install pybit pandas
```

## Run the script

```bash
python orderbook_ws.py
```
