from functools import wraps
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = Sanic(__name__)

public_key = "pub key here"


def verify_key(
    raw_body: str, signature: str, timestamp: str, client_public_key: str
) -> bool:
    message = timestamp.encode() + raw_body
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False


def verified():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            signature = request.headers.get("X-Signature-Ed25519")
            timestamp = request.headers.get("X-Signature-Timestamp")
            is_verified = verify_key(request.body, signature, timestamp, public_key)

            if is_verified:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({"status": 401, "message": "not_verified"}, 401)

        return decorated_function

    return decorator


@app.post("/")
@verified()
async def _main_route(request: Request):
    if request.json["type"] == 1:
        return json({"type": 1})
    else:
        import hiyobi

        value = request.json["data"]["options"][0]["value"]

        hiyobi_cls = hiyobi.HiyobiExt()

        info = await hiyobi_cls.info_embed(value)

        return json({"type": 4, "data": {"embeds": [info.to_dict()]}})


app.run("0.0.0.0")