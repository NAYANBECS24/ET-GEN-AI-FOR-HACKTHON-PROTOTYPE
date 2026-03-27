from dataclasses import dataclass


@dataclass
class DecoyConfig:
    environment: str
    image: str
    port: int
