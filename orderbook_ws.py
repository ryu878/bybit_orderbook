from pybit.unified_trading import WebSocket
import time
import pandas as pd

# Manually select the Asset to trade
asset = input(' What Asset To Check? ')
asset = (asset+'USDT').upper()

ws = WebSocket(testnet=False, channel_type='linear')

'''
Linear & inverse:
Level 1 data, push frequency: 10ms
Level 50 data, push frequency: 20ms
Level 200 data, push frequency: 100ms
Level 500 data, push frequency: 100ms

'''

def handle_message(message):
    # Create DataFrames for bids and asks
    bids_df = pd.DataFrame(message['data']['b'], columns=['Price', 'Size']).astype({'Price': float, 'Size': int})
    asks_df = pd.DataFrame(message['data']['a'], columns=['Price', 'Size']).astype({'Price': float, 'Size': int})

    # Sort bids descending (highest price first) and asks ascending (lowest price first)
    bids_df = bids_df.sort_values('Price', ascending=False)
    asks_df = asks_df.sort_values('Price', ascending=False)

    # Calculate USD value (Price × Size)
    bids_df['Total USD'] = bids_df['Price'] * bids_df['Size']
    asks_df['Total USD'] = asks_df['Price'] * asks_df['Size']

    # Format the output
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.float_format', '{:.4f}'.format)

    usd_format = lambda x: '{:>12,.0f}'.format(x).replace(',', ' ')

    # Calculate padding to ensure total length = 30
    total_width = 30
    asset_len = len(asset)
    remaining_space = total_width - asset_len
    padding = remaining_space // 2

    # Print the order book
    header_line = ('=' * padding) + asset + ('=' * (remaining_space - padding))
    print(header_line)
    print(f'          Asks (Sells)')
    print('Price      Size      Total USD')
    print('='*30)
    print(asks_df.tail(10).to_string(index=False, header=False, formatters={
        'Price': '{:>8.7f}'.format,
        'Size': '{:>8}'.format,
        'Total USD': usd_format
    }))
    print(f'          Bids (Buys)')
    print('='*30)
    print(bids_df.head(10).to_string(index=False, header=False, formatters={
        'Price': '{:>8.7f}'.format,
        'Size': '{:>8}'.format,
        'Total USD': usd_format
    }))
    


ws.orderbook_stream(depth=50, symbol=asset, callback=handle_message)


while True:
    time.sleep(1)
