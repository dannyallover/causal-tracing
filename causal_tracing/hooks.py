from typing import Iterable, Callable, Optional, Union, List, Tuple, Dict
import torch

def create_slice_from_str(indices: str) -> slice:
    one, two = indices.split(':')
    return slice(int(one), int(two), 1)

# modified from unseal
def additive_output_noise(
    indices: str,
    mean: Optional[float] = 0,
    std: Optional[float] = 0.1,
    index: Optional[int] = 0,
    seed: Optional[int] = 0,
) -> Callable:
    slice = create_slice_from_str(indices)
    def func(save_ctx, input, output):
        torch.manual_seed(seed)
        noise = mean + (std * torch.randn_like(output[index][slice]))
        output[index][slice] += noise
        return output
    return func

# modified from unseal
def hidden_patch_hook_fn(
    layer: int,
    position: int,
    replacement_tensor: torch.Tensor,
) -> Callable:
    def func(save_ctx, input, output):
        output[0][:,position] = replacement_tensor[layer][:,0,position]
        return output
    return func
