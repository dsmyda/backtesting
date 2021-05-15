from core.strategies import MACD, RSI

factory = {
    'macd': MACD,
    'rsi': RSI
}


def create(name: str):
    return factory[name]
