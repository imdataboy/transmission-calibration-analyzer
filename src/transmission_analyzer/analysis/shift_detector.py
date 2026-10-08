from transmission_analyzer.models.shift_event import ShiftEvent

class ShiftDetector:
    def detect(self, gear_signal):
        shifts = []

        for i in range(1, len(gear_signal.samples)):
            previous_gear = gear_signal.samples[i - 1]
            current_gear = gear_signal.samples[i]

            if current_gear != previous_gear:
                if current_gear > previous_gear:
                    shift_type = "upshift"
                else:
                    shift_type = "downshift"

                shifts.append(
                    ShiftEvent(
                        time=float(gear_signal.timestamps[i]),
                        from_gear=int(previous_gear),
                        to_gear=int(current_gear),
                        shift_type=shift_type
                    )
                )

        return shifts