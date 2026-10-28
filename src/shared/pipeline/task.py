from typing import Callable, Dict

from prefect import task

from shared.model.pipeline import LayerRoutine, Routine


def _map_dependecies(
    routine_futures: dict,
    routine: Routine,
) -> list:
    wait_for = []
    for dependency in routine.depends_on:
        dependency_label = dependency.label
        if dependency_label in routine_futures:
            wait_for.append(routine_futures[dependency_label])

    return wait_for


@task
def task_process_routine(
    conn_fn: Callable,
    routine: Routine,
):
    with conn_fn() as conn:
        for operation in routine.operations:
            operation(conn=conn)


@task
def task_process_layer(
    conn_fn: Callable,
    layer: LayerRoutine,
):
    with conn_fn() as conn:
        for operation in layer.operations:
            operation(conn=conn)

    routine_futures = {}
    for routine in layer.routines:
        routine_future = task_process_routine.submit(
            conn_fn=conn_fn,
            routine=routine,
            wait_for=_map_dependecies(
                routine_futures=routine_futures,
                routine=routine,
            ),
        )
        routine_futures[routine.label] = routine_future

    for routine_future in routine_futures.values():
        routine_future.result()
