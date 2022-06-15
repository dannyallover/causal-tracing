# gpt_interp

## <ins>Experiments</ins>

For our experiments, we use [unseal](https://github.com/TomFrederik/unseal/), which implement various hooks for our usage.

### <ins>Causal Tracing</ins>

We perform causal tracing on [GPT2-Large](https://huggingface.co/gpt2-large) as described in the [ROME](https://arxiv.org/abs/2202.05262) paper by Meng et al., and we use the following [dataset](https://drive.google.com/file/d/1u6wKzi26vvQ18LlD7UtIZnQxmIjNsCFn/view).

#### <ins>Gaussian Noise Subject Corruption (Patching Bad State with Good State)</ins>
We took 100 examples, and for each example we corrupt the subject by adding gaussian noise. We then perform causual tracing, restoring each state with its non-corrupted counterpart. Here are the results of the indirect effect (p*,h(token) - p*(token)) on 100 examples. Here are the results of the average indirect effect across the 100 examples. Here is the standard deivation of the indirect effect across the 100 examples.

#### <ins>Gaussian Noise Subject Corruption (Patching Good State with Bad State)</ins>
We took 100 examples and corrupted the subject by adding gaussian noise as we did in the previous experiment; then we saved the states. Instead of running 
the prompt with the corrupted subject through the model and patching with the non-corrupted states, we instead do the opposite. That is, we run the vanilla prompt through the model and patch each state with its corresponding corrupted state. Here are the results of measuring the indirect effect (p_h*(token) -p(token)) across the 100 examples. Here are the results of the average indirect effect across the 100 examples. Here is the standard deivation of the indirect effect across the 100 examples.

#### <ins>Varying Gaussian Noise Subject Corruption (Patching Bad State with Good State)</ins>

#### <ins>Random Gaussian Embedding Subject Corruption (Patching Bad State with Good State)</ins>

#### <ins>Shuffling Embeddings of the Subject (Patching Bad State with Good State)</ins>

## lit-review
See this google doc for relevant literature.

## to-do
<ol>
  <li>Get access to stats computing cluster and run on X GPU (currently I am running experiments on this GPU in google collab). </li>
  <li>Parallelize Causual Tracing.</li>
</ol>
