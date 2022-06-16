# gpt_interp

## <ins>Experiments</ins>

For our experiments, we use [unseal](https://github.com/TomFrederik/unseal/), which implement various hooks for our usage. For now we are using an edited forked version, since the main version has some [issues](link).

### <ins>Causal Tracing</ins>

We perform causal tracing on [GPT2-Large](https://huggingface.co/gpt2-large) as described in the [ROME](https://arxiv.org/abs/2202.05262) paper by Meng et al., and we use the following [dataset](https://drive.google.com/file/d/1u6wKzi26vvQ18LlD7UtIZnQxmIjNsCFn/view).

#### <ins>Gaussian Noise Subject Corruption</ins>
We took 100 examples, and for each example we corrupt the subject by adding gaussian noise. We then perform causual tracing, restoring each state with its non-corrupted counterpart. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/indirect_effect_100_examples.pdf) are the complete results of the indirect effect, $ p_{\*,h_{i}^{l}}(token) - p_{\*}(token)$, on 100 examples. [Some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/last_subject_token.pdf) examples match the last subject token/late site phenomena pretty well. [Some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/second_to_last_subject_token.pdf) examples have high indirect effect at the second to last subject token. [Some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/no_consistency.pdf) examples seem to have no consistency.
<br>
<br>
[Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/average_indirect_effect_100_examples.pdf) are the results of the average indirect effect across the 100 examples (it is similar to the results in the ROME paper). Here is the standard deivation of the indirect effect across the 100 examples.

#### <ins>Gaussian Noise Subject Corruption (Patching Good State with Bad State)</ins>
We took 100 examples and corrupted the subject by adding gaussian noise as we did in the previous experiment; then we saved the states. Instead of running 
the prompt with the corrupted subject through the model and patching with the non-corrupted states, we instead do the opposite. That is, we run the vanilla prompt through the model and patch each state with its corresponding corrupted state. Here are the results of measuring the indirect effect (p_h*(token) -p(token)) across the 100 examples. Here are the results of the average indirect effect across the 100 examples. Here is the standard deivation of the indirect effect across the 100 examples.

#### <ins>Varying Gaussian Noise Subject Corruption</ins>

#### <ins>Random Gaussian Embedding Subject Corruption</ins>

#### <ins>Shuffling Embeddings of the Subject</ins>

#### <ins>Adding Non-Confusing Prefix to the Subject</ins>

#### <ins>Prefix with False Facts</ins>

## <ins>lit-review</ins>
See this [doc](link) for notes on relevant literature.

## <ins>to-do</ins>
<ol>
  <li>Get SCF access and access to Balrog (40GB) so you can run experiments on GTP-J (currently I am running experiments on Y GPU in google collab). </li>
  <li>Run experimetns on GPT-J once above is done.</li>
  <li>Parallelize Causual Tracing.</li>
  <li>Run experiments on all 1000 examples once above is done. </li>
  <li>Measure how often the indirect effect is in the wrong direction. </li>
</ol>
