from functools import partial
from typing import Callable

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

from src.persistence.database.operation import load_extensions
from src.shared.model.pipeline import Catalog, Layer, Routine

@task(
    name="Process Routine",
    task_run_name="{routine.label}",
)
def task_process_routine(
    routine: Routine,
    conn_fn: Callable,
):
    with conn_fn() as conn:
        for operation in routine.operations:
            operation(conn=conn)


@task(
    name="Process Layer",
    task_run_name="{layer.label}",
)
def task_process_layer(
    layer: Layer,
    conn_fn: Callable,
):
    if layer.required_extensions:
        load_extensions_fn = partial(
            load_extensions,
            extensions=layer.required_extensions,
        )

    with conn_fn(load_extensions_fn=load_extensions_fn) as conn:
        for operation in layer.operations:
            operation(conn=conn)

    routine_futures = {}
    for routine in layer.routines:

        wait_for = []
        for dep_routine in routine.depends_on:
            label = dep_routine.label
            if label in routine_futures:
                wait_for.append(routine_futures[label])

        routine_future = task_process_routine.submit(
            conn_fn=conn_fn,
            routine=routine,
            wait_for=wait_for,
        )

        routine_futures[routine.label] = routine_future

    for routine_future in routine_futures.values():
        routine_future.result()


@flow(
    name="Process Catalog",
    flow_run_name="{catalog.label}",
    task_runner=ConcurrentTaskRunner()
)
def flow_process_catalog(
    catalog: Catalog,
    conn_fn: Callable,
):

    layer_futures = {}
    for layer in catalog.layers:

        wait_for = []
        for dep_layer in layer.depends_on:
            label = dep_layer.label
            if label in layer_futures:
                wait_for.append(layer_futures[label])

        layer_future = task_process_layer.submit(
            conn_fn=conn_fn,
            layer=layer,
            wait_for=wait_for,
        )

        layer_futures[layer.label] = layer_future

    for layer_future in layer_futures.values():
        layer_future.result()
