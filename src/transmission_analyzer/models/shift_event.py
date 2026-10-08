from dataclasses import dataclass

@dataclass
class ShiftEvent:
    time: float
    from_gear: int
    to_gear: int
    shift_type: str


    @property
    def gear_delta(self):
        return self.to_gear - self.from_gear

    @property
    def is_skip_shift(self):
        return abs(self.gear_delta) > 1


