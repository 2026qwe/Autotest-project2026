import pytest
import re

def get_latest_order_id(session, base_url):
    """从订单列表页面获取第一个订单的ID（简单正则）"""
    url = f"{base_url}/Home/Order/order_list.html"
    resp = session.get(url)
    if resp.status_code != 200:
        return None
    # 匹配 order_id=数字
    match = re.search(r'order_id=(\d+)', resp.text)
    return match.group(1) if match else None

@pytest.fixture
def payment_order_id(logged_in_session, base_url):
    order_id = get_latest_order_id(logged_in_session, base_url)
    if not order_id:
        pytest.skip("没有找到可支付的订单，请先执行下单测试")
    return order_id

def test_payment_page_access(logged_in_session, base_url, payment_order_id):
    """访问支付页面，只验证状态码和页面包含基本内容"""
    url = f"{base_url}/index.php/Home/Payment/getCode.html"
    data = {
        "pay_radio": "pay_code=alipay",
        "master_order_sn": "",
        "order_id": payment_order_id
    }
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    # 不强制检查具体文本，只确保不是错误页面（例如不包含“系统错误”）
    assert "系统错误" not in resp.text
    print(f"\n✅ 支付页面访问成功，订单号: {payment_order_id}")

def test_payment_missing_order_id(logged_in_session, base_url):
    """缺少订单ID，应返回错误或正常页面（只验证不崩溃）"""
    url = f"{base_url}/index.php/Home/Payment/getCode.html"
    data = {
        "pay_radio": "pay_code=alipay",
        "master_order_sn": "",
        "order_id": ""
    }
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    # 至少保证不是500错误
    print("\n✅ 缺少订单ID测试通过，服务器正常响应")