class TransportStrategy:
    def calculate(self, distance: float, weight: float) -> float:
        pass

# Strategy pattern to determine transport method based on distance

class MiniVanStrategy(TransportStrategy):
    def calculate(self, distance: float, weight: float) -> float:
        return distance * weight * 3


class TruckStrategy(TransportStrategy):
    def calculate(self, distance: float, weight: float) -> float:
        return distance * weight * 2


class AeroplaneStrategy(TransportStrategy):
    def calculate(self, distance: float, weight: float) -> float:
        return distance * weight * 1
    
# We can easily add new strategies in the future without modifying existing code, adhering to the Open/Closed Principle.

# Factory method to get the appropriate transport strategy based on distance
def get_transport_strategy(distance: float) -> TransportStrategy:
    if distance > 500:
        return AeroplaneStrategy()
    elif distance > 100:
        return TruckStrategy()
    else:
        return MiniVanStrategy()