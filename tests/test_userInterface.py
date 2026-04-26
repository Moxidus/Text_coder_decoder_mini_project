# example code coppied from https://github.com/zauberzeug/nicegui/blob/main/examples/pytests/tests/test_with_user.py

import pytest
from nicegui.testing import User


async def test_page_loads_with_title(user: User) -> None:
    await user.open("/")
    await user.should_see("Text Coder and Decoder")
