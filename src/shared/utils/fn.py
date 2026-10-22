from functools import partial, wraps

def named_partial(
    name, 
    fn, 
    *args, 
    **kwargs,
):
    """
    Cria um partial funcional que possui um atributo __name__ personalizado
    e preserva a docstring da função original.
    """
    partial_fn = partial(
        fn, 
        *args, 
        **kwargs
    )
    
    @wraps(fn)
    def wrapper(
        *call_args, 
        **call_kwargs
    ):
        return partial_fn(
            *call_args, 
            **call_kwargs
    )
    
    wrapper.__name__ = name
    return wrapper