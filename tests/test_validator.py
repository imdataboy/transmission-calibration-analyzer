from transmission_analyzer.data.mf4_reader import MF4Reader
from transmission_analyzer.data.validator import MF4Validator

FILE_PATH = "demo_data/campaign_001/calibration_A/city_01.mf4"


def test_valid_file_hasno_missing_channels():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    validator = MF4Validator(reader)


    missing = validator.missing_channels()
    assert missing == []

def test_detects_missing_channels():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    validator = MF4Validator(reader)

    validator.REQUIRED_CHANNELS = [
        "VehicleSpeed",
        "CurrentGear",
        "FakeSignal"
    ]


    missing = validator.missing_channels()
    assert missing == ["FakeSignal"]


def test_is_valid_false():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    validator = MF4Validator(reader)

    validator.REQUIRED_CHANNELS = [
        "VehicleSpeed",
        "CurrentGear",
        "FakeSignal"
    ]

    assert validator.is_valid() is False

def test_is_valid_true():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    validator = MF4Validator(reader)

    assert validator.is_valid() is True


def test_no_empty_channels():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    validator = MF4Validator(reader)

    assert validator.empty_channels() == []


def test_detects_empty_channel():

    class FakeSignal:
        def __init__(self, samples):
            self.samples = samples

    class FakeReader:
        def list_channels(self):
            return ["VehicleSpeed", "CurrentGear"]

        def get_signal(self, channel_name):
            if channel_name == "VehicleSpeed":
                return FakeSignal([10, 20, 30])

            if channel_name == "CurrentGear":
                return FakeSignal([])

    reader = FakeReader()
    validator = MF4Validator(reader)

    validator.REQUIRED_CHANNELS = [
        "VehicleSpeed",
        "CurrentGear"
    ]

    assert validator.empty_channels() == ["CurrentGear"]


def test_is_valid_false_when_channel_empty():

    class FakeSignal:
        def __init__(self, samples):
            self.samples = samples

    class FakeReader:
        def list_channels(self):
            return ["VehicleSpeed", "CurrentGear"]

        def get_signal(self, channel_name):
            if channel_name == "VehicleSpeed":
                return FakeSignal([10, 20, 30])

            if channel_name == "CurrentGear":
                return FakeSignal([])

    reader = FakeReader()
    validator = MF4Validator(reader)

    validator.REQUIRED_CHANNELS = [
        "VehicleSpeed",
        "CurrentGear"
    ]

    assert validator.is_valid() is False


def test_validate_report_for_valid_file():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    validator = MF4Validator(reader)

    report = validator.validate()

    assert report == {
        "is_valid": True,
        "missing_channels": [],
        "empty_channels": []
    }

def test_validate_report_with_missing_channel():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    validator = MF4Validator(reader)

    validator.REQUIRED_CHANNELS = [
        "VehicleSpeed",
        "CurrentGear",
        "FakeSignal"
    ]

    report = validator.validate()

    assert report == {
        "is_valid": False,
        "missing_channels": ["FakeSignal"],
        "empty_channels": []
    }