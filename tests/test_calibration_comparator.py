from transmission_analyzer.analysis.calibration_comparator import CalibrationComparator
from transmission_analyzer.data.mf4_reader import MF4Reader
from transmission_analyzer.analysis.shift_detector import ShiftDetector
from transmission_analyzer.analysis.kpi_engine import KPIEngine

import pytest


def test_compare_shift():

    shift_a = {
    "time": 5.0,
    "from_gear": 1,
    "to_gear": 2,
    "shift_type": "upshift",
    "vehicle_speed": 20.0,
    "rpm_change": -194.0,
    "throttle_position": 48.0,
    "engine_torque": 192.0
    }

    shift_b = {
        "time": 4.5,
        "from_gear": 1,
        "to_gear": 2,
        "shift_type": "upshift",
        "vehicle_speed": 18.0,
        "rpm_change": -180.0,
        "throttle_position": 48.0,
        "engine_torque": 188.0
    }

    comparator = CalibrationComparator()

    result = comparator.compare_shift(
        shift_a,
        shift_b
    )

    assert result["shift"] == "1 -> 2"
    assert result["time_difference"] == -0.5
    assert result["speed_difference"] == -2.0
    assert result["rpm_change_difference"] == 14.0
    assert result["throttle_difference"] == 0.0
    assert result["torque_difference"] == -4.0

def test_compare_multiple_shifts():

    shifts_a = [
        {
            "time": 5.0,
            "from_gear": 1,
            "to_gear": 2,
            "shift_type": "upshift",
            "vehicle_speed": 20.0,
            "rpm_change": -194.0,
            "throttle_position": 48.0,
            "engine_torque": 192.0
        },
        {
            "time": 10.0,
            "from_gear": 2,
            "to_gear": 3,
            "shift_type": "upshift",
            "vehicle_speed": 40.0,
            "rpm_change": -222.0,
            "throttle_position": 24.0,
            "engine_torque": 141.0
        }
    ]

    shifts_b = [
        {
            "time": 4.5,
            "from_gear": 1,
            "to_gear": 2,
            "shift_type": "upshift",
            "vehicle_speed": 18.0,
            "rpm_change": -180.0,
            "throttle_position": 48.0,
            "engine_torque": 188.0
        },
        {
            "time": 9.3,
            "from_gear": 2,
            "to_gear": 3,
            "shift_type": "upshift",
            "vehicle_speed": 37.0,
            "rpm_change": -190.0,
            "throttle_position": 30.0,
            "engine_torque": 150.0
        }
    ]

    comparator = CalibrationComparator()

    results = comparator.compare_shifts(
        shifts_a,
        shifts_b
    )

    assert len(results) == 2
    assert results[0]["shift"] == "1 -> 2"
    assert results[1]["shift"] == "2 -> 3"



FILE_PATH_A ="demo_data/campaign_001/calibration_A/city_01.mf4"
FILE_PATH_B ="demo_data/campaign_001/calibration_B/city_01.mf4"

def test_compare_calibration_a_vs_b_from_mf4():

    reader_a = MF4Reader(FILE_PATH_A)
    reader_a.open()

    reader_b = MF4Reader(FILE_PATH_B)
    reader_b.open()

    gear_a = reader_a.get_signal("CurrentGear")
    gear_b = reader_b.get_signal("CurrentGear")

    speed_a = reader_a.get_signal("VehicleSpeed")
    speed_b = reader_b.get_signal("VehicleSpeed")

    rpm_a = reader_a.get_signal("EngineSpeed")
    rpm_b = reader_b.get_signal("EngineSpeed")

    throttle_a = reader_a.get_signal("ThrottlePosition")
    throttle_b = reader_b.get_signal("ThrottlePosition")

    torque_a = reader_a.get_signal("EngineTorque")
    torque_b = reader_b.get_signal("EngineTorque")


    shift_detector = ShiftDetector()
    shift_a = shift_detector.detect(gear_a)
    shift_b = shift_detector.detect(gear_b)

    kpi_engine = KPIEngine()

    data_a = kpi_engine.analyze_shifts(shift_a, speed_a, rpm_a, throttle_a, torque_a)
    data_b = kpi_engine.analyze_shifts(shift_b, speed_b, rpm_b, throttle_b, torque_b)

    comparator = CalibrationComparator()

    results = comparator.compare_shifts(data_a, data_b)

    assert len(results) == 7

    for i in results:
        print(i)

def test_summarize_comparison():

    results = [
        {
            "time_difference": -0.5,
            "speed_difference": -2.0
        },
        {
            "time_difference": -0.7,
            "speed_difference": -3.0
        },
        {
            "time_difference": 1.0,
            "speed_difference": -2.5
        }
    ]

    comparator = CalibrationComparator()

    summary = comparator.summarize(results)

    assert summary["average_time_difference"] == pytest.approx(-0.0667, abs=0.001)
    assert summary["average_speed_difference"] == pytest.approx(-2.5)
    assert summary["earlier_shifts"] == 2
    assert summary["later_shifts"] == 1
    assert summary["same_time_shifts"] == 0



def test_summurize_on_mf4():
    reader_a = MF4Reader(FILE_PATH_A)
    reader_a.open()

    reader_b = MF4Reader(FILE_PATH_B)
    reader_b.open()

    gear_a = reader_a.get_signal("CurrentGear")
    speed_a = reader_a.get_signal("VehicleSpeed")
    rpm_a = reader_a.get_signal("EngineSpeed")
    torque_a = reader_a.get_signal("EngineTorque")
    throttle_a = reader_a.get_signal("ThrottlePosition")

    gear_b = reader_b.get_signal("CurrentGear")
    speed_b = reader_b.get_signal("VehicleSpeed")
    rpm_b = reader_b.get_signal("EngineSpeed")
    torque_b = reader_b.get_signal("EngineTorque")
    throttle_b = reader_b.get_signal("ThrottlePosition")


    detector = ShiftDetector()

    shifts_a = detector.detect(gear_a)
    shifts_b = detector.detect(gear_b)

    kpi_engine = KPIEngine()
    analysis_a = kpi_engine.analyze_shifts(shifts_a, speed_a, rpm_a, throttle_a, torque_a)
    analysis_b = kpi_engine.analyze_shifts(shifts_b, speed_b, rpm_b, throttle_b, torque_b)

    comparator = CalibrationComparator()

    results = comparator.compare_shifts(analysis_a, analysis_b)

    summury = comparator.build_report(results)

    assert len(summury) > 0

    for k, v in summury.items():
        print(k, ": ", v)