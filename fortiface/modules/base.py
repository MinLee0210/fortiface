from __future__ import annotations

from abc import ABC, abstractmethod


class BaseModule(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError
