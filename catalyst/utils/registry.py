import copy
from typing import Dict, Callable, Any, Union, Type, Mapping, Tuple
import warnings

Factory = Union[Type, Callable[..., Any]]


class RegistryException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Registry:
    """
    Universal class allowing to add and access various factories by name
    """

    def __init__(self):
        self._factories: Dict[str, Factory] = {}

    @staticmethod
    def _get_factory_name(f, provided_name=None) -> str:
        if not provided_name:
            provided_name = getattr(f, "__name__", None)
            if not provided_name:
                raise RegistryException(
                    f"Factory {f} has no __name__ and no "
                    f"name was provided"
                )
            if provided_name == "<lambda>":
                raise RegistryException(
                    "Name for lambda factories msut be provided"
                )
        return provided_name

    def add(
        self,
        factory: Factory = None,
        *factories: Factory,
        name: str = None,
        **named_factories: Factory
    ) -> None:
        """
        Adds factory to registry with it's __name__ attribute or provided
        name.
        Signature is flexible.

        :param factory: Factory instance
        :param factories: More instances
        :param name: Provided name for first instance. Use only when pass
        single instance.
        :param named_factories: Factory and their names as kwargs
        """
        if len(factories) > 0 and name is not None:
            raise RegistryException(
                "Multiple factories with single name are not allowed"
            )

        if factory is not None:
            named_factories[self._get_factory_name(factory, name)] = factory

        if len(factories) > 0:
            named_factories.update({
                self._get_factory_name(f): f
                for f in factories
            })

        if len(named_factories) == 0:
            warnings.warn("No factories were provided!")

        for name in named_factories:
            if name in self._factories:
                raise RegistryException(
                    f"Factory with name '{name}' is already present"
                )

        self._factories.update(named_factories)

    def add_from_module(self, module) -> None:
        """
        Adds all factories present in module.
        If __all__ attribute is present, takes ony what mentioned in it

        :param module: module to scan
        :return: None
        """
        factories = module.__dict__

        # Filter by __all__ if present
        names_to_add = getattr(module, "__all__", list(factories.keys()))

        to_add = {name: factories[name] for name in names_to_add}

        self.add(**to_add)

    def get(self, name: str) -> Factory:
        """
        Retrieves factory, without creating any objects with it or raises
        error

        :param factory name
        :returns Factory
        """
        res = self._factories.get(name, None)

        if not res:
            raise RegistryException(
                f"No factory with name '{name}' was registered"
            )

        return res

    def get_instance(self, name: str, *args, **kwargs):
        """
        Creates instance by calling specified factory
        :param name: factory name
        :param args: args to pass to the factory
        :param kwargs: kwargs to pass to the factory
        :return: created instance
        """
        f = self.get(name)

        try:
            if hasattr(f, "create_from_params"):
                return f.create_from_params(*args, **kwargs)
            return f(*args, **kwargs)
        except Exception as e:
            raise RegistryException(
                f"Factory '{name}' call failed: args={args} kwagrs={kwargs}"
            ) from e

    def get_from_config(
        self,
        name_key: str,
        config: Mapping[str, Any],
        instantiate=True,
        **kwargs

    ) -> Union[Any, Tuple[Any, Mapping[str, Any]]]:
        """
        Creates instance based in configuration dict.
        If config[name_key] is None, None is returned.

        :param name_key: key in config containing name of the factory
        :param config: config dict
        :param instantiate: If true, calls factory with rest of config dict
        and kwargs, if false, returns factory and the rest of config and
        kwargs joined
        :param kwargs: additional kwargs for factory
        :return: result of factory call or (factory, config) tuple
        """
        config = copy.deepcopy(dict(config))
        name = config.pop(name_key, None)
        if name:
            if instantiate:
                return self.get_instance(name, **config, **kwargs)
            else:
                config.update(kwargs)
                return self.get(name), config
        return None if instantiate else None, config


__all__ = ["Registry"]
