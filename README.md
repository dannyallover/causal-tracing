# gpt_interp

## Experiments

### GPT2-Large

We perform causal tracing on [GPT2-Large](https://huggingface.co/gpt2-large) as described in the [ROME](https://arxiv.org/abs/2202.05262) paper by Meng et al., and we use the following [dataset](https://drive.google.com/file/d/1u6wKzi26vvQ18LlD7UtIZnQxmIjNsCFn/view).

#### Patching Good State with Bad State
We took 100 examples and for each example we corrupt the subject by adding gaussian noise. We then perform causual tracing, restoring each state with its non-corrupted counterpart. Here are the results of the indirect effect on 100 examples. Here are the results of the average indirect effect across the 100 examples. Here is the standard deivation of the indirect effect across the 100 examples.
