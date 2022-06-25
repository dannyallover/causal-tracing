from typing import Iterable, Callable, Optional, Union, List, Tuple, Dict
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import BoundaryNorm
import numpy as np
import transformers
import torch


def plot_results(results: torch.Tensor, x: int, y: List[str], lower_bound: float, upper_bound: float, \
                 incr: float, title: str, color_schema: str):
    
    cmap = plt.get_cmap(color_schema)

    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # create the new map
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

    bounds = np.arange(lower_bound, upper_bound, incr)
    idx=np.searchsorted(bounds,0)
    bounds=np.insert(bounds,idx,0)
    norm = BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(7,5))
    image = plt.pcolormesh(results, norm=norm, cmap=cmap)
    plt.yticks(np.arange(len(y))+0.5, y)
    plt.xticks(np.arange(0, x, 5)+0.5, np.arange(0, x, 5))
    cbar = plt.colorbar(image)
    plt.gca().invert_yaxis()
    cbar.ax.set_title(title, x = 1 + len(title)/6, y = -0.1)
    
def subject_corruption_AIE(analysis: List[Tuple[torch.Tensor, List[str]]], num_layers: int):
    prob = torch.zeros(6, num_layers)
    count = [0] * 6
    for i in range(len(analysis)):
        tkens = analysis[i][1]
        pre_subject = True
        j = 0
        for p in analysis[i][0]:
            if (j == 0 and tkens[j][-1] == '*') or \
               (j > 0 and tkens[j][-1] == '*' and tkens[j-1][-1] != '*'): # first subject token
                prob[0] += p
                count[0] += 1
                pre_subject = False
            elif pre_subject: # pre subject token, which we don't count
                j += 1
                continue
            elif tkens[j][-1] == '*' and tkens[j+1][-1] == '*': # middle subject token
                prob[1] += p
                count[1] += 1
            elif tkens[j][-1] == '*' and tkens[j+1][-1] != '*': # last subject token
                prob[2] += p
                count[2] += 1
            elif tkens[j][-1] != '*' and tkens[j-1][-1] == '*': # first subsequent token
                prob[3] += p
                count[3] += 1
            elif j == len(tkens) - 1: # last token
                prob[5] += p
                count[5] += 1
            else: # further tokens
                prob[4] += p
                count[4] += 1
            j += 1
    for i in range(len(prob)):
        prob[i] /= count[i]
        
    return prob

def get_subject_positions(tkens: List[str], subject: str):
    for i in range(len(tkens)):
        for j in range(len(tkens)):
            sub = tkens[i:j]
            sub_str = ''.join(sub).strip()
            if sub_str == subject:
                return [i, j]
    return [-1, -1]

# unseal doesn't include this in their utilities
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

# modified from unseal
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

# modified from unseal
def save_output(save_ctx: dict, input: torch.Tensor, output: torch.Tensor):
    if isinstance(output, torch.Tensor):
        save_ctx['output'] = output.to('cpu')
    elif isinstance(output, Iterable): # hope for the best
        save_ctx['output'] = recursive_to_device(output, 'cpu')