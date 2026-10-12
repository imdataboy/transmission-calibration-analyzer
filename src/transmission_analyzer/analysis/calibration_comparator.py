import numpy as np



class CalibrationComparator:
    def compare_shift(self, shift_a, shift_b):

        return {
            "shift": f"{shift_a['from_gear']} -> {shift_b['to_gear']}",
            "shift_type": shift_a["shift_type"],
            "time_difference": shift_b['time'] - shift_a['time'],
            "speed_difference": shift_b["vehicle_speed"] - shift_a["vehicle_speed"],
            "rpm_change_difference": shift_b["rpm_change"] - shift_a["rpm_change"],
            "throttle_difference": shift_b["throttle_position"] - shift_a["throttle_position"],
            "torque_difference": shift_b["engine_torque"] - shift_a["engine_torque"]
        }


    def compare_shifts(self, shift_a, shift_b):
        results = []
        for shift_a, shift_b in zip(shift_a, shift_b):
            comparison = self.compare_shift(shift_a, shift_b)

            results.append(comparison)

        return results

    def summarize(self, results):

        if not results:
            return {
                "average_time_difference": None,
                "average_speed_difference": None,
                "earlier_shifts": 0,
                "later_shifts": 0,
                "same_time_shifts": 0
            }

        average_time_difference = (
            sum(result["time_difference"] for result in results)
            / len(results)
        )

        average_speed_difference = (
            sum(result["speed_difference"] for result in results)
            / len(results)
        )

        earlier_shifts = sum(
            1 for result in results
            if result["time_difference"] < 0
        )

        later_shifts = sum(
            1 for r in results
            if r["time_difference"] > 0
        )

        same_time_shifts = sum(
            1 for r in results
            if r["time_difference"] == 0
        )

        return {
            "average_time_difference": average_time_difference,
            "average_speed_difference": average_speed_difference,
            "earlier_shifts": earlier_shifts,
            "later_shifts": later_shifts,
            "same_time_shifts": same_time_shifts
        }


    def summurize_by_shift_type(self, results):
        upshifts = [i for i in results if i["shift_type"] == "upshift"]
        downshifts = [i for i in results if i["shift_type"] == "downshift"]

        return {
            "upshift": self.summarize(upshifts),
            "downshift": self.summarize(downshifts)
        }


    def build_report(self, results):
        return {
            "overall": self.summarize(results),
            "by_shift_type": self.summurize_by_shift_type(results)
        }
        