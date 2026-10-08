from transmission_analyzer.analysis.shift_detector import ShiftDetector
from transmission_analyzer.data.mf4_reader import MF4Reader
from transmission_analyzer.models.shift_event import ShiftEvent


FILE_PATH = "demo_data/campaign_001/calibration_A/city_01.mf4"

class FakeSignal:
    def __init__(self, timestamps, samples):
        self.timestamps=timestamps
        self.samples=samples


def test_detect_shift():
    signal = FakeSignal(
        timestamps=[0.0, 0.1, 0.2, 0.3, 0.4],
        samples=[1, 1, 1, 2, 2]
    )

    detector = ShiftDetector()
    shifts= detector.detect(signal)

    assert shifts == [
        ShiftEvent(
            time=0.3,
            from_gear=1,
            to_gear=2,
            shift_type="upshift"
        )
    ]


def test_detect_multiple_shifts():
    signal = FakeSignal(
        timestamps=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        samples=[1, 1, 2, 2, 3, 3, 2]
    )

    detector = ShiftDetector()
    shifts = detector.detect(signal)

    assert shifts == [
        ShiftEvent(
            time=0.2,
            from_gear=1,
            to_gear=2,
            shift_type="upshift"
        ),
        ShiftEvent(
            time=0.4,
            from_gear=2,
            to_gear=3,
            shift_type="upshift"
        ),
        ShiftEvent(
            time=0.6,
            from_gear=3,
            to_gear=2,
            shift_type="downshift"
        )
    ]


def test_no_shift():
    signal = FakeSignal(
        timestamps= [0.0, 0.1, 0.2, 0.3],
        samples= [2, 2, 2, 2]
    )

    detector = ShiftDetector()
    shifts = detector.detect(signal)

    assert shifts == []


def test_detect_shift_from_mf4():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    gear_signal = reader.get_signal("CurrentGear")

    detector = ShiftDetector()
    shifts = detector.detect(gear_signal)

    assert len(shifts) > 0

    print(shifts)

def test_detect_skip_shift():
    signal = FakeSignal(
        timestamps=[0.0, 0.1, 0.2],
        samples=[1, 1, 3]
    )

    detector = ShiftDetector()
    shifts = detector.detect(signal)

    assert shifts == [
        ShiftEvent(
            time=0.2,
            from_gear=1,
            to_gear=3,
            shift_type="upshift"
        )
    ]