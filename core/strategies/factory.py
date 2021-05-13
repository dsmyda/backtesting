from core.strategies import MacdCross, SmaCross

factory = {
    'macdcross': MacdCross,
    'smacross': SmaCross
}


def create(name: str):
    return factory[name]
