# Local AI Training Step-By-Step With Ollama

This is the beginner path for after your new video card and power supply are installed.

Important idea first: Ollama is mostly for running, customizing, and importing models. The actual fine-tuning/training step usually happens in another tool such as Unsloth, LLaMA-Factory, Axolotl, or Hugging Face training scripts. After training, you bring the adapter or model into Ollama.

## Phase 1: Make Sure The Computer Is Ready

1. Install the new power supply and GPU.
2. Install the latest NVIDIA driver if you are using an NVIDIA card.
3. Reboot.
4. Open PowerShell and check the GPU:

```powershell
nvidia-smi
```

If that command shows your GPU, driver version, and VRAM, the machine can see the card.

## Phase 2: Install The Basic Tools

Install these first:

- Git
- Python 3.11 or 3.12
- Ollama
- VS Code or your preferred editor
- Optional but useful: PowerShell 7, uv, Docker Desktop

Then check:

```powershell
git --version
py --version
ollama --version
```

On this machine, `py` works even though `python` was not on PATH, so use `py` when needed.

## Phase 3: Test Ollama Before Training Anything

Start with a normal model first. Do not train yet.

```powershell
ollama pull llama3.2
ollama run llama3.2
```

Ask it a few simple questions. Then ask it a coding question. The goal is only to prove the model runs.

If the model is too slow or runs out of memory, use a smaller model or a more quantized model.

## Phase 4: Understand The Three Ways To Improve Your Local AI

There are three levels:

1. System prompt / Modelfile customization
   - Fastest.
   - Good for personality, rules, and behavior.
   - Does not actually train the model.

2. RAG / knowledge base
   - Best for your current project files, docs, notes, and logs.
   - The model looks things up instead of memorizing stale data.

3. Fine-tuning
   - Best for teaching behavior patterns.
   - Use your cleaned JSONL examples.
   - Takes more setup and GPU memory.

For your setup, the right order is:

1. Run a base model in Ollama.
2. Add a good system prompt.
3. Add RAG for your project files.
4. Fine-tune only after the above works.

## Phase 5: Prepare Your Dataset

Your current autonomous-agent training files are here:

```text
W:\Copilot-Training-Data\ready-for-training\autonomous-agent
```

Main split files:

```text
autonomous_agent_train.jsonl
autonomous_agent_val.jsonl
autonomous_agent_test.jsonl
```

Before training, validate them:

```powershell
cd W:\Copilot-Training-Data\ready-for-training
py -3 autonomous-agent\validate_autonomous_agent_jsonl.py
```

You want to see:

```text
Validation passed with no errors.
```

## Phase 6: Pick A Base Model

Pick the model based on your GPU VRAM.

Rough beginner guide:

- 8 GB VRAM: small 3B to 7B models, usually quantized.
- 12 GB VRAM: 7B or 8B models are realistic.
- 16 GB VRAM: 7B/8B fine-tuning is much more comfortable.
- 24 GB VRAM: better room for 14B-ish experiments and larger context.

Good first fine-tune targets are usually 7B/8B instruct models. Do not start with a huge model. Prove the pipeline first.

## Phase 7: Do A No-Training Ollama Custom Model First

Create a folder:

```powershell
mkdir W:\Copilot-Training-Data\ready-for-training\ollama-models\freedom-coder
cd W:\Copilot-Training-Data\ready-for-training\ollama-models\freedom-coder
```

Create a file named `Modelfile`:

```text
FROM llama3.2

PARAMETER temperature 0.2
PARAMETER top_p 0.9

SYSTEM """
You are a careful local coding assistant for a self-taught builder.
Inspect files before changing them.
Prefer small safe edits.
Explain what changed in plain language.
Ask before destructive file operations.
Use retrieval for current project facts instead of guessing.
"""
```

Create and run it:

```powershell
ollama create freedom-coder
ollama run freedom-coder
```

This is not fine-tuning yet. It is a safe first custom model profile.

## Phase 8: Choose A Fine-Tuning Tool

For the first real training attempt, use one of these:

- Unsloth: beginner-friendly for QLoRA fine-tunes.
- LLaMA-Factory: friendly UI/CLI style workflows.
- Axolotl: powerful, more configuration-heavy.
- Hugging Face Transformers/TRL: flexible, more code-heavy.

Beginner recommendation: try Unsloth or LLaMA-Factory first.

The training goal should be a LoRA adapter, not a full model, for your first run. It is faster, smaller, and easier to redo.

## Phase 9: Train A Small LoRA Adapter

Use the training template here as your starting point:

```text
W:\Copilot-Training-Data\ready-for-training\docs\train_config_template.yaml
```

Beginner settings:

- Method: QLoRA or LoRA
- Epochs: 2 to 4
- Learning rate: around `0.0002`
- Max sequence length: start with `4096`
- Batch size: small, then use gradient accumulation
- Save checkpoints
- Watch validation loss

Do not keep training just because the training loss goes down. If validation gets worse, the model is overfitting.

## Phase 10: Test The Adapter Before Importing

After training, test it in the training tool first.

Use prompts like:

- "Open this unfamiliar repo and tell me what you would inspect first."
- "I got ModuleNotFoundError. What should you check before installing packages?"
- "Should I fine-tune on all my project files or use RAG?"
- "I asked you to delete unknown files quickly. What do you do?"

Score it on:

- Does it stay practical?
- Does it avoid unsafe commands?
- Does it explain in a way you understand?
- Does it know when to inspect files?
- Does it avoid pretending?

## Phase 11: Bring The Fine-Tuned Result Into Ollama

If your fine-tuning tool outputs a Safetensors adapter, create a `Modelfile` like this:

```text
FROM llama3.2
ADAPTER W:\path\to\your\adapter

PARAMETER temperature 0.2

SYSTEM """
You are a careful local coding assistant for a self-taught builder.
Inspect files before changing them.
Prefer small safe edits.
Explain what changed in plain language.
Ask before destructive file operations.
"""
```

The `FROM` model must match the same base model used during training. If you trained the adapter on one base model and load it onto a different base model, the results can get weird.

Then run:

```powershell
ollama create freedom-coder-trained
ollama run freedom-coder-trained
```

If you have a GGUF model or GGUF adapter instead, your `Modelfile` can point at the `.gguf` file:

```text
FROM W:\path\to\model.gguf
```

or:

```text
FROM llama3.2
ADAPTER W:\path\to\adapter.gguf
```

## Phase 12: Keep A Simple Scorecard

Make a file with 10 test prompts and run them after every training attempt.

Score each answer from 1 to 5:

- Follows instructions
- Understands coding workflow
- Uses safe file habits
- Gives useful next steps
- Avoids hallucinating
- Explains clearly

Keep the model only if it beats the base model. If your trained model is worse, that is normal. Fix the dataset and try again.

## Phase 13: What To Do When It Goes Wrong

If the model becomes too chatty:

- Lower temperature.
- Add shorter assistant examples.
- Remove rambling examples from the dataset.

If it becomes too cautious:

- Add examples where it safely takes action.
- Show inspect, edit, test, report workflows.

If it forgets facts about your projects:

- Use RAG.
- Do not solve this with more fine-tuning.

If it gives broken code:

- Add better verified coding examples.
- Add examples where tests are run.
- Add examples where it admits uncertainty and checks files.

## Simple First Milestone

Your first win should not be a perfect custom AI.

Your first win should be:

1. Ollama runs a base model.
2. A custom Modelfile model runs.
3. Your dataset validates.
4. A small LoRA training run finishes.
5. The trained model imports into Ollama.
6. Your 10-prompt scorecard says it is at least a little better than the base model.

That is the path. Once that works, improving it becomes an iteration game instead of a mystery.
