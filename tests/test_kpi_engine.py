from transmission_analyzer.analysis.kpi_engine import KPIEngine
from transmission_analyzer.models.shift_event import ShiftEvent
from transmission_analyzer.analysis.shift_detector import ShiftDetector
from transmission_analyzer.data.mf4_reader import MF4Reader

from asammdf import Signal
import numpy as np 
import pytest

def test_value_at_time():
    timestamps = np.array([9.9, 10.0, 10.1, 10.2])
    time = 10.08

    signal = Signal(
        samples = np.array([1000, 1100, 1200, 1300]),
        timestamps=timestamps,
        name="EngineSpeed"
    )

    kpi_engine = KPIEngine()
    value = kpi_engine.value_at_time(signal, time)

    assert value == 1200


def test_value_at_time_empty_signal():

    signal= Signal(
        samples=np.array([]),
        timestamps=np.array([]),
        name="EngineSpeed"
    )

    kpi_engine = KPIEngine()

    with pytest.raises(ValueError, match="cannot calculate KPI from an empty signal."):
        kpi_engine.value_at_time(signal, 10.0)



def test_vehicle_speed_at_shift():
    speed_signal = Signal(
        samples=np.array([20.0, 30.0, 40.0, 50.0]),
        timestamps= np.array([9.8, 9.9, 10.0, 10.1]),
        name="VehicleSpeed"
    )

    shift = ShiftEvent(
        time=10.0,
        from_gear=2,
        to_gear=2,
        shift_type="upshift"
    )

    kpi_engine = KPIEngine()

    speed = kpi_engine.vehicle_speed_at_shift(speed_signal, shift)

    assert speed == 40.0


def test_engine_speed_at_shift():
    engine_signal = Signal(
        samples=np.array([1800.0, 2000.0, 2200.0, 2400.0]),
        timestamps= np.array([9.8, 9.9, 10.0, 10.1]),
        name="EngineSpeed"
    )

    shift = ShiftEvent(
        time=10.0,
        from_gear=2,
        to_gear=2,
        shift_type="upshift"
    )

    kpi_engine = KPIEngine()

    engine_speed = kpi_engine.vehicle_speed_at_shift(engine_signal, shift)

    assert engine_speed == 2200.0


def test_rpm_change_around_shift():
    engine_signal = Signal(
            samples=np.array([2400.0, 2300.0, 2200.0, 2000.0, 1900]),
            timestamps= np.array([9.8, 9.9, 10.0, 10.1, 10.2]),
            name="EngineSpeed"
        )

    shift = ShiftEvent(
            time=10.0,
            from_gear=2,
            to_gear=3,
            shift_type="upshift"
        )


    kpi_engine = KPIEngine()

    rpm_chnage = kpi_engine.rpm_change_around_shift(engine_signal, shift, window=2.0)

    assert rpm_chnage == -500.0



def test_throttle_at_shift():
    throttle_signal = Signal(
                samples=np.array([20.0, 30.0, 45.0, 50.0]),
                timestamps= np.array([9.8, 9.9, 10.0, 10.1]),
                name="ThrottlePosition"
            )
    
    shift = ShiftEvent(
            time=10.0,
            from_gear=2,
            to_gear=3,
            shift_type="upshift"
        )


    kpi_engine = KPIEngine()

    throttle = kpi_engine.throttle_at_shift(throttle_signal, shift)

    assert throttle == 45.0



def test_analyze_shift():
    speed_signal = Signal(
        samples=np.array([20.0, 30.0, 40.0, 50.0]),
        timestamps= np.array([9.8, 9.9, 10.0, 10.1]),
        name="VehicleSpeed"
    )

    rpm = Signal(
        samples=np.array([1800.0, 2000.0, 2200.0, 2400.0, 2500.0]),
        timestamps= np.array([9.8, 9.9, 10.0, 10.1, 10.2]),
        name="EngineSpeed"
    )

    throttle = Signal(
        samples=np.array([20.0, 30.0, 45.0, 50.0]),
        timestamps= np.array([9.8, 9.9, 10.0, 10.1]),
        name="ThrottlePosition"
    )

    torque = Signal(
        samples=np.array([150.0, 170.0, 190.0, 210.0, 220.0]),
        timestamps=np.array([9.8, 9.9, 10.0, 10.1, 10.2]),
        name="EngineTorque"
    )

    shift = ShiftEvent(
        time=10.0,
        from_gear=2,
        to_gear=3,
        shift_type="upshift"
    )

    kpi_engine = KPIEngine()

    analysis = kpi_engine.analyze_shift(shift, speed_signal, rpm, throttle, torque)

    assert analysis == {
        "time": 10.0,
        "from_gear": 2,
        "to_gear": 3,
        "shift_type": "upshift",
        "is_skip_shift": False,
        "vehicle_speed": 40.0,
        "engine_speed": 2200.0,
        "throttle_position": 45.0,
        "engine_torque": 190.0,
        "rpm_change": 700.0
    }


FILE_PATH = "demo_data/campaign_001/calibration_A/city_01.mf4"

def test_analyze_shift_from_mf4():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    gear_signal = reader.get_signal("CurrentGear")
    speed_siganl = reader.get_signal("VehicleSpeed")
    rpm = reader.get_signal("EngineSpeed")
    throttle_signal = reader.get_signal("ThrottlePosition")
    torque = reader.get_signal("EngineTorque")

    detector = ShiftDetector()
    shift = detector.detect(gear_signal)

    first_shift = shift[0]

    kpi_engine = KPIEngine()

    analysis = kpi_engine.analyze_shift(
        first_shift,
        speed_siganl,
        rpm,
        throttle_signal,
        torque
    )

    print(analysis)


    assert analysis["time"] == 5.0
    assert analysis["from_gear"] == 1
    assert analysis["to_gear"] == 2
    assert analysis["shift_type"] == "upshift"
    assert analysis["vehicle_speed"] == 20.0
    assert analysis["engine_speed"] == 1100.0
    assert analysis["throttle_position"] == 48.0
    assert analysis["engine_torque"] == 192.0
    assert analysis["rpm_change"] == -194.0
    assert analysis["is_skip_shift"] is False


def test_analyze_all_shift_events():

    reader = MF4Reader(FILE_PATH)
    reader.open()

    gear = reader.get_signal("CurrentGear")
    speed = reader.get_signal("VehicleSpeed")
    rpm = reader.get_signal("EngineSpeed")
    throttle = reader.get_signal("ThrottlePosition")
    torque = reader.get_signal("EngineTorque")

    detector = ShiftDetector()
    shifts = detector.detect(gear)

    kpi_engine = KPIEngine()

    results = kpi_engine.analyze_shifts(shifts, speed, rpm, throttle, torque)

    assert len(results) == 7

    for r in results:
        print(r)


def test_engine_torque_at_shift():
    torque_signal = Signal(
        samples=np.array([150.0, 170.0, 190.0, 210.0]),
        timestamps=np.array([9.8, 9.9, 10.0, 10.1]),
        name="EngineTorque"
    )

    shift = ShiftEvent(
        time=10.0,
        from_gear=2,
        to_gear=3,
        shift_type="upshift"
    )

    kpi_engine = KPIEngine()

    torque = kpi_engine.engine_torque_at_shift(
        torque_signal,
        shift
    )

    assert torque == 190.0