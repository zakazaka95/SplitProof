"""Controlled consensus/storage test double; not GenVM or live model evidence."""
import copy
import importlib.util
import pathlib
import sys
import types
from datetime import datetime as RealDateTime


class UserError(Exception):
    pass


class Return:
    def __init__(self, calldata):
        self.calldata = calldata


class Runtime:
    def __init__(self):
        self.outputs = []
        self.validator_outputs = None
        self.mutate = None
        self.prompts = []
        self.calls = 0
        self.phase = "leader"
        self.stage = 0
        self.sender = "0x" + "1" * 40
        self.clock = 1_800_000_000
        self.in_model = False
        self.model_clock_reads = 0
        self.clock_reads = 0
        self.fake = None

    def prompt(self, prompt, response_format=None):
        assert response_format == "json"
        self.prompts.append({"phase": self.phase, "prompt": prompt, "stage": self.stage})
        self.calls += 1
        outputs = self.validator_outputs if self.phase == "validator" and self.validator_outputs is not None else self.outputs
        if self.stage >= len(outputs):
            raise RuntimeError("No controlled model output for this stage")
        output = outputs[self.stage]
        self.stage += 1
        if isinstance(output, Exception):
            raise output
        return copy.deepcopy(output)

    def run(self, leader, validator):
        self.in_model = True
        try:
            self.phase, self.stage = "leader", 0
            candidate = leader()
            if self.mutate:
                candidate = self.mutate(copy.deepcopy(candidate))
            self.phase, self.stage = "validator", 0
            if not validator(Return(candidate)):
                raise AssertionError("Independent validator rejected complete receipt")
            return candidate
        finally:
            self.in_model = False

    def as_sender(self, address):
        self.sender = address
        self.fake.message.sender_address = address


def load():
    runtime = Runtime()
    fake = types.ModuleType("genlayer")
    fake.contract = types.SimpleNamespace(Contract=object)
    fake.storage = types.SimpleNamespace(TreeMap=dict)
    fake.public = types.SimpleNamespace(write=lambda f: f, view=lambda f: f)
    fake.message = types.SimpleNamespace(sender_address=runtime.sender)
    fake.nondet = types.SimpleNamespace(exec_prompt=runtime.prompt)
    fake.vm = types.SimpleNamespace(UserError=UserError, Return=Return, run_nondet_default=runtime.run)
    types_module = types.ModuleType("genlayer.types")
    types_module.u64 = int
    types_module.__all__ = ["u64"]
    previous = {name: sys.modules.get(name) for name in ["genlayer", "genlayer.types"]}
    sys.modules["genlayer"] = fake
    sys.modules["genlayer.types"] = types_module
    path = pathlib.Path(__file__).with_name("SplitProof.py")
    spec = importlib.util.spec_from_file_location("SplitProof", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        for name, value in previous.items():
            if value is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = value
    runtime.fake = fake

    class PublicMethodClock:
        @staticmethod
        def now(tz=None):
            runtime.clock_reads += 1
            if runtime.in_model:
                runtime.model_clock_reads += 1
                raise AssertionError("Clock may not be read inside model receipt reconstruction")
            return RealDateTime.fromtimestamp(runtime.clock, tz)

    # Exercise the source's real timestamp helper rather than replacing _now.
    module.datetime = PublicMethodClock
    contract = module.SplitProof()
    for name, annotation in module.SplitProof.__annotations__.items():
        if getattr(annotation, "__origin__", None) is dict:
            setattr(contract, name, {})
    return module, contract, runtime
