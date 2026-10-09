

class AnomalyDetector:
    def has_unexpected_rpm_direction(self, shift_analysis):

        shift_type = shift_analysis["shift_type"]
        rpm_change = shift_analysis["rpm_change"]

        if shift_type == "upshift" and rpm_change > 0:
            return True

        if shift_type == "downshift" and rpm_change < 0:
            return True


        return False

    def has_extreme_rpm_change(self, shift_analysis, threshold=800.0):
        rpm_change = shift_analysis["rpm_change"]

        return abs(rpm_change)>threshold


    def analyze_shift(self, shift_analysis):

        anomalies = []

        if self.has_unexpected_rpm_direction(shift_analysis):
            anomalies.append({
                "type": "unexpected_rpm_direction",
                "message": "RPM changed in an unexpected direction for this shift"
            })

        if shift_analysis["is_skip_shift"]:
            anomalies.append({
                "type": "skip_shift",
                "message": "A non-sequential gear shift was detected."
            })


        if self.has_extreme_rpm_change(shift_analysis):
            anomalies.append({
                "type": "extreme_rpm_change",
                "message": "RPM change exeeded the configured threshold"
            })

        return anomalies

    def analyse_shifts(self, shift_anlyses):

        results = []

        for shift_analysis in shift_anlyses:
            anomalies = self.analyze_shift(shift_analysis)
            results.append(
                {
                    "shift": shift_analysis,
                    "anomalies": anomalies
                }
            )

        return results


