from enum import Enum


class Scope(Enum):
    ViewUserCert = "cert:view"
    ViewAllUserCert = "cert:view:all"
    CreateCert = "cert:create"
    EditCert = "cert:edit"
    
    def __str__(self):
        return str(self.value)

