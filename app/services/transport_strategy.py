class TransportStrategy:
    def calculate(self, distance: float, weight: float) -> float:
        pass


class MiniVanStrategy(TransportStrategy):
    def calculate(self, distance: float, weight: float) -> float:
        return distance * weight * 3


class TruckStrategy(TransportStrategy):
    def calculate(self, distance: float, weight: float) -> float:
        return distance * weight * 2


class AeroplaneStrategy(TransportStrategy):
    def calculate(self, distance: float, weight: float) -> float:
        return distance * weight * 1


def get_transport_strategy(distance: float) -> TransportStrategy:
    if distance > 500:
        return AeroplaneStrategy()
    elif distance > 100:
        return TruckStrategy()
    else:
        return MiniVanStrategy()