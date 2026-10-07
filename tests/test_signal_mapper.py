from transmission_analyzer.data.signal_mapper import SignalMapper
import pytest

def test_get_engine_speed_mapping():
    mapper = SignalMapper()
    channel_name = mapper.get("engine_speed")

    assert channel_name == "EngineSpeed"

def test_multiple_signal_mappings():
    mapper = SignalMapper()

    assert mapper.get("vehicle_speed") == "VehicleSpeed"
    assert mapper.get("current_gear") == "CurrentGear"
    assert mapper.get("target_gear") == "TargetGear"
    assert mapper.get("engine_torque") == "EngineTorque"


def test_unknown_signal_mapping():
    mapper = SignalMapper()

    with pytest.raises(ValueError):
        mapper.get("fake_signal")


def test_custom_config(tmp_path):
    config_file = tmp_path / "custom.yaml"

    config_file.write_text(
        """
signals:
  engine_speed: N_Engine
  vehicle_speed: VehSpd
"""
    )

    mapper = SignalMapper(config_file)

    assert mapper.get("engine_speed") == "N_Engine"
    assert mapper.get("vehicle_speed") == "VehSpd"


def test_config_without_signals_section(tmp_path):
    config_file = tmp_path / "invalid.yaml"

    config_file.write_text(
        """
application:
  name: Transmission Analyzer
"""
    )

    with pytest.raises(ValueError):
        SignalMapper(config_file)

def test_empty_config(tmp_path):
    config_file = tmp_path / "empty.yaml"

    config_file.write_text("")

    with pytest.raises(ValueError):
        SignalMapper(config_file)

def test_missing_config_file():
    with pytest.raises(FileNotFoundError):
        SignalMapper("config/does_not_exist.yaml")