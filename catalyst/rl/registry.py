from catalyst.contrib.registry import (
    MODULES, CRITERIONS, OPTIMIZERS, SCHEDULERS, GRAD_CLIPPERS, CALLBACKS,
    Module, Optimizer, Scheduler, Callback, Criterion
)
from ..utils.registry import Registry

AGENTS = Registry("agent")
ALGORITMS = Registry("")
ENVIRONMENTS = Registry("")

Agent = AGENTS.add
Algorithm = ALGORITMS.add
Environment = ENVIRONMENTS.add

__all__ = [
    "Agent", "Environment", "Algorithm", "Criterion", "MODULES", "CRITERIONS",
    "OPTIMIZERS", "SCHEDULERS", "GRAD_CLIPPERS", "CALLBACKS", "Module",
    "Optimizer", "Scheduler", "Callback"
]
