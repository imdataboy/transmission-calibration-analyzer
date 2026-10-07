import yaml

class SignalMapper:
    def __init__(self, config_path="config/default.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        if not config or "signals" not in config:
            raise ValueError(
                "Configuration must contain a 'signals' section."
            )

        self.signals = config["signals"]

    def get(self, name):
        if name not in self.signals:
            raise ValueError(
                f"Signal mapping '{name}' not found in configuration."
            )

        return self.signals[name]