from transmission_analyzer.data.mf4_reader import MF4Reader

class MF4Validator:

    REQUIRED_CHANNELS = [
        "VehicleSpeed",
        "CurrentGear",
        "TargetGear",
        "EngineSpeed",
        "ThrottlePosition",
        "EngineTorque",
        "TransmissionInputSpeed",
        "TransmissionOutputSpeed",
    ]

    def __init__(self, reader:MF4Reader):
        self.reader = reader


    def missing_channels(self):
        avalable_channels = self.reader.list_channels()

        missing = []

        for c in self.REQUIRED_CHANNELS:
            if c not in avalable_channels:
                missing.append(c)

        return missing


    def is_valid(self):
        return not self.missing_channels() and not self.empty_channels()

    def empty_channels(self):
        avalable_channels = self.reader.list_channels()
        empty_chans = []

        for c in self.REQUIRED_CHANNELS:
            if c not in avalable_channels:
                continue
            signals = self.reader.get_signal(c)

            if len(signals.samples) == 0:
                empty_chans.append(c)

        return empty_chans

    def validate(self):
            return {
                "is_valid": self.is_valid(),
                "missing_channels": self.missing_channels(),
                "empty_channels": self.empty_channels()
            }

    
