import pytest
import requests
import random

BASE_URL = "http://www.myshop.com"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def test_user():
    """登录用的测试账号"""
    return {
        "username": "15866661234",
        "password": "aa123456",
        "verify_code": "8888"
    }

@pytest.fixture(scope="session")
def order_data():
    """下单用的基础参数（需要根据实际情况调整）"""
    return {
        "action": "buy_now",
        "goods_id": 65,
        "item_id": 122,
        "goods_num": 1,
        "address_id": 829,
        "invoice_desc": "不开发票",
        "couponTypeSelect": 1,
        "coupon_id": 0,
        "couponCode": "",
        "shipping_code": "shentong",
        "user_note": "",
        "paypwd": "",
        "user_money": "",
        "pay_points": "",
        "act": "submit_order"
    }

@pytest.fixture
def anonymous_session():
    """每个测试独立的新会话（无任何预置 Cookie，但会添加基础请求头）"""
    sess = requests.Session()
    sess.trust_env = False          # 忽略环境变量中的代理
    sess.proxies = {}               # 清空代理设置
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Origin": BASE_URL,
    })
    # 预先设置一些固定的 Cookie（从手动抓包中提取）
    sess.cookies.set("province_id", "1")
    sess.cookies.set("city_id", "2")
    sess.cookies.set("district_id", "3")
    sess.cookies.set("admin_type", "1")
    sess.cookies.set("is_distribut", "1")
    sess.cookies.set("cn", "0")
    # 统计类 Cookie 可选，但为了模拟完整，也加上
    sess.cookies.set("Hm_lvt_7d86eb847ecfd3c972fa457a6abaa0da", "1775984203")
    sess.cookies.set("HMACCOUNT", "00FD03D31DD8CD65")
    sess.cookies.set("Hm_lpvt_7d86eb847ecfd3c972fa457a6abaa0da", "1775984394")
    return sess

@pytest.fixture
def logged_in_session(anonymous_session, base_url, test_user):
    """已登录的会话（供后续依赖登录的测试使用）"""
    # 请求验证码接口
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)
    # 登录
    login_url = f"{base_url}/index.php?m=Home&c=User&a=do_login"
    resp = anonymous_session.post(login_url, data=test_user)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == 1, f"登录失败: {data.get('msg')}"
    return anonymous_session