async def data_to_model(model, data):
    from core.db_helper import db_helper
    session = db_helper.get_scoped_session()
    try:
        session.add(model(**data))
        await session.commit()
    finally:
        await session.close_all()
    return data


async def check_pagination(url, data):
    expected_keys = ('total', 'limit', 'offset')
    for expected_key in expected_keys:
        assert expected_key in data
