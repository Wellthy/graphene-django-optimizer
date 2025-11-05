import graphql
from graphql import GraphQLSchema, GraphQLObjectType, FieldNode
from graphql.execution.execute import get_field_def

noop = lambda *args, **kwargs: None


def is_iterable(obj):
    return hasattr(obj, "__iter__") and not isinstance(obj, str)


def get_field_def_compat(
    schema: GraphQLSchema, parent_type: GraphQLObjectType, field_node: FieldNode
):
    return get_field_def(
        schema,
        parent_type,
        field_node.name.value if graphql.version_info < (3, 2) else field_node,
    )


def sanitize_queryset_kwargs(kwargs):
    """
    Sanitize kwargs for QuerySet methods to prevent SQL injection.
    
    Removes the '_connector' key from kwargs to prevent SQL injection attacks
    as described in Django security advisory regarding QuerySet.filter(),
    QuerySet.exclude(), and QuerySet.get() methods.
    
    Args:
        kwargs: Dictionary of keyword arguments to be passed to QuerySet methods
        
    Returns:
        Sanitized dictionary with '_connector' removed if present
    """
    if isinstance(kwargs, dict) and '_connector' in kwargs:
        sanitized = kwargs.copy()
        del sanitized['_connector']
        return sanitized
    return kwargs
