import os

class Config:
    max_iters=100
    COMPACT_AT=0.75
    CONTEXT_WINDOW=200000 # fallback when the model's window is unknown
    LLM="openai/gpt-5.2"
    LLM_API_KEY=os.getenv("OPENAI_API_KEY")

config = Config()