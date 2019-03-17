import torch.optim.lr_scheduler

from ..utils.registry import Registry
from catalyst.contrib import criterion, models, modules, optimizers
from catalyst.dl import callbacks

CRITERIONS = Registry()
CALLBACKS = Registry()
MODELS = Registry()
MODULES = Registry()
OPTIMIZERS = Registry()
SCHEDULERS = Registry()
GRAD_CLIPPERS = Registry()

CatalystCriterion = CRITERIONS.add
CatalystModel = MODELS.add
CatalystModule = MODULES.add
CatalystOptimizer = OPTIMIZERS.add
CatalystCallback = CALLBACKS.add
CatalystScheduler = SCHEDULERS.add

CRITERIONS.add_from_module(criterion)
MODELS.add_from_module(models)
MODULES.add_from_module(modules)
OPTIMIZERS.add_from_module(optimizers)
CALLBACKS.add_from_module(callbacks)
SCHEDULERS.add_from_module(torch.optim.lr_scheduler)
GRAD_CLIPPERS.add_from_module(torch.nn.utils)


__all__ = [
    "CatalystCriterion", "CatalystModel", "CatalystModule",
    "CatalystCallback", "CatalystOptimizer", "CatalystScheduler"
]
