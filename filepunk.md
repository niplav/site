[home](./index.md)
-------------------

*author: niplav, created: 2025-08-19, modified: 2025-08-19, language: english, status: in progress, importance: 1, confidence: likely*

> __Fileservers × mechanism design × sub-cent microtransactions. A personal
æsthetic.__

`filepunk`
============

Notes:

* Currently mostly LLM-generated, I'll edit it.
* Something with sending an email for the price of 0.1 cent

```
# Mount services as filesystems
$ mount -t claudefs $CLAUDE_VIGILA /mnt/claude
$ echo $USER $CLAUDE_VIGILA_APIKEY >/mnt/claude/auth
$ cat /usr/niplav/vigila/CLAUDE.md >/mnt/claude/proj/conf/sysprompt
$ chmod -u claudefs -R u+rwx -u /usr/niplav/vigila
$ fossil backup -s /usr/niplav/vigila -d /mnt/tarsnap/store/home/vigila
pwd:
$ cat /usr/niplav/vigila/TODO.txt | tee /mnt/claude/models/4.3/sonnet
# Simple micropayment to an AI service
$ cat <{echo -e '0.00002 ETH\n'} <{cat /mnt/claude/billing/address/eth} >/mnt/ethereum/transactions/send/new

# Subscribe to a service with micropayments
echo "0.001 ETH/month" > /mnt/spotify/subscription/new
echo "0.00001 ETH/article" > /mnt/nytimes/payment_model

# Set up auto-micropayments with spending limits
mkdir -p /mnt/payments/auto/arxiv
echo "0.00002 ETH/paper" > /mnt/payments/auto/arxiv/rate
echo "0.001 ETH/month" > /mnt/payments/auto/arxiv/cap

# Stream content with pay-as-you-go model
tail -f /mnt/netflix/shows/stranger_things/s05e01 |
  tee /dev/video &
cat /mnt/payments/streaming_meter  # Shows: "0.000003 ETH/minute currently"

# Create a collaborative document with pay-for-edit
setfacl -m "u:friend1:0.00001 ETH/write" /home/docs/collab.md

# Query data markets
echo "SELECT avg_temp FROM weather.historical WHERE city='Prague' AND year>2020" > /mnt/datamarket/queries/new
cat /mnt/datamarket/queries/last/cost  # Shows: "0.00004 ETH"
cat /mnt/datamarket/queries/last/result

# Automatic context-based prompting service
find /home/projects/current -type f -name "*.rs" |
  xargs cat |
  grep TODO |
  tee /mnt/claude/contexts/rust
echo "Generate test cases for these TODOs" > /mnt/claude/tasks/new

# Mount computational resources with dynamic pricing
mount -t gpufs -o model=h200,bid=auto,max=0.0003eth/min aws.gpu.market /mnt/gpu
echo "source('~/models/diffusion.R')" > /mnt/gpu/sessions/new
cat /mnt/gpu/sessions/last/pricing  # "Current rate: 0.00018 ETH/min (4 bidders)"

# VCG auction for computing time with complex bids
cat > /mnt/auction/compute/bids/new << EOF
resource: "32-core CPU, 4h"
value: "0.002 ETH"
deadline: "2025-05-16T18:00:00Z"
priority: "can pay 0.0005 ETH more if completed by tomorrow"
alternatives: "would accept 16-core for 6h at 0.0015 ETH"
EOF
cat /mnt/auction/compute/bids/last/status  # "Matched: 16-core for 5h at 0.00135 ETH"

# Probabilistic programming as a service
cat > /mnt/stan/models/new.stan << EOF
data {
  int<lower=0> N;
  vector[N] y;
}
parameters {
  real mu;
  real<lower=0> sigma;
}
model {
  y ~ normal(mu, sigma);
}
EOF
cat data.json > /mnt/stan/models/last/data
cat /mnt/stan/models/last/cost  # "Estimated: 0.00008 ETH (complex model)"
cat /mnt/stan/models/last/run > results.json

# Collaborative document with attribution tracking and automatic compensation
mkdir -p /mnt/collab/papers/quantum-ml
cat ~/research/draft.md > /mnt/collab/papers/quantum-ml/content
echo "shapley" > /mnt/collab/papers/quantum-ml/compensation_model
watch -n 60 cat /mnt/collab/papers/quantum-ml/contributions
# Shows: "alice: 63%, bob: 28%, charlie: 9% (updated 2025-05-14 15:42)"

# Shared canvas for collaborative design with attribution
mount -t figma collab.key /mnt/canvas
echo "mode=realtime" > /mnt/canvas/projects/ui-redesign/settings
cat /mnt/canvas/projects/ui-redesign/contributors
# Shows: "david: 45 elements, emma: 22 elements, frank: 18 elements"
echo "0.0001 ETH" > /mnt/canvas/projects/ui-redesign/bounty/logo-improvement

# Prediction market with model aggregation
mkdir -p /mnt/predmarket/questions/climate
echo "Will Prague exceed 35°C in June 2025?" > /mnt/predmarket/questions/climate/new
echo "0.00005 ETH" > /mnt/predmarket/questions/climate/last/stake
ls /mnt/predmarket/questions/climate/last/predictions
# Shows: claude_model  gpt4_model  human_consensus  llama3_model  metaculus_aggregate

# Set up a DAO for a shared resource
mkdir -p /mnt/daos/neighborhood_solar
cat > /mnt/daos/neighborhood_solar/rules.yaml << EOF
voting:
  threshold: 0.6
  token: "SOLAR"
treasury: "0.03 ETH"
proposals:
  expiry: "7d"
EOF

# Decentralized research funding with quadratic voting
mkdir -p /mnt/quadratic/research/climate
echo "Improved carbon capture via oceanic olivine grinding" > /mnt/quadratic/research/climate/proposals/new
find ~/credentials -name "reputation-*.key" | xargs cat > /mnt/quadratic/research/climate/credentials
echo "5" > /mnt/quadratic/research/climate/votes/olivine
cat /mnt/quadratic/research/climate/matching_pool  # "Current: 0.5 ETH"

# Public goods funding through quadratic matching
echo "0.0001 ETH" > /mnt/commons/projects/openfus/donations/new
cat /mnt/commons/projects/openfus/total
# Shows: "Donations: 0.0042 ETH, Matching: 0.0168 ETH, Total: 0.021 ETH"

# Automated content licensing with fair distribution
echo "fairshare" > /mnt/audio/songs/electronic/licensing_model
cat myproject.mp3 > /mnt/audio/projects/new
cat /mnt/audio/projects/last/samples
# Shows: "3 samples detected: bass_loop_01 (0.00002 ETH), synth_pad_04 (0.00001 ETH), drumkit_09 (0.000005 ETH)"
echo "accept" > /mnt/audio/projects/last/license
echo "0.0001 ETH/download" > /mnt/audio/projects/last/pricing

# Zero-knowledge proof verification for privacy-preserving computations
cat sensitive_data.json | /mnt/zkp/generate tax_computation > proof.zkp
cat proof.zkp > /mnt/tax/submissions/new
cat /mnt/tax/submissions/last/verification  # "Valid proof, tax owed: 0.32 ETH"
```

Slogans
--------

* ¢∘⋈
* ¤⊸⟚
* `data flows, attribution backpropagates, pipes brim`
* `heaven rests if compute is optimally allocated`
