from typing import Union

from pypika import Table, MySQLQuery, Parameter, Field, Order, Criterion

# Constants
CRITERION = {
    'all': Criterion.all,
    'any': Criterion.any,
}

# Helpers

def _get_order(desc):
    return Order.desc if desc else Order.asc


def create_placeholders(amount:int)-> list[Parameter]:
    return [Parameter("%s") for _ in range(amount)]

def insert_query(table:Table, columns:list[Field])-> MySQLQuery:
    placeholders = create_placeholders(len(columns))
    query = MySQLQuery.into(table) \
        .columns(*columns) \
        .insert(*placeholders)
    
    return query

def select_query(
    table:Table, columns:list[Field], condition:list = None, 
    distinct:bool = False, criterion:str = 'all',
    order_by: str = None, desc:bool = True, limit:int = None
    )-> MySQLQuery:
    query = MySQLQuery.from_(table).select(*columns)

    if distinct:
        query = query.distinct()

    if condition:
        # Check Criterion in pypika to understand
        criterion = CRITERION[criterion]
        query = query.where(
            criterion(condition)
        )
    
    if order_by:
        order = _get_order(desc)
        query = query.orderby(order_by, order=order)

    if limit:
        query = query.limit(limit)
    
    return query

def select_join_query(
    from_:Table, join:Table, on_fields:tuple[str],
    columns:list[Field], condition:tuple = None,
    criterion: str = 'all', order_by: str = None,
    desc: bool = True
    )-> MySQLQuery:
    query =  MySQLQuery \
        .from_(from_) \
        .join(join) \
        .on_field(*on_fields) \
        .select(*columns)

    if condition:
        # Check Criterion in pypika to understand
        criterion = CRITERION[criterion]
        query = query.where(
            criterion(condition)
        )
    
    if order_by:
        order = _get_order(desc)
        query = query.orderby(order_by, order=order)

    return query

def select_join_on_query(
    from_:Table, join_on:list[tuple[Table, tuple]], 
    columns:list[Field], condition:list = None, order_by:str = None,
    criterion:str = 'all'
    )-> MySQLQuery:
    query = MySQLQuery.from_(from_)
    for table, on_condition in join_on:
        query = query.join(table).on(on_condition)

    query = query.select(*columns)
    if condition:
        criterion = CRITERION[criterion]
        query = query.where(
            criterion(condition)
        )
    
    if order_by:
        query = query.orderby(order_by, order=Order.desc)
    return query
    

def delete_query(table:Table, condition:tuple)-> MySQLQuery:
    return MySQLQuery.from_(table).delete().where(condition)
    
def update_query(table:Table, updates:Union[tuple, list[tuple]], condition:tuple)-> MySQLQuery:
    query = MySQLQuery.update(table)
    if type(updates) == list:
        for update in updates:
            query = query.set(*update)
    else:
        query = query.set(*updates)

    query = query.where(condition)
    return query