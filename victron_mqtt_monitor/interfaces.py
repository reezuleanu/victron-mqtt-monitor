from pydantic import BaseModel, field_validator


class Tree(dict):
    def add_to_tree(self, topic: str, value: any = None) -> None:
        parts = topic.split("/")
        current = self
        for part in parts[:-1]:
            if not current.get(part):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value


class BatteryInfo(BaseModel):
    """
    Args:
        soc (float): battery percentage
        power (float): battery watts being supplied
        current (float): battery amps being supplied
        voltage (float): battery volts being supplied
    """

    soc: float  # battery percentage
    power: float
    current: float
    voltage: float

    @property
    def percentage(self) -> float:
        return self.soc


class VictronStats(BaseModel):
    Batteries: list[BatteryInfo]

    @field_validator("Batteries", mode="before")
    def process_batteries(cls, v):
        if isinstance(v, dict) and "value" in v:
            return v["value"]
        else:
            return v
