from transmission_analyzer.data.processed_data import ProcessedDataBuilder
from transmission_analyzer.services.campaign_service import CampaignService

import polars as pl

def test_shifts_to_dataframe():

    results = [
        {
            "shift": {
                "time": 5.0,
                "from_gear": 1,
                "to_gear": 2,
                "shift_type": "upshift",
                "is_skip_shift": False,
                "vehicle_speed": 20.0,
                "engine_speed": 1100.0,
                "throttle_position": 48.0,
                "engine_torque": 192.0,
                "rpm_change": -194.0
            },
            "anomalies": []
        }
    ]

    builder = ProcessedDataBuilder()

    df = builder.shifts_to_dataframe(results)

    assert df.height == 1
    assert df["from_gear"][0] == 1
    assert df["to_gear"][0] == 2
    assert df["anomaly_count"][0] == 0




def test_shifts_to_dataframe_from_mf4():

    service = CampaignService()

    results = service.analyze_file(
        "demo_data/campaign_001/calibration_A/city_01.mf4"
    )

    builder = ProcessedDataBuilder()

    df = builder.shifts_to_dataframe(results)

    assert df.height == 7
    assert "time" in df.columns
    assert "vehicle_speed" in df.columns
    assert "engine_torque" in df.columns
    assert "anomaly_count" in df.columns

    print(df)

def test_save_parquet(tmp_path):

    results = [
        {
            "shift": {
                "time": 5.0,
                "from_gear": 1,
                "to_gear": 2,
                "shift_type": "upshift",
                "is_skip_shift": False,
                "vehicle_speed": 20.0,
                "engine_speed": 1100.0,
                "throttle_position": 48.0,
                "engine_torque": 192.0,
                "rpm_change": -194.0
            },
            "anomalies": []
        }
    ]

    builder = ProcessedDataBuilder()

    df = builder.shifts_to_dataframe(results)

    output_path = tmp_path / "shifts.parquet"

    builder.save_parquet(
        df,
        output_path
    )

    assert output_path.exists()


def test_read_saved_parquet(tmp_path):

    results = [
        {
            "shift": {
                "time": 5.0,
                "from_gear": 1,
                "to_gear": 2,
                "shift_type": "upshift",
                "is_skip_shift": False,
                "vehicle_speed": 20.0,
                "engine_speed": 1100.0,
                "throttle_position": 48.0,
                "engine_torque": 192.0,
                "rpm_change": -194.0
            },
            "anomalies": []
        }
    ]

    builder = ProcessedDataBuilder()

    df = builder.shifts_to_dataframe(results)

    output_path = tmp_path / "shifts.parquet"

    builder.save_parquet(df, output_path)

    loaded_df = pl.read_parquet(output_path)

    assert loaded_df.height == 1
    assert loaded_df["from_gear"][0] == 1
    assert loaded_df["vehicle_speed"][0] == 20.0
    assert loaded_df["anomaly_count"][0] == 0


def test_build_and_save_from_mf4(tmp_path):

    service = CampaignService()

    results = service.analyze_file(
        "demo_data/campaign_001/calibration_A/city_01.mf4"
    )

    builder = ProcessedDataBuilder()

    output_path = tmp_path / "city_01.parquet"

    df = builder.build_and_save(
        results,
        output_path
    )

    assert output_path.exists()
    assert df.height == 7


def test_build_calibration(tmp_path):

    service = CampaignService()
    builder = ProcessedDataBuilder()

    output_dir = (
        tmp_path
        / "calibration_A"
    )

    files = builder.build_calibration(
        service,
        "demo_data/campaign_001/calibration_A",
        output_dir
    )

    assert len(files) == 3
    assert (
        output_dir / "city_01.parquet"
    ).exists()
    assert (
        output_dir / "city_02.parquet"
    ).exists()
    assert (
        output_dir / "highway_01.parquet"
    ).exists()


def test_build_campaign(tmp_path):

    service = CampaignService()
    builder = ProcessedDataBuilder()

    output_dir = tmp_path / "processed"

    result = builder.build_campaign(
        service,
        "demo_data/campaign_001",
        output_dir
    )

    assert "calibration_A" in result
    assert "calibration_B" in result

    assert len(result["calibration_A"]) == 3
    assert len(result["calibration_B"]) == 3