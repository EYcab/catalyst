"""
catalyst.dl subpackage registries
"""

from catalyst.utils.registry import Registry


def _grad_clip_loader(r: Registry):
    from torch.nn.utils import clip_grad as m
    r.add_from_module(m)


GRAD_CLIPPERS = Registry("func")
GRAD_CLIPPERS.late_add(_grad_clip_loader)


def _criterion_loader(r: Registry):
    from catalyst.contrib import criterion as m
    r.add_from_module(m)


CRITERIONS = Registry("criterion")
CRITERIONS.late_add(_criterion_loader)
Criterion = CRITERIONS.add


def _model_loader(r: Registry):
    from catalyst.contrib import models as m
    r.add_from_module(m)


MODELS = Registry("model")
MODELS.late_add(_model_loader)
Model = MODELS.add


def _modules_loader(r: Registry):
    from catalyst.contrib import modules as m
    r.add_from_module(m)


MODULES = Registry("module")
MODULES.late_add(_modules_loader)
Module = MODULES.add


def _callbacks_loader(r: Registry):
    from catalyst.dl import callbacks as m
    r.add_from_module(m)


CALLBACKS = Registry("callback")
CALLBACKS.late_add(_callbacks_loader)
Callback = CALLBACKS.add


def _optimizers_loader(r: Registry):
    from catalyst.contrib import optimizers as m
    r.add_from_module(m)


OPTIMIZERS = Registry("optimizer")
OPTIMIZERS.late_add(_optimizers_loader)
Optimizer = OPTIMIZERS.add


def _schedulers_loader(r: Registry):
    from torch.optim import lr_scheduler as m
    r.add_from_module(m)


SCHEDULERS = Registry("scheduler")
SCHEDULERS.late_add(_schedulers_loader)
Scheduler = SCHEDULERS.add

__all__ = [
    "Criterion", "Model", "Module", "Callback", "Optimizer", "Scheduler"
]
