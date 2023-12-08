async def data_to_model(model, data):
    from core.db_helper import db_helper
    session = db_helper.get_scoped_session()
    try:
        session.add(model(**data))
        await session.commit()
    finally:
        await session.close_all()
    return data
