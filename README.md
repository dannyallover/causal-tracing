# gpt_interp

## <ins>Experiments</ins>

For our experiments, we use [unseal](https://github.com/TomFrederik/unseal/), which implement various hooks for our usage. For now we are using an edited forked version, since the main version has some [issues](link).

### <ins>Causal Tracing</ins>

We perform causal tracing on [GPT2-Large](https://huggingface.co/gpt2-large) as described in the [ROME](https://arxiv.org/abs/2202.05262) paper by Meng et al., and we use the following [dataset](https://drive.google.com/file/d/1u6wKzi26vvQ18LlD7UtIZnQxmIjNsCFn/view).

#### <ins>Gaussian Noise Subject Corruption</ins>
We took 100 examples, and for each example we corrupt the subject by adding gaussian noise. We then perform causual tracing, restoring each state with its non-corrupted counterpart. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/indirect_effect_100_examples.pdf) are the complete results of the indirect effect, $p_{\*,h_{i}^{l}}(token) - p_{\*}(token)$, on 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/average_indirect_effect_100_examples.pdf) are the results of the average indirect effect across the 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/standard_deviation_at_each_site.pdf) is the standard deivation of the indirect effect across the 100 examples.
<br>
<br>
<ins>observations:</ins>
[Some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/last_subject_token.pdf) examples match the last subject token/late site phenomena pretty well. [Some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/second_to_last_subject_token.pdf) examples have high indirect effect at the second to last subject token. [Some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/no_consistency.pdf) examples seem to have no consistency. The results from averaging the indirect effect across 100 examples seems to align with the results from the ROME paper (it's not quite the same but perhaps that's because we didn't use 1000 examples). The magnitude of the standard deviation seems to correlate with the early/late site phenomena (not sure what to make of that).

#### <ins>Gaussian Noise Subject Corruption (Patching Good State with Bad State)</ins>
We took 100 examples and corrupted the subject by adding gaussian noise as we did in the previous experiment; then we saved the states. Instead of running 
the prompt with the corrupted subject through the model and patching with the non-corrupted states, we instead do the opposite. That is, we run the vanilla prompt through the model and patch each state with its corresponding corrupted state. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subect_patch_good_with_bad/indirect_effect_100_examples.pdf) are the results of measuring the indirect effect, $p_{h\*\_{i}^{l}}(token) - p(token)$, across the 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subect_patch_good_with_bad/average_indirect_effect_100_examples.pdf) are the results of the average indirect effect across the 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subect_patch_good_with_bad/standard_deviation_at_each_site.pdf) is the standard deivation of the indirect effect across the 100 examples.
<br>
<br>
<ins>observations:</ins>
Like the previous experiment, [some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subect_patch_good_with_bad/last_subject_token.pdf) examples match the last subject token/late site phenomena pretty well. Also like before, [some](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subect_patch_good_with_bad/second_to_last_subject_token.pdf) examples have high indirect effect at the second to last subject token. Unlike the [last](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subject/no_consistency.pdf) experiment, we actually don't have any examples where patching the states has no consistency (I find this to be very interesrting, and I cannot explain why). Also, another [naunce](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subect_patch_good_with_bad/all_subject_tokens.pdf) in this expiriment, is that it seems that more of the subject tokens have a role (rather than just strictly the last or second to last token). Another [peculiarity](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_noise_subect_patch_good_with_bad/early_vs_late_subject_tokens.pdf) of this experiment is that it seems that the indirect effect of the earlier tokens seem to go in the opposite direction while the indirect effect effect fo the later tokens are in the expected direction. Lastly, the average indirect effect more consistnetly follows the results in the ROME paper. The standard deviation also much more consistently correlates with the average indirect effect.

#### Addendum on Above Two Experiments: <ins>Indirect Effect Wrong Direction</ins>
What I've observed in the above two experiments (especially when we patch the good state with the bad), is that the indirect effect goes in the opposite direction. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/indirect_effect_wrong_direction/indirect_effect_wrong_direction.pdf) is the percentage at which each site goes in the opposite direction for the first experiment. I'm not sure why the indirect effect would go in the opposite direction; however, there is a pattern to it: the indirect effect is less likely to go in the opposite direction at the last subject token/late site phenomenom. This could be explained by the fact that these sites are critical in predicting the token, so patching these areas lead to improvement more often. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/indirect_effect_wrong_direction/indirect_effect_opposite_direction_patch_good_with_bad.pdf) are the same results for the second experiment. This also follows the last subject/late site pattern, but there are two additional naunces here: the first subject token is much more vulnerable in going in the opposite direction (I noted this in the observations in experiment two), and also the very last site will never go in the opposite direction.

#### <ins>Varying Gaussian Noise Subject Corruption</ins>
We sought to find out the effect of varying the amount of guassian noise added to the subject. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/different_amounts_gaussian_noise_subject/indirect_effect_10_examples.pdf) are the results of the indirect effect on 10 examples where we vary the standard deviation by the following amounts: `[0.000001, 0.001, 0.01, 0.1, 0.5, 1, 1.5, 2.5, 5, 10, 100, 1000000]`.
<br>
<br>
<ins>observations:</ins>
What we see is what we expect: adding little guassian noise has less effect on predicting the token vs adding a large amount of guassian noise. In fact, when you add a large amount of guassian noise, patching does [not](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/different_amounts_gaussian_noise_subject/high_noise.pdf) really make a difference.

#### <ins>Random Gaussian Embedding Subject Corruption</ins>
Another experiment we performed was to replace the subject with a random guassian embedding. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_embedding_subject/indirect_effect_100_examples.pdf) are the results of the indirect effect on 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_embedding_subject/average_indirect_effect_100_examples.pdf) is the average of the indirect effect across the 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/gaussian_embedding_subject/standard_deviation_at_each_site.pdf) is the standard deviation at each site.
<br>
<br>
<ins>observations:</ins>
The results show that the last subject token/late site phenomenon is still present, although it is more subtle.

#### <ins>Shuffling Embeddings of the Subject</ins>
The last non-prefix experiment we performed was to shuffle the subject embeddings. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/shuffle_subject_embeddings/indirect_effect_100_examples.pdf) are the results of the indirect effect on 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/shuffle_subject_embeddings/average_indirect_effect_100_examples.pdf) is the average of the indirect effect across the 100 examples. [Here](https://github.com/dannyallover/gpt_interp/blob/main/causal_tracing/gtp-large/shuffle_subject_embeddings/standard_deviation_at_each_site.pdf) is the standard deviation at each site.
<br>
<br>
<ins>observations:</ins>
While the previous experiment still obeyed the phenomenom we've been seeing, this experiment finally breaks it. We see no consistency in both the average indirect effect and the standard deviation. It is probably the case that shuffling subject embeddings is more confusing (adversarial, let's say) than simply replacing with something random.

#### <ins>[deprioritized] Adding Non-Confusing Prefix to the Subject</ins>

#### <ins>Prefix with False Facts</ins>

## <ins>Relevant Literature</ins>
See this [doc](link) for notes on relevant literature.

## <ins>to-do:</ins>
<ol>
  <li>Get SCF access and access to Balrog (40GB) so you can run experiments on GTP-J (currently I am running experiments on Y GPU in google collab). </li>
  <li>Run experimetns on GPT-J once above is done.</li>
  <li>Parallelize Causual Tracing.</li>
  <li>Run experiments on all 1000 examples once above is done. </li>
</ol>
