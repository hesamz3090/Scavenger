#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from .request import Requests


class Perpetual(Requests):
    def __init__(self, access_id, secret_key):
        # Pass the access_id and secret_key to the parent class (RequestsClient)
        super().__init__(access_id, secret_key)

    def set_leverage(self, market, margin_mode, leverage):
        path = "/futures/adjust-position-leverage"
        url = f"{self.url}{path}"
        params = {
            'market': market,
            'market_type': 'FUTURES',
            'margin_mode': margin_mode,
            'leverage': leverage,
        }

        body = json.dumps(params)
        return self.request("POST", url, params=params, data=body)

    def get_balance(self):
        path = "/assets/futures/balance"
        url = f"{self.url}{path}"
        return self.request("GET", url, params={})

    def get_position(self, market):
        path = "/futures/pending-position"
        url = f"{self.url}{path}"
        params = {
            'market': market,
            'market_type': 'FUTURES',
        }

        body = json.dumps(params)
        return self.request("GET", url, params=params, data=body)

    def get_old_position(self, market=None):
        path = "/futures/finished-position"
        url = f"{self.url}{path}"
        params = {
            'market_type': 'FUTURES',
        }
        params.update(market=market) if market else None
        body = json.dumps(params)
        return self.request("GET", url, params=params, data=body)

    def set_order(self, market, side, amount, order_type='market', price=None, client_id=None, is_hide=None,
                  stp_mode=None):
        path = "/futures/order"
        url = f"{self.url}{path}"
        params = {
            'market': market,
            'side': side,
            'type': order_type,
            'amount': amount,
            'market_type': 'FUTURES',
            'price': price,
            'client_id': client_id,
            'is_hide': is_hide,
            'stp_mode': stp_mode,
        }

        body = json.dumps(params)
        return self.request("POST", url, params=params, data=body)

    def set_stop(self, market, price, order_type='latest_price'):
        path = "/futures/set-position-stop-loss"
        url = f"{self.url}{path}"
        params = {
            'market': market,
            'stop_loss_type': order_type,
            'stop_loss_price': price,
            'market_type': 'FUTURES',
        }

        body = json.dumps(params)
        return self.request("POST", url, params=params, data=body)

    def set_target(self, market, price, order_type='latest_price'):
        path = "/futures/set-position-take-profit"
        url = f"{self.url}{path}"
        params = {
            'market': market,
            'take_profit_type': order_type,
            'take_profit_price': price,
            'market_type': 'FUTURES',
        }

        body = json.dumps(params)
        return self.request("POST", url, params=params, data=body)

    def close_position(self, market, order_type='market'):
        path = "/futures/close-position"
        url = f"{self.url}{path}"
        params = {
            'market': market,
            'type': order_type,
            'market_type': 'FUTURES',
        }

        body = json.dumps(params)
        return self.request("POST", url, params=params, data=body)

    def get_price(self, market=None):
        path = "/futures/index"
        url = f"{self.url}{path}"
        params = {
            'market': market,
        }

        body = json.dumps(params)
        return self.request("GET", url, params=params, data=body)

    def get_depth(self, market, interval, limit=50):
        path = "/futures/depth"
        url = f"{self.url}{path}"
        params = {
            'market': market,
            'limit': limit,
            'interval': interval,
        }

        body = json.dumps(params)
        return self.request("GET", url, params=params, data=body)

    def get_market(self, market=None):
        path = "/futures/market"
        url = f"{self.url}{path}"
        params = {}
        params.update(market=market) if market else None

        body = json.dumps(params)
        return self.request("GET", url, params=[], data=body)
