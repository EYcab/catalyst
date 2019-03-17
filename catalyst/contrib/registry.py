from typing import Type, Union, Callable, List
import copy
import torch
import torch.nn as nn
from catalyst.contrib import criterion, models, modules, optimizers
from catalyst.dl import callbacks
from catalyst.rl import agents, environments
from catalyst.rl.offpolicy import algorithms
from catalyst.dl.fp16 import Fp16Wrap

Factory = Union[Type, Callable]

_REGISTERS = {
    "agent": agents.__dict__,
    "algorithm": algorithms.__dict__,
    "callback": callbacks.__dict__,
    "criterion": criterion.__dict__,
    "environment": environments.__dict__,
    "experiment": {},
    "model": models.__dict__,
    "module": modules.__dict__,
    "optimizer": optimizers.__dict__,
    "runner": {},
}


class Registry:
    @staticmethod
    def _inner_register(
        register_type: str, *object_factories: Factory
    ) -> Union[Factory, List[Factory]]:

        for factory in object_factories:
            registers = _REGISTERS[register_type]
            registers[factory.__name__] = factory

        if len(object_factories) == 1:
            return object_factories[0]
        return object_factories

    @staticmethod
    def agent(*agent_factories: Factory) -> Union[Factory, List[Factory]]:
        """Add agent type or factory method to global
            agent list to make it available in config
            Can be called or used as decorator
            :param: agent_factories
                Required agent factory (method or type)
            :returns: single agent factory or list of them
        """
        return Registry._inner_register("agent", *agent_factories)

    @staticmethod
    def algorithm(
        *algorithm_factories: Factory
    ) -> Union[Factory, List[Factory]]:
        """Add algorithm type or factory method to global
            algorithm list to make it available in config
            Can be called or used as decorator
            :param: algorithm_factories
                Required algorithm factory (method or type)
            :returns: single algorithm factory or list of them
        """
        return Registry._inner_register("algorithm", *algorithm_factories)

    @staticmethod
    def callback(
        *callback_factories: Factory
    ) -> Union[Factory, List[Factory]]:
        """Add callback type or factory method to global
            callback list to make it available in config
            Can be called or used as decorator
            :param: callback_factories
                Required callback factory (method or type)
            :returns: single callback factory or list of them
        """
        return Registry._inner_register("callback", *callback_factories)

    @staticmethod
    def criterion(
        *criterion_factories: Factory
    ) -> Union[Factory, List[Factory]]:
        """Add criterion type or factory method to global
            criterion list to make it available in config
            Can be called or used as decorator
            :param: criterion_factories
                Required criterion factory (method or type)
            :returns: single criterion factory or list of them
        """
        return Registry._inner_register("criterion", *criterion_factories)

    @staticmethod
    def environment(
        *environment_factories: Factory
    ) -> Union[Factory, List[Factory]]:
        """Add environment type or factory method to global
            environment list to make it available in config
            Can be called or used as decorator
            :param: environment_factories
                Required environment factory (method or type)
            :returns: single environment factory or list of them
        """
        return Registry._inner_register("environment", *environment_factories)

    @staticmethod
    def experiment(*factories: Factory) -> Union[Factory, List[Factory]]:
        """
        @TODO: refactor registry
        """
        return Registry._inner_register("experiment", *factories)

    @staticmethod
    def model(*models_factories: Factory) -> Union[Factory, List[Factory]]:
        """Add model type or factory method to global
            model list to make it available in config
            Can be called or used as decorator
            :param: models_factories
                Required model factory (method or type)
            :returns: single model factory or list of them
        """
        return Registry._inner_register("model", *models_factories)

    @staticmethod
    def module(*modules_factories: Factory) -> Union[Factory, List[Factory]]:
        """Add module type or factory method to global
            module list to make it available in config
            Can be called or used as decorator
            :param: modules_factories
                Required module factory (method or type)
            :returns: single module factory or list of them
        """
        return Registry._inner_register("module", *modules_factories)

    @staticmethod
    def optimizer(
        *optimizer_factories: Factory
    ) -> Union[Factory, List[Factory]]:
        """Add optimizer type or factory method to global
            optimizer list to make it available in config
            Can be called or used as decorator
            :param: optimizer_factories
                Required optimizer factory (method or type)
            :returns: single optimizer factory or list of them
        """
        return Registry._inner_register("optimizer", *optimizer_factories)

    @staticmethod
    def runner(*factories: Factory) -> Union[Factory, List[Factory]]:
        """
        @TODO: refactor registry
        """
        return Registry._inner_register("runner", *factories)



    @staticmethod
    def get_agent(agent=None, **agent_params):
        if agent is None:
            return None
        agent_fn = _REGISTERS["agent"][agent]
        try:
            agent = agent_fn(**agent_params)
        except Exception:
            agent = agent_fn.create_from_params(**agent_params)
        return agent

    @staticmethod
    def get_algorithm(algorithm=None, **algorithm_params):
        if algorithm is None:
            return None
        algorithm_fn = _REGISTERS["algorithm"][algorithm]
        try:
            algorithm = algorithm_fn(**algorithm_params)
        except Exception:
            algorithm = algorithm_fn.create_from_params(**algorithm_params)
        return algorithm

    @staticmethod
    def get_environment(environment=None, **environment_params):
        if environment is None:
            return None
        environment_fn = _REGISTERS["algorithm"][environment]
        try:
            environment = environment_fn(**environment_params)
        except Exception:
            environment = environment_fn.create_from_params(
                **environment_params
            )
        return environment
