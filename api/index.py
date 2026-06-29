from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default layer
config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

# YAML layer
config.update({
    "port": 8937,
    "log_level": "info",
})

# .env layer
config.update({
    "port": 8340,
    "debug": False,
    "log_level": "error",
    "api_key": "key-1ap39ekxww",
})

# OS env layer
config.update({
    "api_key": "key-d227jlop4o",
})


def parse_bool(v):
    return str(v).lower() in ["true", "1", "yes", "on"]


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    cfg = config.copy()

    for item in set:
        if "=" not in item:
            continue

        k, v = item.split("=", 1)

        if k in ["port", "workers"]:
            cfg[k] = int(v)
        elif k == "debug":
            cfg[k] = parse_bool(v)
        else:
            cfg[k] = v

    cfg["api_key"] = "****"

    return cfg
