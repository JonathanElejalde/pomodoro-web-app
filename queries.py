from typing import Union

from pypika import Table, MySQLQuery, Parameter, Field, Order


def create_placeholders(amount:int)-> list[Parameter]:
    return [Parameter("%s") for _ in range(amount)]

def insert_query(table:Table, columns:list[Field])-> MySQLQuery:
    placeholders = create_placeholders(len(columns))
    query = MySQLQuery.into(table) \
        .columns(*columns) \
        .insert(*placeholders)
    
    return query

def select_query(table:Table, columns:list[Field], condition:tuple = None, distinct:bool = False)-> MySQLQuery:
    query = MySQLQuery.from_(table).select(*columns)

    if distinct:
        query = query.distinct()

    if condition:
        query = query.where(condition)

    return query

def select_join_query(
    from_:Table, join:Table, on_fields:tuple[str],
    columns:list[Field], condition:tuple = None
    )-> MySQLQuery:
    query =  MySQLQuery \
        .from_(from_) \
        .join(join) \
        .on_field(*on_fields) \
        .select(*columns)

    if condition:
        query = query.where(condition)

    return query

def select_join_on_query(
    from_:Table, join_on:list[tuple[Table, tuple]], 
    columns:list[Field], condition:tuple = None, order_by:str = None
    )-> MySQLQuery:
    query = MySQLQuery.from_(from_)
    for table, on_condition in join_on:
        query = query.join(table).on(on_condition)

    query = query.select(*columns)
    if condition:
        query = query.where(condition)
    
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