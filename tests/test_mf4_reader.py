from transmission_analyzer.data.mf4_reader import MF4Reader
import pytest

FILE_PATH = "demo_data/campaign_001/calibration_A/city_01.mf4"


def test_open_valid_mf4():
    reader = MF4Reader(FILE_PATH)
    reader.open()
    assert reader.mdf is not None


def test_list_channels():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    channels = reader.list_channels()

    assert "VehicleSpeed" in channels
    assert "EngineSpeed" in channels
    assert "CurrentGear" in channels

def test_get_signal():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    signal = reader.get_signal("EngineSpeed")

    assert signal.name == "EngineSpeed"
    assert signal.unit == "rpm"
    assert len(signal.samples) > 0


def test_missing_signal():
    reader = MF4Reader(FILE_PATH)
    reader.open()

    with pytest.raises(ValueError):
        reader.get_signal("FakeSignal")


def test_missing_file():
    reader = MF4Reader("does_not_exist.mf4")

    with pytest.raises(FileNotFoundError):
        reader.open()


def test_get_signal_before_open():
    reader = MF4Reader(FILE_PATH)

    with pytest.raises(RuntimeError):
        reader.get_signal("EngineSpeed")


def test_list_channels_before_open():
    reader = MF4Reader(FILE_PATH)

    with pytest.raises(RuntimeError):
        reader.list_channels()