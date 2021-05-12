from enum import Enum


class Exchange(Enum):
    BINANCE = {
        "commission": 0.01,
        "columns": ["Open_Time", "Open", "High", "Low", "Close", "Volume", "Close_Time", "Quote_Asset_Volume",
                    "Number_of_Trades", "Taker_Buy_Base_Asset_Volume", "Taker_Buy_Quote_Asset_Volume"],
        "datetime": "Open_Time"
    }
