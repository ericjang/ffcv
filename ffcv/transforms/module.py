"""
Mixup augmentation [CITE]
"""
import torch as ch
from numpy.random import permutation, rand
from typing import Callable, Optional, Tuple
from ..pipeline.allocation_query import AllocationQuery
from ..pipeline.operation import Operation
from ..pipeline.stage import Stage
from ..pipeline.state import State

class ModuleWrapper(Operation):
    def __init__(self, module: ch.nn.Module):
        super().__init__()
        self.module = module
    
    def generate_code(self) -> Callable:
        def apply_module(inp, dst):
            self.module(inp)
            return inp

        return apply_module
    
    def declare_state_and_memory(self, previous_state: State) -> Tuple[State, Optional[AllocationQuery]]:
        assert previous_state.stage == Stage.PYTORCH
        return previous_state, None 
                             # AllocationQuery(previous_state.shape, 
                               #                dtype=previous_state.dtype,
                               #                device=previous_state.device)