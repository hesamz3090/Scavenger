from lib.perpetual import Perpetual
import numpy as np

access_id = ""  # Replace with your access id
secret_key = ""  # Replace with your secret key

market = 'TRXUSDT'
leverage = 5
amount_percent = 20

client = Perpetual(access_id, secret_key)
position = client.get_position(market)
if position['message'] == 'OK':
    if position['data']:
        print('Position Exist')
    else:
        data = client.get_depth(market, '0.001')

        asks = data['data']['depth']['asks']
        bids = data['data']['depth']['bids']

        asks_volumes = [float(x[1]) for x in asks]
        bids_volumes = [float(x[1]) for x in bids]

        median_asks_volume = np.median(asks_volumes)
        median_bids_volume = np.median(bids_volumes)

        asks_volume_sum = sum(asks_volumes)
        bids_volume_sum = sum(bids_volumes)
        market_pressure = (bids_volume_sum / (bids_volume_sum + asks_volume_sum)) * 100

        buy_confirm = (median_asks_volume < asks_volumes[0]) and (market_pressure > 55)
        sell_confirm = (median_bids_volume < bids_volumes[0]) and (market_pressure < 45)

        if buy_confirm or sell_confirm:

            now_price = float(client.get_price(market)['data'][0]['price'])
            asks_max_volume = max(asks_volumes)
            bids_max_volume = max(bids_volumes)
            asks_max_index = asks_volumes.index(asks_max_volume)
            bids_max_index = bids_volumes.index(bids_max_volume)
            if buy_confirm:
                side = 'buy'
                print('is in buy')
                stop_price = float(bids[bids_max_index][0])
                target_price = float(asks[asks_max_index][0])

                stop_percent = round(abs(100 * ((now_price - stop_price) / now_price)), 2)
                target_percent = round(abs(100 * ((target_price - now_price) / now_price)), 2)

                if stop_percent >= 0.4 and target_percent >= 0.4:
                    balance = round(float(client.get_balance()['data'][0]['available']), 2)
                    amount = (((balance / now_price) * amount_percent) / 100) * leverage
                    # change_leverage = client.set_leverage(market, 'isolated', leverage)
                    order = client.set_order(market, side, amount)
                    if order['message'] == 'OK':
                        stop_result = client.set_stop(market, stop_price)
                        if stop_result['message'] == 'OK':
                            target_result = client.set_target(market, target_price)
                            if target_result['message'] == 'OK':
                                print('Positions opened')
                        else:
                            print(order['message'])
                            client.close_position(market)
                    else:
                        print(order['message'])
                        client.close_position(market)
                else:
                    print('Less than one')

            else:
                side = 'sell'
                print('is in sell')
                stop_price = float(asks[asks_max_index][0])
                target_price = float(bids[bids_max_index][0])

                stop_percent = round(abs(100 * ((stop_price - now_price) / now_price)), 2)
                target_percent = round(abs(100 * ((now_price - target_price) / now_price)), 2)

                if stop_percent > 0.4 and target_percent > 0.4:
                    balance = round(float(client.get_balance()['data'][0]['available']), 2)
                    amount = (((balance / now_price) * amount_percent) / 100) * leverage
                    # change_leverage = client.set_leverage(market, 'isolated', leverage)
                    order = client.set_order(market, side, amount)
                    if order['message'] == 'OK':
                        stop_result = client.set_stop(market, stop_price)
                        if stop_result['message'] == 'OK':
                            target_result = client.set_target(market, target_price)
                            if target_result['message'] == 'OK':
                                print('Positions opened')
                        else:
                            client.close_position(market)
                    else:
                        client.close_position(market)
                else:
                    print('Low Stop/Target')

        else:
            print('Not enough volume')

else:
    print(position['message'])
