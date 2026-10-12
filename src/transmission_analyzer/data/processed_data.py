import polars as pl
from pathlib import Path


class ProcessedDataBuilder:

    def shifts_to_dataframe(self, results):

        rows = []

        for result in results:

            shift = result["shift"]

            rows.append({
                "time": shift["time"],
                "from_gear": shift["from_gear"],
                "to_gear": shift["to_gear"],
                "shift_type": shift["shift_type"],
                "is_skip_shift": shift["is_skip_shift"],
                "vehicle_speed": shift["vehicle_speed"],
                "engine_speed": shift["engine_speed"],
                "throttle_position": shift["throttle_position"],
                "engine_torque": shift["engine_torque"],
                "rpm_change": shift["rpm_change"],
                "anomaly_count": len(result["anomalies"])
            })

        return pl.DataFrame(rows)


    def save_parquet(self, df, output_path):
        df.write_parquet(output_path)


    def build_and_save(self, results, output_path):

        df = self.shifts_to_dataframe(results)

        self.save_parquet(
            df,
            output_path
        )

        return df

    def build_calibration(self, service, calibration_dir, output_dir):
        calibration_dir = Path(calibration_dir)
        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        created_files = []

        for mf4_file in sorted(
            calibration_dir.glob("*.mf4")
        ):
            results = service.analyze_file(
                mf4_file
            )

            output_path = (
                output_dir
                / f"{mf4_file.stem}.parquet"
            )

            self.build_and_save(
                results,
                output_path
            )

            created_files.append(
                output_path
            )

        return created_files


    def build_campaign(self, service, campaign_dir, output_dir):
        campaign_dir = Path(campaign_dir)
        output_dir = Path(output_dir)

        created = {}

        for calibration_dir in sorted(
            path for path in campaign_dir.iterdir()
            if path.is_dir()
        ):
            calibration_output = (
                output_dir / calibration_dir.name
            )

            files = self.build_calibration(
                service,
                calibration_dir,
                calibration_output
            )

            created[calibration_dir.name] = files

        return created