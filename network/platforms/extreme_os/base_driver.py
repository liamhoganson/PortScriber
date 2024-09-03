from scrapli.driver.network.base_driver import PrivilegeLevel

PRIVS = {
    "privilege_exec": (
        PrivilegeLevel(
            pattern=r"^rtr\.[\w-]+\.\d+\s#\s*$",
            name="privilege_exec",
            previous_priv="",
            deescalate="",
            escalate="",
            escalate_auth=False,
            escalate_prompt="",
        )
    ),
    "configuration": (
        PrivilegeLevel(
            pattern=r"^rtr\.[\w-]+\.\d+\s#\s*$",
            name="configuration",
            previous_priv="privilege_exec",
            deescalate="exit",
            escalate="configure",
            escalate_auth=False,
            escalate_prompt="",
        )
    )
}

FAILED_WHEN_CONTAINS = [
    "%% Invalid input detected at '^' marker."
]
