**Environment Setup**
```
uv init
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

```

**Inference with vLLM**
```
python3 -m vllm.entrypoints.openai.api_server     
--model microsoft/Phi-3.5-vision-instruct
--chat-template ./vlm_chat_template.jinja
--trust-remote-code     
--gpu-memory-utilization 0.5     
--max-model-len 1024
--port 8801     
--disable-log-stats

```


```
$ export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

python3 -m vllm.entrypoints.openai.api_server 
--model Qwen/Qwen2.5-VL-3B-Instruct 
--chat-template ./vlm_chat_template.jinja 
--trust-remote-code 
--gpu-memory-utilization 0.5 
--max-model-len 1024 
--max-num-seqs 32 
--max-num-batched-tokens 2048 
--kv-cache-dtype auto 
--port 8801 
--disable-log-stats
```