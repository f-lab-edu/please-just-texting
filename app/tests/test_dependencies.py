import pytest
from app.dependencies import get_db
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_get_db(mocker: MockerFixture) -> None:
    # given
    mock_get_session = mocker.MagicMock()
    mock_session = mocker.MagicMock()
    mock_session.name = "session"
    mock_db = mocker.MagicMock()
    mock_db.name = "db"
    mock_db.close = mocker.AsyncMock()
    mocker.patch("app.dependencies.get_session", mock_get_session)
    mock_get_session.return_value = mock_session
    mock_session.return_value = mock_db

    # when
    agen = get_db()
    db = await anext(agen)
    assert db is mock_db
    mock_session.assert_called_once()
    mock_db.close.assert_not_called()

    await anext(agen, None)
    mock_db.close.assert_called_once()
