import base64
import hashlib
import os
import ecdsa
import requests
from dotenv import load_dotenv
from .models import Order, OrderItems

load_dotenv()
mono_token = os.getenv("MONOBANK_API_KEY")


def create_order(order_data, webhook_url):
    basketOrder = []
    order_items = []
    amount = 0
    order = Order.objects.create(total_price=0)
    for order_item in order_data:
        item_sum = order_item["book_id"].price * order_item["quantity"]
        basketOrder.append(
            {
                "name": order_item["book_id"].title,
                "qty": order_item["quantity"],
                "sum": item_sum,
                "unit": "шт.",
            }
        )
        item = OrderItems.objects.create(
            book=order_item["book_id"], order=order, quantity=order_item["quantity"]
        )
        order_items.append(item)
        amount += item_sum
    order.total_price = amount
    order.save()

    body = {
        "amount": amount,
        "merchantPaymInfo": {
            "reference": str(order.id),
            "basketOrder": basketOrder,
        },
        "webHookUrl": webhook_url,
    }
    request = requests.post(
        "https://api.monobank.ua/api/merchant/invoice/create",
        headers={"X-Token": mono_token},
        json=body,
    )
    request.raise_for_status()
    order.invoice_id = request.json()["invoiceId"]
    order.save()
    url = request.json()["pageUrl"]
    return {"url": url, "id": order.id}


def verify_signature(pub_key_base64, x_sign_base64, body_bytes):
    try:
        pub_key_bytes = base64.b64decode(pub_key_base64)
        signature_bytes = base64.b64decode(x_sign_base64)
        pub_key = ecdsa.VerifyingKey.from_pem(pub_key_bytes.decode())
        ok = pub_key.verify(
            signature_bytes,
            body_bytes,
            sigdecode=ecdsa.util.sigdecode_der,
            hashfunc=hashlib.sha256,
        )
    except Exception:
        return False
    if ok:
        return True
    else:
        return False
