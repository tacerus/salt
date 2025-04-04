import pytest

try:
    import win32com.client

    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

import salt.utils.win_update as win_update
from tests.support.mock import MagicMock, patch

pytestmark = [
    pytest.mark.windows_whitelisted,
    pytest.mark.skip_unless_on_windows,
    pytest.mark.skipif(not HAS_WIN32, reason="Requires Win32 libraries"),
]


def test_available_no_updates():
    """
    Test installed when there are no updates on the system
    """
    with patch("salt.utils.winapi.Com", autospec=True), patch(
        "win32com.client.Dispatch", autospec=True
    ), patch.object(win_update.WindowsUpdateAgent, "refresh", autospec=True):
        wua = win_update.WindowsUpdateAgent(online=False)
        wua._updates = []

        available_updates = wua.available()

        assert available_updates.updates.Add.call_count == 0


def test_available_no_updates_empty_objects():
    """
    Test installed when there are no updates on the system
    """
    with patch("salt.utils.winapi.Com", autospec=True), patch(
        "win32com.client.Dispatch", autospec=True
    ), patch.object(win_update.WindowsUpdateAgent, "refresh", autospec=True):
        wua = win_update.WindowsUpdateAgent(online=False)
        wua._updates = [win32com.client.CDispatch, win32com.client.CDispatch]

        available_updates = wua.available()

        assert available_updates.updates.Add.call_count == 0


def test_installed_no_updates():
    """
    Test installed when there are no updates on the system
    """
    with patch("salt.utils.winapi.Com", autospec=True), patch(
        "win32com.client.Dispatch", autospec=True
    ), patch.object(win_update.WindowsUpdateAgent, "refresh", autospec=True):
        wua = win_update.WindowsUpdateAgent(online=False)
        wua._updates = []

        installed_updates = wua.installed()

        assert installed_updates.updates.Add.call_count == 0


def test_installed_no_updates_installed():
    """
    Test installed when there are no Installed updates on the system
    """
    with patch("salt.utils.winapi.Com", autospec=True), patch(
        "win32com.client.Dispatch", autospec=True
    ), patch.object(win_update.WindowsUpdateAgent, "refresh", autospec=True):
        wua = win_update.WindowsUpdateAgent(online=False)

        wua._updates = [
            MagicMock(IsInstalled=False),
            MagicMock(IsInstalled=False),
            MagicMock(IsInstalled=False),
        ]

        installed_updates = wua.installed()

        assert installed_updates.updates.Add.call_count == 0


def test_installed_updates_all_installed():
    """
    Test installed when all updates on the system are Installed
    """
    with patch("salt.utils.winapi.Com", autospec=True), patch(
        "win32com.client.Dispatch", autospec=True
    ), patch.object(win_update.WindowsUpdateAgent, "refresh", autospec=True):
        wua = win_update.WindowsUpdateAgent(online=False)

        wua._updates = [
            MagicMock(IsInstalled=True),
            MagicMock(IsInstalled=True),
            MagicMock(IsInstalled=True),
        ]

        installed_updates = wua.installed()

        assert installed_updates.updates.Add.call_count == 3


def test_installed_updates_some_installed():
    """
    Test installed when some updates are installed on the system
    """
    with patch("salt.utils.winapi.Com", autospec=True), patch(
        "win32com.client.Dispatch", autospec=True
    ), patch.object(win_update.WindowsUpdateAgent, "refresh", autospec=True):
        wua = win_update.WindowsUpdateAgent(online=False)

        wua._updates = [
            MagicMock(IsInstalled=True),
            MagicMock(IsInstalled=False),
            MagicMock(IsInstalled=True),
            MagicMock(IsInstalled=False),
            MagicMock(IsInstalled=True),
        ]

        installed_updates = wua.installed()

        assert installed_updates.updates.Add.call_count == 3
