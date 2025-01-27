from __future__ import annotations

from fortiface.modules.base import BaseModule

from deepface import DeepFace


class FaceAnalyze(BaseModule):
    def __init__(self): ...

    def execute(self, *args, **kwargs):
        return super().execute(*args, **kwargs)
