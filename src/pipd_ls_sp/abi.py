"""The Need / Occupant ABI, and the Consumer that goes through it.

WP-FHS-13 was blocked on `ABI_CONSUMER_MISSING`. `tools/hotswap.py` implements the swap itself (preimage → bind →
stage → swap → control → POS → NEG → rollback, 5/5 tests), but a swap needs three things it did not have:

    Need      what a consumer requires of a capability: a name and a contract version
    Occupant  what a provider offers: the implementation that satisfies a Need
    Consumer  the code that resolves a Need to an Occupant at call time

Without the third, a hot swap can only be checked by running a separate process and reading its output -- which
proves that *some* entry point changed, not that the consumer the system actually uses now reaches the new occupant.
That distinction is the whole point of the work package, so this module makes the consumer the thing under test.

Design rules, each one a defect this file exists to prevent:

  * A version mismatch is a refusal, never a best-effort call. An occupant that answers a different contract is
    indistinguishable from a working one until it corrupts something.
  * Resolution happens per call, not at construction. A consumer that binds once cannot observe a swap -- it is a
    cached answer pretending to be a live lookup.
  * An unsatisfied need raises a named error. Returning None turns a wiring fault into a TypeError three frames away.
"""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

ABI_VERSION = 1


class AbiError(Exception):
    """Base for ABI faults; each subclass carries a stable code."""

    code = "ERR_ABI"


class AbiUnsatisfied(AbiError):
    code = "ERR_ABI_UNSATISFIED"


class AbiVersionMismatch(AbiError):
    code = "ERR_ABI_VERSION_MISMATCH"


class AbiDuplicateOccupant(AbiError):
    code = "ERR_ABI_DUPLICATE_OCCUPANT"


@dataclass(frozen=True)
class Need:
    """What a consumer requires. `version` is part of the requirement, not metadata."""

    name: str
    version: int = ABI_VERSION
    methods: tuple[str, ...] = ()

    def satisfied_by(self, occupant: "Occupant") -> bool:
        if occupant.need.name != self.name:
            return False
        if occupant.need.version != self.version:
            return False
        return all(hasattr(occupant.impl, m) for m in self.methods)


@dataclass
class Occupant:
    """A provider bound to a Need. `impl` is any object exposing the needed methods."""

    need: Need
    impl: Any
    origin: str = ""

    def call(self, method: str, *args, **kwargs):
        if not hasattr(self.impl, method):
            raise AbiUnsatisfied(f"{self.origin or type(self.impl).__name__} has no method {method!r}")
        return getattr(self.impl, method)(*args, **kwargs)


@dataclass
class Registry:
    """Need-name → Occupant. Deliberately not a global: two registries in one process must not see each other."""

    occupants: dict[str, Occupant] = field(default_factory=dict)

    def bind(self, occupant: Occupant, *, replace: bool = False) -> None:
        name = occupant.need.name
        if name in self.occupants and not replace:
            raise AbiDuplicateOccupant(f"{name!r} is already bound by {self.occupants[name].origin!r}")
        self.occupants[name] = occupant

    def resolve(self, need: Need) -> Occupant:
        occ = self.occupants.get(need.name)
        if occ is None:
            raise AbiUnsatisfied(f"no occupant for need {need.name!r}")
        if not need.satisfied_by(occ):
            raise AbiVersionMismatch(
                f"need {need.name!r} v{need.version} is not satisfied by {occ.origin or 'occupant'} "
                f"v{occ.need.version}" + (f" missing {[m for m in need.methods if not hasattr(occ.impl, m)]}"
                                          if need.methods else ""))
        return occ


def occupant_from_file(need: Need, path: Path, *, factory: str = "build") -> Occupant:
    """Load an occupant from a Python file. This is the shape a hot swap produces: the file changes, the Need does not."""
    path = Path(path)
    if not path.exists():
        raise AbiUnsatisfied(f"occupant file {path} does not exist")
    spec = importlib.util.spec_from_file_location(f"_occupant_{need.name}_{abs(hash(str(path)))}", path)
    if spec is None or spec.loader is None:
        raise AbiUnsatisfied(f"cannot load occupant from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, factory):
        raise AbiUnsatisfied(f"{path} has no factory {factory!r}")
    return Occupant(need=need, impl=getattr(mod, factory)(), origin=str(path))


class Consumer:
    """The code the system actually calls.

    `registry` is consulted on every call, so replacing the occupant is visible to a consumer that was constructed
    before the swap. A consumer that caches the occupant cannot tell you whether a swap took effect, and that is
    exactly the question a hot swap has to answer.
    """

    def __init__(self, need: Need, registry: Registry):
        self.need = need
        self.registry = registry

    def __call__(self, method: str, *args, **kwargs):
        return self.registry.resolve(self.need).call(method, *args, **kwargs)

    def serves(self, method: str, *args, **kwargs) -> dict:
        """POS/NEG probe: does the consumer, as wired, reach a working occupant?"""
        try:
            value = self(method, *args, **kwargs)
            return {"ok": True, "value": value, "origin": self.registry.resolve(self.need).origin}
        except AbiError as exc:
            return {"ok": False, "code": exc.code, "why": str(exc)}


def make_consumer(need: Need, occupant_path: Path, *, factory: str = "build") -> Consumer:
    """Convenience wiring: one need, one occupant file, one consumer."""
    reg = Registry()
    reg.bind(occupant_from_file(need, occupant_path, factory=factory))
    return Consumer(need, reg)
