from transmission_analyzer.analysis.anomaly_detector import AnomalyDetector
from transmission_analyzer.data.mf4_reader import MF4Reader
from transmission_analyzer.analysis.shift_detector import ShiftDetector
from transmission_analyzer.analysis.kpi_engine import KPIEngine

def test_detect_unexpected_rpm_increase_during_upshift():

    shift_analysis = {
        "shift_type": "upshift",
        "rpm_change": 300.0
    }

    detector = AnomalyDetector()

    result = detector.has_unexpected_rpm_direction(
        shift_analysis
    )

    assert result is True


def test_normal_rpm_decrease_during_upshift():

    shift_analysis = {
        "shift_type": "upshift",
        "rpm_change": -200.0
    }

    detector = AnomalyDetector()

    result = detector.has_unexpected_rpm_direction(
        shift_analysis
    )

    assert result is False


def test_detect_unexpected_rpm_decrease_during_downshift():

    shift_analysis = {
        "shift_type": "downshift",
        "rpm_change": -250.0
    }

    detector = AnomalyDetector()

    result = detector.has_unexpected_rpm_direction(
        shift_analysis
    )

    assert result is True


def test_normal_rpm_increase_during_downshift():

    shift_analysis = {
        "shift_type": "downshift",
        "rpm_change": 200.0
    }

    detector = AnomalyDetector()

    result = detector.has_unexpected_rpm_direction(
        shift_analysis
    )

    assert result is False


def test_analyze_shift_with_unexpected_rpm():

    shift_analysis = {
        "shift_type": "upshift",
        "rpm_change": 300.0,
        "is_skip_shift": False
    }

    detector = AnomalyDetector()

    anomalies = detector.analyze_shift(shift_analysis)

    assert len(anomalies) == 1
    assert anomalies[0]["type"] == "unexpected_rpm_direction"


def test_analyze_shift_with_no_anomaly():

    shift_analysis = {
        "shift_type": "downshift",
        "rpm_change": 300.0,
        "is_skip_shift": False
    }

    detector = AnomalyDetector()

    anomalies = detector.analyze_shift(shift_analysis)

    assert anomalies == []


def test_skip_shift_detector():

    shift_analysis = {
        "shift_type": "upshift",
        "rpm_change": -200.0,
        "is_skip_shift": True
    }

    detector = AnomalyDetector()
    anomalies = detector.analyze_shift(shift_analysis)

    assert len(anomalies) == 1
    assert anomalies[0]["type"] == "skip_shift"

    print(anomalies)



def test_analyze_multiple_shifts():
    shift_anlyses = [
        {
            "shift_type": "upshift",
            "rpm_change": -200,
            "is_skip_shift": False
        },
        {
            "shift_type": "upshift",
            "rpm_change": 300,
            "is_skip_shift": False
        }
    ]


    detector = AnomalyDetector()

    results = detector.analyse_shifts(shift_anlyses)

    assert len(results) == 2
    assert results[0]["anomalies"] == []
    assert len(results[1]["anomalies"]) == 1

    for i in results:
        print(i)


FILE_PATH = "demo_data/campaign_001/calibration_A/city_01.mf4"

def test_anaomaly_detection_mf4():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    gear = reader.get_signal("CurrentGear")
    speed = reader.get_signal("VehicleSpeed")
    rpm = reader.get_signal("EngineSpeed")
    throttle = reader.get_signal("ThrottlePosition")
    torque = reader.get_signal("EngineTorque")


    shift_detector = ShiftDetector()
    shifts = shift_detector.detect(gear)

    kpi_engine = KPIEngine()
    analysis = kpi_engine.analyze_shifts(shifts, speed, rpm, throttle, torque)

    anomaly_detector = AnomalyDetector()
    results = anomaly_detector.analyse_shifts(analysis)

    assert len(results) > 0

    for i in results:
        print(i)


def test_multiple_anomalies_on_same_shift():

    shift_analysis = {
        "shift_type": "upshift",
        "rpm_change": 250.0,
        "is_skip_shift": True
    }

    detector = AnomalyDetector()

    anomalies = detector.analyze_shift(shift_analysis)

    assert len(anomalies) == 2
    assert anomalies[0]["type"] == "unexpected_rpm_direction"
    assert anomalies[1]["type"] == "skip_shift"

    for i in anomalies:
        print(i)


def test_detect_extreme_rpm_change():

    shift_analysis = {
        "shift_type": "upshift",
        "rpm_change": -1200.0,
        "is_skip_shift": False
    }

    detector = AnomalyDetector()

    anomalies = detector.analyze_shift(shift_analysis)

    assert len(anomalies) == 1
    assert anomalies[0]["type"] == "extreme_rpm_change"