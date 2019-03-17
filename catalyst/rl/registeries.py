from ..utils.registry import Registry

from catalyst.rl import agents, environments
from catalyst.rl.offpolicy import algorithms
from catalyst.contrib import criterion

AGENTS = Registry()
ALGORITMS = Registry()
ENVIRONMENTS = Registry()
CRITERIONS = Registry()

CatalystAgent = AGENTS.add
CatalystAlgorithm = ALGORITMS.add
CatalystEnvironment = ENVIRONMENTS.add
CatalystCriterion = CRITERIONS.add

AGENTS.add_from_module(agents)
ALGORITMS.add_from_module(algorithms)
ENVIRONMENTS.add_from_module(environments)
CRITERIONS.add_from_module(criterion)

__all__ = [
    "CatalystAgent", "CatalystEnvironment", "CatalystAlgorithm",
    "CatalystCriterion"
]
