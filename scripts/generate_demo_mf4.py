from asammdf import MDF, Signal
import numpy as np

# create timestamp
timestamps = np.arange(0, 20, 0.1)


# create vehicle speed
vehicle_speed_values = np.linspace(0, 100, len(timestamps))

vehicle_speed = Signal(
    samples=vehicle_speed_values,
    timestamps=timestamps,
    name="VehicleSpeed",
    unit="km/h"
)


# create gear
gear_values = np.select(
    [
        vehicle_speed_values < 20,
        vehicle_speed_values < 40,
        vehicle_speed_values < 60,
        vehicle_speed_values < 80
    ],
    [1, 2, 3, 4], default=5
)

current_gear = Signal(
    samples=gear_values,
    timestamps=timestamps,
    name="CurrentGear",
    unit=""
)

# create RPM

engine_speed_values = (
    900 + (vehicle_speed_values * 35) - (gear_values * 250)
)

engine_speed = Signal(
    samples=engine_speed_values,
    timestamps=timestamps,
    name="EngineSpeed",
    unit="rpm"
)


mdf = MDF(version="4.10")
mdf.append([
    vehicle_speed,
    current_gear,
    engine_speed
])


mdf.save("demo_data/city_01.mf4", overwrite=True)

