
import numpy as np

class KPIEngine:
    
    
    def value_at_time(self, signal, time):
    
        if len(signal.timestamps) == 0:
            raise ValueError("cannot calculate KPI from an empty signal.")
    
        index = np.argmin(np.abs(signal.timestamps - time))
        return signal.samples[index]


    def vehicle_speed_at_shift(self, vehicule_speed_signal, shift_event):

        return self.value_at_time(
            vehicule_speed_signal,
            shift_event.time
        )


    def engine_speed_at_shift(self, engine_speed_signal, shift_event):
        return self.value_at_time(
            engine_speed_signal,
            shift_event.time
        )


    def rpm_change_around_shift(self, engine_speed_signal, shift_event, window=2.0):
        rpm_before = self.value_at_time(
            engine_speed_signal,
            shift_event.time - window
        )

        rpm_after = self.value_at_time(
            engine_speed_signal,
            shift_event.time + window
        )

        return rpm_after - rpm_before


    def throttle_at_shift(self, throttle_signal, shift_event):
        return self.value_at_time(
            throttle_signal,
            shift_event.time
        )

    def engine_torque_at_shift(self, torque_signal, shift_event):
        return self.value_at_time(
            torque_signal,
            shift_event.time
        )


    def analyze_shift(self, shift_event, vehicle_speed_signal, engine_speed_signal, throttle_signal, torque_signal):
        
        return {
            "time": shift_event.time,
            "from_gear": shift_event.from_gear,
            "to_gear": shift_event.to_gear,
            "shift_type": shift_event.shift_type,
            "vehicle_speed": float(self.vehicle_speed_at_shift(vehicle_speed_signal, shift_event)),
            "engine_speed": float(self.engine_speed_at_shift(engine_speed_signal, shift_event)),
            "throttle_position": float(self.throttle_at_shift(throttle_signal, shift_event)),
            "engine_torque": float(self.engine_speed_at_shift(torque_signal, shift_event)),
            "rpm_change": float(self.rpm_change_around_shift(engine_speed_signal, shift_event, window=0.2))
        }


    def analyze_shifts(self, shift_events, vehicle_speed_signal, engine_speed_signal, throttle_signal, torque_signal):

        results = []

        for shift_event in shift_events:
            analysis = self.analyze_shift(
                shift_event,
                vehicle_speed_signal,
                engine_speed_signal,
                throttle_signal,
                torque_signal
            )

            results.append(analysis)

        return results