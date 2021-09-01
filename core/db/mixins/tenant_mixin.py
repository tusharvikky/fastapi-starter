from sqlalchemy import Column, inspect, BigInteger, func, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Query

from core.db import session

class TenantMixin:

    @declared_attr
    def team_id(cls):
        if not cls.__multitenant__:
            return None
        
        return Column(BigInteger, nullable=False, default=_current_session_tenant)

def _current_session_tenant():
    try:
        tenant = session.info.get('tenant', False)
        if not tenant:
            return 1
        
        return tenant.id
    except:
        return 1


@event.listens_for(Query, 'before_compile', retval=True)
def before_compile(query):
    tenant_safe = query._execution_options.get('tenant_safe', False)
    if tenant_safe:
        return query
    
    for column in query.column_descriptions:
        entity = column['entity']
        if entity is None:
            continue

        inspector = inspect(column['entity'])
        mapper = getattr(inspector, 'mapper', None)
        if mapper and issubclass(mapper.class_, TenantMixin):
            query = query.enable_assertions(False).filter(
                entity.team_id.__eq__(query.session.info.get('tenant').id),
            )

    return query
