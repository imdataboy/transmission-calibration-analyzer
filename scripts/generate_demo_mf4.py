from asammdf import MDF, Signal
import numpy as np
from pathlib import Path

def gen_speed_profile(ts, scenario, run_id):
        if scenario == "city":
            if run_id == 1:
                speeds = [0, 40, 40, 10, 0, 50, 50, 30]

            elif run_id == 2:
                speeds = [0, 35, 45, 15, 0, 45, 55, 25]

            else:
                raise ValueError(f"unknown run_id: {run_id}")
            speed = np.interp(
                ts,
                [0, 10, 20, 30, 35, 45, 55, 60],
                speeds
            )

        elif scenario == "highway":
            speed = np. interp(
                ts,
                [0, 15, 25, 45, 60],
                [0, 100, 120, 120, 90]
            )


        else:
            raise ValueError(
                f"unknown scenario: {scenario}"
            )

        return speed

def generate_test(
    output_path: str,
    scenario: str,
    calibration: str,
    run_id: int,
    duration: float = 60.0,
    sample_rate: float = 10.0
):
    # 1. Create timestamps
    dt = 1.0 / sample_rate
    timestamps = np.arange(0, duration, dt)

    print(f"duration: {duration} s")
    print(f"sample rate: {sample_rate} Hz")
    print(f"samples: {len(timestamps)}")



    # 2. Create vehicle speed
    vehicle_speed_values = gen_speed_profile(
        timestamps,
        scenario,
        run_id
    )

    speed_change = np.gradient(
        vehicle_speed_values, timestamps
    )

    throttle_values = np.clip(
        speed_change *12, 0, 100
    )

    throttle_position = Signal(
        samples=throttle_values,
        timestamps=timestamps,
        name="ThrottlePosition",
        unit="%"
    )


    vehicle_speed = Signal(
        samples=vehicle_speed_values,
        timestamps=timestamps,
        name="VehicleSpeed",
        unit="km/h"
    )


    # 3. Create gear
    if calibration == "a":
        gear_thresholds = [20, 40, 60, 80]

    elif calibration == "b":
        gear_thresholds = [18, 37, 57, 77]

    else:
        raise ValueError(f"unknow calibration: {calibration}")
    
    gear_values = np.select(
        [
            vehicle_speed_values < gear_thresholds[0],
            vehicle_speed_values < gear_thresholds[1],
            vehicle_speed_values < gear_thresholds[2],
            vehicle_speed_values < gear_thresholds[3],
        ],
        [1, 2, 3, 4],
        default=5
    )

    current_gear = Signal(
        samples=gear_values,
        timestamps=timestamps,
        name="CurrentGear",
        unit=""
    )

    shift_lead_seconds = 0.3
    lead_samples = int(shift_lead_seconds * sample_rate)

    target_gear_values = np.roll(
        gear_values, -lead_samples
    )

    target_gear_values[-lead_samples:] = gear_values[-1]

    target_gear = Signal(
        samples=target_gear_values,
        timestamps=timestamps,
        name="TargetGear",
        unit=""
    )


    # 4. Create engine RPM
    engine_speed_values = (
        900
        + vehicle_speed_values * 35
        - gear_values * 250
    )

    engine_speed = Signal(
        samples=engine_speed_values,
        timestamps=timestamps,
        name="EngineSpeed",
        unit="rpm"
    )

    engine_torque_values = (50 + (throttle_values * 2.5) + (engine_speed_values*0.02))

    engine_torque = Signal(
        samples=engine_torque_values,
        timestamps=timestamps,
        name="EngineTorque",
        unit="Nm"
    )

    transmission_output_speed_values = vehicle_speed_values * 35

    transmission_output_speed = Signal(
        samples=transmission_output_speed_values,
        timestamps=timestamps,
        name="TransmissionOutputSpeed",
        unit="rpm"
    )

    gear_rations = np.array([
        0.0,
        3.50, # gear 1
        2.10, # gear 2
        1.40, # gear 3
        1.00, # gear 4
        0.80, # gear 5
    ])

    transmission_input_speed_values = transmission_output_speed_values * gear_rations[gear_values]
    transmission_input_speed = Signal(
        samples=transmission_input_speed_values,
        timestamps=timestamps,
        name="TransmissionInputSpeed",
        unit="rpm"
    )


    # 5. Create MDF
    mdf = MDF(version="4.10")

    mdf.append([
        vehicle_speed,
        current_gear,
        target_gear,
        engine_speed,
        throttle_position,
        engine_torque,
        transmission_output_speed,
        transmission_input_speed
    ])


    # 6. Save wherever the caller requested
    mdf.save(
        output_path,
        overwrite=True
    )

    print(f"created: {output_path}")


if __name__ == "__main__":

    vehiclesTestRuns = [
        ("calibration_A", "city_01.mf4", "city", "a", 1),
        ("calibration_A", "city_02.mf4", "city", "a", 2),
        ("calibration_A", "highway_01.mf4", "highway", "a", 1),

        ("calibration_B", "city_01.mf4", "city", "b", 1),
        ("calibration_B", "city_02.mf4", "city", "b", 2),
        ("calibration_B", "highway_01.mf4", "highway", "b", 1),

    ]


    for folder, fname, scenario, calibration, run_id in vehiclesTestRuns:
        output_path = Path("demo_data") / "campaign_001" / folder / fname
        output_path.parent.mkdir(parents=True, exist_ok=True)

        generate_test(
            output_path=str(output_path),
            scenario=scenario,
            calibration=calibration,
            run_id=run_id
        )