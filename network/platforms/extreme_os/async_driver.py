from copy import deepcopy
from io import BytesIO
from typing import Any, Callable, Dict, List, Optional, Union

from scrapli.driver import AsyncNetworkDriver
from .base_driver import FAILED_WHEN_CONTAINS, PRIVS
from scrapli.driver.network.base_driver import PrivilegeLevel


import logging

async def netos_on_open(conn: AsyncNetworkDriver) -> None:
    """
    AsyncNetOSDriver default on_open callable with enhanced debugging.

    Args:
        conn: NetworkDriver object

    Returns:
        None

    Raises:
        N/A
    """
    # Enable debugging to capture everything received from the device
    logging.basicConfig(level=logging.DEBUG)

    # Increase the timeout to allow more time to get the prompt
    conn.channel.timeout_ops = 60.0

    # Read and log the initial banner/output
    initial_output = await conn.channel.read()
    logging.debug(f"Initial output: {initial_output}")

    # Try to acquire the privilege level
    try:
        await conn.acquire_priv(desired_priv=conn.default_desired_privilege_level)
    except Exception as e:
        logging.error(f"Failed to acquire privilege level: {e}")
        raise

    # Disable paging (if necessary)
    await conn.send_command(command="disable clipaging")




async def netos_on_close(conn: AsyncNetworkDriver) -> None:
    """
    AsyncNetOSDriver default on_close callable

    Args:
        conn: NetworkDriver object

    Returns:
        None

    Raises:
        N/A

    """
    await conn.acquire_priv(desired_priv=conn.default_desired_privilege_level)
    await conn.send_command(command="enable clipaging")
    conn.channel.write(channel_input="exit")
    conn.channel.send_return()


class AsyncExtremeOSDriver(AsyncNetworkDriver):
    def __init__(
        self,
        host: str,
        privilege_levels: Optional[Dict[str, PrivilegeLevel]] = None,
        default_desired_privilege_level: str = "privilege_exec",
        port: Optional[int] = None,
        auth_username: str = "",
        auth_password: str = "",
        auth_private_key: str = "",
        auth_private_key_passphrase: str = "",
        auth_strict_key: bool = True,
        auth_bypass: bool = False,
        auth_telnet_login_pattern: str = "",
        auth_password_pattern: str = "",
        auth_passphrase_pattern: str = "",
        timeout_socket: float = 15.0,
        timeout_transport: float = 30.0,
        timeout_ops: float = 30.0,
        comms_return_char: str = "\n",
        comms_roughly_match_inputs: bool = False,
        ssh_config_file: Union[str, bool] = False,
        ssh_known_hosts_file: Union[str, bool] = False,
        on_init: Optional[Callable[..., Any]] = None,
        on_open: Optional[Callable[..., Any]] = None,
        on_close: Optional[Callable[..., Any]] = None,
        transport: str = "system",
        transport_options: Optional[Dict[str, Any]] = None,
        channel_log: Union[str, bool, BytesIO] = False,
        channel_log_mode: str = "write",
        channel_lock: bool = False,
        logging_uid: str = "",
        auth_secondary: str = "",
        failed_when_contains: Optional[List[str]] = None,
        textfsm_platform: str = "extreme_exos",
        genie_platform: str = "",
    ):
        """
        AsyncNetOSDriver Object

        Please see `scrapli.driver.base.base_driver.Driver` for all "base driver" arguments!

        # noqa: DAR101

        Args:
            privilege_levels: optional user provided privilege levels, if left None will default to
                scrapli standard privilege levels
            default_desired_privilege_level: string of name of default desired priv, this is the
                priv level that is generally used to disable paging/set terminal width and things
                like that upon first login, and is also the priv level scrapli will try to acquire
                for normal "command" operations (`send_command`, `send_commands`)
            auth_secondary: password to use for secondary authentication (enable)
            on_open: callable that accepts the class instance as its only argument. this callable,
                if provided, is executed immediately after authentication is completed. Common use
                cases for this callable would be to disable paging or accept any kind of banner
                message that prompts a user upon connection
            on_close: callable that accepts the class instance as its only argument. this callable,
                if provided, is executed immediately prior to closing the underlying transport.
                Common use cases for this callable would be to save configurations prior to exiting,
                or to logout properly to free up vtys or similar.
            textfsm_platform: string name of textfsm parser platform
            genie_platform: string name of cisco genie parser platform
            failed_when_contains: List of strings that indicate a command/config has failed

        Returns:
            None

        Raises:
            N/A

        """
        if privilege_levels is None:
            privilege_levels = deepcopy(PRIVS)

        if on_open is None:
            on_open = netos_on_open
        if on_close is None:
            on_close = netos_on_close

        if failed_when_contains is None:
            failed_when_contains = FAILED_WHEN_CONTAINS.copy()

        super().__init__(
            host=host,
            port=port,
            auth_username=auth_username,
            auth_password=auth_password,
            auth_private_key=auth_private_key,
            auth_private_key_passphrase=auth_private_key_passphrase,
            auth_strict_key=auth_strict_key,
            auth_bypass=auth_bypass,
            auth_telnet_login_pattern=auth_telnet_login_pattern,
            auth_password_pattern=auth_password_pattern,
            auth_passphrase_pattern=auth_passphrase_pattern,
            timeout_socket=timeout_socket,
            timeout_transport=timeout_transport,
            timeout_ops=timeout_ops,
            comms_return_char=comms_return_char,
            comms_roughly_match_inputs=comms_roughly_match_inputs,
            ssh_config_file=ssh_config_file,
            ssh_known_hosts_file=ssh_known_hosts_file,
            on_init=on_init,
            on_open=on_open,
            on_close=on_close,
            transport=transport,
            transport_options=transport_options,
            channel_log=channel_log,
            channel_log_mode=channel_log_mode,
            channel_lock=channel_lock,
            logging_uid=logging_uid,
            privilege_levels=privilege_levels,
            default_desired_privilege_level=default_desired_privilege_level,
            auth_secondary=auth_secondary,
            failed_when_contains=failed_when_contains,
            textfsm_platform=textfsm_platform,
            genie_platform=genie_platform,
        )