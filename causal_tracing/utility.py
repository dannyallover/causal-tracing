from typing import Iterable, Callable, Optional, Union, List, Tuple, Dict

### taken from unseal
def prepare_input(
    text: str,
    tokenizer: transformers.AutoTokenizer,
    device: Optional[Union[str, torch.device]] = 'cpu'
) -> Tuple[dict, int]:
    encoded_text = tokenizer(text, return_tensors='pt').to(device)

    # split correct target token from sentence
    correct_id = encoded_text['input_ids'][0,-1].item()
    encoded_text['input_ids'] = encoded_text['input_ids'][:,:-1]
    encoded_text['attention_mask'] = encoded_text['attention_mask'][:,:-1]

    return encoded_text, correct_id

### modified from unseal
def recursive_to_device(
    iterable: Union[Iterable, torch.Tensor],
    device: Union[str, torch.device],
) -> Iterable:
    if isinstance(iterable, torch.Tensor):
        return iterable.to(device)

    new = []
    for i, item in enumerate(iterable):
        if isinstance(item, torch.Tensor):
            new.append(item.to(device))
        elif isinstance(item, Iterable):
            new.append(recursive_to_device(item, device))
        else:
            raise TypeError(f'Expected type tensor or Iterable but got {type(item)}.')
    if isinstance(iterable, Tuple):
        new = tuple(new)
    return new

### modified from unseal
def save_output(save_ctx: dict, input: torch.Tensor, output: torch.Tensor):
    if isinstance(output, torch.Tensor):
        save_ctx['output'] = output.to('cpu')
    elif isinstance(output, Iterable): # hope for the best
        save_ctx['output'] = recursive_to_device(output, 'cpu')

def create_slice_from_str(indices: str) -> slice:
    one, two = indices.split(':')
    return slice(int(one), int(two), 1)
