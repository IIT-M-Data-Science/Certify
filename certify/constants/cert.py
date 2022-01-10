from enum import Enum


class CertType(Enum):
    PARTICIPATION = "Participation"
    EXCELLENCE = "Excellence"

    def __str__(self):
        return self.value


class CertTemplate(Enum):
    BASIC = "basic"

    def __str__(self):
        return self.value
