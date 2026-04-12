import pytest
import re

def get_first_address_id(session, base_url):
    """从地址列表页面解析第一个地址的ID（用于后续操作）"""
    url = f"{base_url}/Home/User/address_list.html"
    resp = session.get(url)
    assert resp.status_code == 200
    # 在HTML中查找地址ID，通常格式：data-id="123" 或 id="address_123"
    match = re.search(r'data-id="(\d+)"', resp.text)
    if not match:
        match = re.search(r'id="address_(\d+)"', resp.text)
    if match:
        return match.group(1)
    return None

def test_address_list_page(logged_in_session, base_url):
    """访问地址列表页面，验证可访问"""
    url = f"{base_url}/Home/User/address_list.html"
    resp = logged_in_session.get(url)
    assert resp.status_code == 200
    assert "地址" in resp.text or "address" in resp.text.lower()
    print("\n✅ 地址列表页面可访问")

def test_add_address_success(logged_in_session, base_url):
    """正常新增地址"""
    url = f"{base_url}/index.php?m=Home&c=User&a=add_address&scene=1&call_back=call_back_fun"
    data = {
        "consignee": "李刚",
        "province": 1,
        "city": 2,
        "district": 14,
        "twon": 15,
        "address": "一号",
        "zipcode": "",
        "mobile": "15866661234"
    }
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    # 成功时响应包含 call_back_fun('success')
    assert "call_back_fun('success')" in resp.text
    print("\n✅ 新增地址成功")

def test_add_address_missing_consignee(logged_in_session, base_url):
    """缺少收货人姓名，预期失败并提示“收货人不能为空”"""
    url = f"{base_url}/index.php?m=Home&c=User&a=add_address&scene=1&call_back=call_back_fun"
    data = {
        "consignee": "",
        "province": 1,
        "city": 2,
        "district": 14,
        "twon": 15,
        "address": "一号",
        "zipcode": "",
        "mobile": "15866661234"
    }
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    assert "收货人不能为空" in resp.text
    print("\n✅ 缺少收货人测试通过")

def test_add_address_missing_mobile(logged_in_session, base_url):
    """缺少手机号，预期失败并提示“手机号码格式有误”"""
    url = f"{base_url}/index.php?m=Home&c=User&a=add_address&scene=1&call_back=call_back_fun"
    data = {
        "consignee": "李刚",
        "province": 1,
        "city": 2,
        "district": 14,
        "twon": 15,
        "address": "一号",
        "zipcode": "",
        "mobile": ""
    }
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    assert "手机号码格式有误" in resp.text
    print("\n✅ 缺少手机号测试通过")