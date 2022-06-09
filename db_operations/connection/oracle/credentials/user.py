from strenum import StrEnum


class QaUser(StrEnum):
    USERNAME = "sch_dmall"
    PASSWORD = "sch_dmall123",
    DSN = "QA_N11"


class TestUser(StrEnum):
    USERNAME = "sch_dmall"
    PASSWORD = "dmalltest",
    DSN = "TEST_N11"


class StUser(StrEnum):
    USERNAME = "USR_DMALL_ATM_TEST"
    PASSWORD = "qwzA123*",
    DSN = "ST_N11"
