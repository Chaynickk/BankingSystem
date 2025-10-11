#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install httpx colorama uvloop  (uvloop опционален на *nix)

import asyncio
import random
import time
import uuid
from dataclasses import dataclass
from typing import Dict, Any, List

import httpx
from colorama import init as colorama_init, Fore, Style

# ---------- конфиг под твой API ----------
API_URL = "http://127.0.0.1:8000"  # поменяй при надобности

CLIENT_LOGIN = "/client/login"               # POST json: {username, password}
CLIENT_REG   = "/client/registration"        # POST json: {...}
ACC_GET      = "/account/get"                # GET Bearer
ACC_REG      = "/account/registration"       # POST Bearer
ACC_DEL      = "/account/del?account_id="    # DELETE Bearer + query
ACC_TX       = "/account/transaction"        # PUT Bearer json: {money, from_account_id, to_account_id}

USERS_TOTAL  = 300          # сколько виртуальных юзеров
CONCURRENCY  = 100          # одновременных
RAMP_UP_SEC  = 15           # разгон нагрузки
HTTP_TIMEOUT = 10.0         # сек
DO_REGISTER  = True         # делать ли регистрацию
DO_TX        = True         # делать ли перевод

VERBOSE_FIRST_N = 8         # сколько юзеров распечатывать подробно
SHOW_BODIES_422 = 3         # показать примеры 422

# ---------- утилиты ----------
colorama_init()

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *exc):
        self.dt = time.perf_counter() - self.start

def percentiles(values: List[float], ps=(50, 95, 99)):
    if not values:
        return {p: float("nan") for p in ps}
    xs = sorted(values)
    out = {}
    for p in ps:
        k = (len(xs)-1) * (p/100)
        f, c = int(k), min(int(k)+1, len(xs)-1)
        out[p] = xs[f] if f == c else xs[f] + (xs[c]-xs[f])*(k-f)
    return out

@dataclass
class Metrics:
    ok: int = 0
    err: int = 0
    lat: List[float] = None
    codes: Dict[int, int] = None
    total_requests: int = 0
    success_requests: int = 0
    seen_422: int = 0
    seen_422_req: int = 0

    def __post_init__(self):
        self.lat = []
        self.codes = {}

def good(msg: str):  print(Fore.GREEN + msg + Style.RESET_ALL)
def bad(msg: str):   print(Fore.RED   + msg + Style.RESET_ALL)
def info(msg: str):  print(Fore.CYAN  + msg + Style.RESET_ALL)

# ---------- обёртки запросов (async, json only) ----------
async def post_json(client: httpx.AsyncClient, url: str, json: dict, headers: dict = None):
    with Timer() as t:
        r = await client.post(url, json=json, headers=headers)
    return r, t.dt

async def put_json(client: httpx.AsyncClient, url: str, json: dict, headers: dict = None):
    with Timer() as t:
        r = await client.put(url, json=json, headers=headers)
    return r, t.dt

async def get(client: httpx.AsyncClient, url: str, headers: dict = None):
    with Timer() as t:
        r = await client.get(url, headers=headers)
    return r, t.dt

async def delete(client: httpx.AsyncClient, url: str, headers: dict = None):
    with Timer() as t:
        r = await client.delete(url, headers=headers)
    return r, t.dt

# ---------- шаги сценария ----------
async def step_register(client, seed):
    data = {
        "first_name":  "Test",
        "last_name":   f"User{seed}",
        "email":       f"user{seed}@test.local",
        "phone_number": f"+79{random.randint(108, 109-1)}",
        "password":    "pass1237777777777777777!",
        "patronymic":  None
    }
    return await post_json(client, API_URL + CLIENT_REG, json=data)

async def step_login(client, seed):
    data = {"username": f"user{seed}@test.local", "password": "pass123!"}
    return await post_json(client, API_URL + CLIENT_LOGIN, json=data)

async def step_get_accounts(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    return await get(client, API_URL + ACC_GET, headers=headers)
async def step_tx(client, token, from_id, to_id, money):
    headers = {"Authorization": f"Bearer {token}"}
    body = {"money": int(money), "from_account_id": int(from_id), "to_account_id": int(to_id)}
    return await put_json(client, API_URL + ACC_TX, json=body, headers=headers)

# ---------- worker ----------
async def user_flow(i: int, sema: asyncio.Semaphore, client: httpx.AsyncClient, m: Metrics):
    seed = uuid.uuid4().hex[:10] + f"{i:04d}"

    async with sema:
        # 1) регистрация (опц.)
        if DO_REGISTER:
            r, dt = await step_register(client, seed)
            m.lat.append(dt); m.codes[r.status_code] = m.codes.get(r.status_code,0)+1; m.total_requests += 1
            if r.status_code != 200 and r.status_code != 201:
                m.err += 1
                if r.status_code == 422 and m.seen_422 < SHOW_BODIES_422:
                    m.seen_422 += 1
                    bad(f"[422] POST {CLIENT_REG} in {dt:.3f}s -> {r.text}")
                else:
                    bad(f"[x] POST {CLIENT_REG} in {dt:.3f}s -> {r.status_code}")
                return
            else:
                m.success_requests += 1
                if i < VERBOSE_FIRST_N:
                    good(f"[{i}] POST {CLIENT_REG} in {dt:.3f}s")

        # 2) логин
        r, dt = await step_login(client, seed)
        m.lat.append(dt); m.codes[r.status_code] = m.codes.get(r.status_code,0)+1; m.total_requests += 1
        if r.status_code != 200:
            m.err += 1
            bad(f"[x] POST {CLIENT_LOGIN} in {dt:.3f}s -> {r.status_code} {r.text[:120]}")
            return
        m.success_requests += 1
        token = (r.json().get("access_token") or r.json().get("token") or "").strip()
        if i < VERBOSE_FIRST_N: good(f"[{i}] POST {CLIENT_LOGIN} in {dt:.3f}s (token len {len(token)})")

        # 3) получить счета
        r, dt = await step_get_accounts(client, token)
        m.lat.append(dt); m.codes[r.status_code] = m.codes.get(r.status_code,0)+1; m.total_requests += 1
        if r.status_code != 200:
            m.err += 1
            bad(f"[x] GET  {ACC_GET} in {dt:.3f}s -> {r.status_code}")
            return
        m.success_requests += 1
        accounts = r.json() if r.headers.get("content-type","").startswith("application/json") else []
        if i < VERBOSE_FIRST_N: good(f"[{i}] GET  {ACC_GET} in {dt:.3f}s (n={len(accounts)})")

        # 4) транзакция (опц.)
        if DO_TX and isinstance(accounts, list) and len(accounts) >= 2:
            a = accounts[0].get("id", 1)
            b = accounts[1].get("id", 2)
            r, dt = await step_tx(client, token, a, b, money=10)
            m.lat.append(dt); m.codes[r.status_code] = m.codes.get(r.status_code,0)+1; m.total_requests += 1
            if r.status_code not in (200, 201):
                m.err += 1
                bad(f"[x] PUT  {ACC_TX} in {dt:.3f}s -> {r.status_code}")
                return
            m.success_requests += 1
            if i < VERBOSE_FIRST_N: good(f"[{i}] PUT  {ACC_TX} in {dt:.3f}s")

        m.ok += 1  # сценарий прошёл

# ---------- runner ----------
async def main():
    # optional: ускоряшка на *nix
    try:
        import uvloop, asyncio as _a; _a.set_event_loop_policy(uvloop.EventLoopPolicy())
    except Exception:
        pass

    limits = httpx.Limits(max_connections=CONCURRENCY, max_keepalive_connections=CONCURRENCY)
    timeout = httpx.Timeout(HTTP_TIMEOUT)

    m = Metrics()
    sema = asyncio.Semaphore(CONCURRENCY)

    info(f"Start load: users={USERS_TOTAL}, conc={CONCURRENCY}, ramp={RAMP_UP_SEC}s -> {API_URL}")

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        tasks = []
        for i in range(USERS_TOTAL):
            delay = (RAMP_UP_SEC * i) / max(1, USERS_TOTAL - 1)
            async def delayed(ii=i, d=delay):
                if d: await asyncio.sleep(d)
                await user_flow(ii, sema, client, m)
            tasks.append(asyncio.create_task(delayed()))
        t0 = time.perf_counter()
        await asyncio.gather(*tasks)
        total_time = time.perf_counter() - t0

        # ---- сводка
    p = percentiles(m.lat)
    success_pct = 100.0 * m.success_requests / max(m.total_requests, 1)
    error_pct = 100.0 - success_pct
    rps = m.total_requests / max(total_time, 1e-9)

    print("\n===== RESULTZ =====")
    print(f"Users total       : {USERS_TOTAL}")
    print(f"Concurrency       : {CONCURRENCY}")
    print(f"Ramp-up (s)       : {RAMP_UP_SEC}")
    print(f"Duration (s)      : {total_time:.2f}")
    print(f"Requests total    : {m.total_requests}")
    (good if success_pct >= 99 else bad)(f"Success / Error % : {success_pct:.1f}% / {error_pct:.1f}%")
    print(f"RPS (approx)      : {rps:.1f}")
    if m.lat:
        print(
            f"Latency (s)       : min {min(m.lat):.3f}  "
            f"p50 {p[50]:.3f}  p95 {p[95]:.3f}  p99 {p[99]:.3f}  max {max(m.lat):.3f}"
        )
    codes_str = ", ".join(f"{k}:{v}" for k, v in sorted(m.codes.items()))
    print(f"HTTP codes        : {codes_str}")
    print("===================\n")


if __name__ == "__main__":
    asyncio.run(main())