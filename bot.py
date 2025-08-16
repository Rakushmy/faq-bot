import os
import json
import pickle
from pathlib import Path
from typing import List, Tuple

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# -------------------- Config --------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY が未設定です。.env か環境変数に設定してください。")

client = OpenAI(api_key=OPENAI_API_KEY)
EMBED_MODEL = "text-embedding-3-small"   # コスパ良し
GEN_MODEL   = "gpt-4o-mini"

DATA_PATH  = Path("data/faqs.json")
INDEX_PATH = Path("data/faqs.index.pkl")

app = FastAPI(title="FAQ Bot", version="0.1.0")

# -------------------- Data/Index --------------------
def load_faqs() -> List[dict]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"{DATA_PATH} が見つかりません。")
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def embed_texts(texts: List[str]) -> np.ndarray:
    # OpenAI からベクトル取得
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = [d.embedding for d in resp.data]
    return np.array(vecs, dtype="float32")

def build_or_load_index(faqs: List[dict]) -> Tuple[np.ndarray, List[dict]]:
    if INDEX_PATH.exists():
        vecs = pickle.loads(INDEX_PATH.read_bytes())
        return vecs, faqs
    # indexが無ければ作成
    corpus = [f"{f['question']} {f['answer']}" for f in faqs]
    vecs = embed_texts(corpus)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_bytes(pickle.dumps(vecs))
    return vecs, faqs

FAQS = load_faqs()
VECS, FAQS = build_or_load_index(FAQS)

# -------------------- Retrieval --------------------
def cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-8)
    b = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-8)
    return a @ b.T

def retrieve(query: str, k: int = 3) -> List[dict]:
    qvec = embed_texts([query])
    sims = cosine_sim(qvec, VECS)[0]  # (N,)
    topk_idx = sims.argsort()[::-1][:k]
    return [FAQS[i] for i in topk_idx]

# -------------------- Generation --------------------
SYS_PROMPT = (
    "あなたは社内FAQアシスタントです。以下のFAQスニペットのみを根拠に、"
    "日本語で簡潔に回答してください。わからない場合は『手元のFAQでは分かりません』と述べてください。"
)

def answer_with_context(query: str, ctx: List[dict]) -> str:
    ctx_text = "\n\n".join([f"- Q: {c['question']}\n  A: {c['answer']}" for c in ctx])
    messages = [
        {"role":"system", "content": SYS_PROMPT},
        {"role":"user", "content": f"質問: {query}\n\n参考FAQ:\n{ctx_text}"}
    ]
    resp = client.chat.completions.create(model=GEN_MODEL, messages=messages)
    return resp.choices[0].message.content.strip()

# -------------------- API --------------------
class AskReq(BaseModel):
    query: str
    top_k: int = 3

class AskRes(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/healthz")
def healthz():
    return {"status": "ok", "faqs": len(FAQS)}

@app.post("/ask", response_model=AskRes)
def ask(req: AskReq):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query は必須です。")
    ctx = retrieve(req.query, k=req.top_k)
    ans = answer_with_context(req.query, ctx)
    return AskRes(answer=ans, sources=ctx)
