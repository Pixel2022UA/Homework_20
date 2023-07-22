# example pubkey, you should receive one at https://api.monobank.ua/api/merchant/pubkey
pub_key_base64 = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZrd0V3WUhLb1pJemowQ0FRWUlLb1pJemowREFRY0RRZ0FFc05mWXpNR1hIM2VXVHkzWnFuVzVrM3luVG5CYgpnc3pXWnhkOStObEtveDUzbUZEVTJONmU0RlBaWmsvQmhqamgwdTljZjVFL3JQaU1EQnJpajJFR1h3PT0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="

# value from X-Sign header in webhook request
x_sign_base64 = "MEQCICPOfmUOGk9pjzEk2uTA2Rd/ZuIomLI+siDbZxdqRBYWAiBj9k1U8vfVhUtMHu0vk+lIpQlK+NZsHZg/t+3FakM3Kw=="

# webhook request body bytes
body_bytes = b"""{"invoiceId":"2307206RBEekJuS8WgEi","status":"success","amount":4200,"ccy":980,"finalAmount":4200,"createdDate":"2023-07-20T17:15:50Z","modifiedDate":"2023-07-20T17:16:53Z","reference":"31"}"""
