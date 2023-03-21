import numpy as np
from typing import Dict, List
import pandas
import numpy
import statistics
import math
import typing

def rvi(prices):
    # Calculate the absolute difference between the current price and the previous price
    price_diff = np.abs(np.diff(prices))

    # Calculate the absolute difference between the current price and the previous price's moving average
    ma_diff = np.abs(prices[:-1] - prices[:-1].mean())

    # Calculate the RVI
    rvi = np.sqrt(np.sum(price_diff ** 2) / np.sum(ma_diff ** 2))

    return rvi


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Get the best bid and ask prices
                best_bid = max(order_depth.buy_orders.keys())
                best_ask = min(order_depth.sell_orders.keys())

                # Get the midpoint price of the order book
                midpoint_price = (best_bid + best_ask) / 2

                # Calculate the RVI with a lookback of 2 periods
                prices = list(order_depth.sell_orders.keys()) + list(order_depth.buy_orders.keys())
                rvi_val = rvi(prices[-2:])

                # Set the fair price based on the RVI
                if rvi_val > 0.5:
                    if best_bid > midpoint_price:
                        fair_price = best_bid
                    else:
                        fair_price = best_ask
                else:
                    fair_price = midpoint_price

                # Send a buy or sell order at the fair price
                order_volume = 100  # set the order volume
                if fair_price == best_bid:
                    print("BUY", str(-order_volume) + "x", fair_price)
                    orders.append(Order(product, fair_price, -order_volume))
                elif fair_price == best_ask:
                    print("SELL", str(order_volume) + "x", fair_price)
                    orders.append(Order(product, fair_price, order_volume))

                # Add all the above orders to the result dict
                result[product] = orders

        # Return the dict of orders
        return result
