# LLM

## The setup

Docker compose:
* Ollama
    * Runs model
    * Model needs to be downloaded, but only once (volume)
    * GPU would be nice
* rest-wrapper
    * Python fastApi, needs to be built
    * Has personality on files (accessible, not just on volume)
    * Is go between for webUI
* WebUI
    * Optional (is big)
    * But nice

# Config info

## Example .env

```bash
# The model Ollama should use
ACTIVE_MODEL=gemma2:2b

# Open WebUI security (put a random string here)
WEBUI_SECRET_KEY=super-secret-key-123
```

## Changing the model

- In .env, change ACTIVE_MODEL
- Docker compose up -d
- You still need to tell Ollama to download the new "brain":

```bash
docker exec -it ollama ollama pull gemma2:2b
```





# Old information


## What You Can Realistically Run

You’re unlikely to run GPT-3.5 or anything close in size unless you're okay with slow responses and reduced context length. However, these options are promising:
Tiny / Small Models (Recommended for Your Use Case)

- [Phi-2 (2.7B)] — Tiny model by Microsoft, fast, very capable for basic pet-style conversation. Runs well on CPU.
- [Gemma 2B (CPU quantized)] — Google's small open model, also good on CPU with quantization.
- [Mistral 7B (quantized)] — Might be pushing it for your CPU, but possible with quantized formats like int4 and llama.cpp.

## Use in Your Robot Pet

Since you just need short bursts of interaction, not long coherent essays:

- You’re golden with a 2–3B model.
- Add some behavior logic around it (“If you see the owner, say something random and cute”).
- Use external scripts for speech-to-text and text-to-speech — e.g. whisper.cpp and piper.
    