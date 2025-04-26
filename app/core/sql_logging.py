from loguru import logger
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine
from contextvars import ContextVar
import time

request_id_context: ContextVar[str] = ContextVar('request_id', default='')

def set_request_id(request_id: str):
    request_id_context.set(request_id)

def get_request_id() -> str:
    return request_id_context.get()

def setup_sql_logging(engine: AsyncEngine):
    @event.listens_for(engine.sync_engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())
        request_id = get_request_id()
        log = logger.bind(request_id=request_id)
        log.info("Executing SQL: {sql}", sql=statement)
        if parameters:
            log.info("Parameters: {params}", params=parameters)

    @event.listens_for(engine.sync_engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        request_id = get_request_id()
        log = logger.bind(request_id=request_id)
        log.info("SQL executed in {time:.2f}s", time=total) 