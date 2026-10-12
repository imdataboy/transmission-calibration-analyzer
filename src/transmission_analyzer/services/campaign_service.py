from transmission_analyzer.data.mf4_reader import MF4Reader
from transmission_analyzer.data.validator import MF4Validator
from transmission_analyzer.data.signal_mapper import SignalMapper

from transmission_analyzer.analysis.shift_detector import ShiftDetector
from transmission_analyzer.analysis.kpi_engine import KPIEngine
from transmission_analyzer.analysis.anomaly_detector import AnomalyDetector
from transmission_analyzer.analysis.calibration_comparator import CalibrationComparator

from pathlib import Path

class CampaignService:

    def analyze_file(self, file_path):

        reader = MF4Reader(file_path)
        reader.open()

        validator = MF4Validator(reader)
        validation = validator.validate()

        if not validation["is_valid"]:
            raise ValueError(
                f"Invalid MF4 file: {validation}"
            )

        mapper = SignalMapper()

        gear = reader.get_signal(
            mapper.get("current_gear")
        )

        speed = reader.get_signal(
            mapper.get("vehicle_speed")
        )

        rpm = reader.get_signal(
            mapper.get("engine_speed")
        )

        throttle = reader.get_signal(
            mapper.get("throttle_position")
        )

        torque = reader.get_signal(
            mapper.get("engine_torque")
        )

        shift_detector = ShiftDetector()
        shifts = shift_detector.detect(gear)

        kpi_engine = KPIEngine()
        shift_analyses = kpi_engine.analyze_shifts(
            shifts,
            speed,
            rpm,
            throttle,
            torque
        )

        anomaly_detector = AnomalyDetector()
        results = anomaly_detector.analyse_shifts(
            shift_analyses
        )

        return results

    def compare_files(self, file_a, file_b):

        results_a = self.analyze_file(file_a)
        results_b = self.analyze_file(file_b)

        shifts_a = [
            result["shift"]
            for result in results_a
        ]

        shifts_b = [
            result["shift"]
            for result in results_b
        ]

        comparator = CalibrationComparator()

        comparisons = comparator.compare_shifts(
            shifts_a,
            shifts_b
        )

        report = comparator.build_report(comparisons)

        return {
            "comparisons": comparisons,
            "report": report
        }


    def compare_campaigns(self, calibration_a_dir, calibration_b_dir):

        calibration_a_dir = Path(calibration_a_dir)
        calibration_b_dir = Path(calibration_b_dir)

        files_a = {
            file.name: file
            for file in calibration_a_dir.glob("*.mf4")
        }

        files_b = {
            file.name: file
            for file in calibration_b_dir.glob("*.mf4")
        }

        common_files = sorted(
            set(files_a.keys()) & set(files_b.keys())
        )

        results = {}

        for filename in common_files:

            comparison = self.compare_files(
                files_a[filename],
                files_b[filename]
            )

            results[filename] = comparison

        return results

    
    def compare_against_baseline(self, baseline_dir, candidate_dirs):

        results = {}

        for candidate_name, candidate_dir in candidate_dirs.items():

            comparison = self.compare_campaigns(
                baseline_dir,
                candidate_dir
            )

            results[candidate_name] = comparison

        return {
            "baseline": str(baseline_dir),
            "comparisons": results
        }