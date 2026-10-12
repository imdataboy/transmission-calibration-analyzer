from transmission_analyzer.services.campaign_service import CampaignService


FILE_PATH = "demo_data/campaign_001/calibration_A/city_01.mf4"


def test_analyze_file():

    service = CampaignService()

    results = service.analyze_file(FILE_PATH)

    assert len(results) == 7

    for result in results:
        print(result)


def test_compare_files():

    service = CampaignService()

    result = service.compare_files(
        "demo_data/campaign_001/calibration_A/city_01.mf4",
        "demo_data/campaign_001/calibration_B/city_01.mf4"
    )

    assert len(result["comparisons"]) == 7
    assert "overall" in result["report"]
    assert "by_shift_type" in result["report"]

    print(result["report"])


def test_compare_campaigns():

    service = CampaignService()

    results = service.compare_campaigns(
        "demo_data/campaign_001/calibration_A",
        "demo_data/campaign_001/calibration_B"
    )

    assert len(results) == 3

    assert "city_01.mf4" in results
    assert "city_02.mf4" in results
    assert "highway_01.mf4" in results

    for filename, comparison in results.items():
        print("\n", filename)
        print(comparison["report"])


def test_compare_against_baseline():

    service = CampaignService()

    result = service.compare_against_baseline(
        "demo_data/campaign_001/calibration_A",
        {
            "calibration_B":
            "demo_data/campaign_001/calibration_B"
        }
    )

    assert "baseline" in result
    assert "comparisons" in result
    assert "calibration_B" in result["comparisons"]