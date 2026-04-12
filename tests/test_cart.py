import pytest
import re

# ==================== 添加购物车 ====================
ADD_CART_DATA = {
    "goods_id": 46,
    "goods_prom_type": 0,
    "shop_price": "999.00",
    "store_count": 123,
    "market_price": "1099.00",
    "start_time": "",
    "end_time": "",
    "activity_title": "",
    "prom_detail": "",
    "activity_is_on": "",
    "item_id": 70,
    "exchange_integral": 0,
    "point_rate": 1,
    "is_virtual": 0,
    "goods_spec[网络]": "11",
    "goods_spec[内存]": "13",
    "goods_spec[屏幕]": "21",
    "goods_num": 1,
    "goods_id": 46
}

def test_add_cart_success(logged_in_session, base_url):
    """正常添加商品到购物车"""
    url = f"{base_url}/index.php?m=Home&c=Cart&a=ajaxAddCart"
    resp = logged_in_session.post(url, data=ADD_CART_DATA)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == 1
    assert data["msg"] == "成功加入购物车"
    print(f"\n✅ 添加购物车成功，购物车数量: {data.get('result', 'unknown')}")

def test_add_cart_missing_goods_id(logged_in_session, base_url):
    """缺少商品ID"""
    url = f"{base_url}/index.php?m=Home&c=Cart&a=ajaxAddCart"
    data = ADD_CART_DATA.copy()
    del data["goods_id"]
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 缺少商品ID测试通过: {result.get('msg')}")

def test_add_cart_missing_goods_num(logged_in_session, base_url):
    """缺少商品数量"""
    url = f"{base_url}/index.php?m=Home&c=Cart&a=ajaxAddCart"
    data = ADD_CART_DATA.copy()
    del data["goods_num"]
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 缺少商品数量测试通过: {result.get('msg')}")

def test_add_cart_invalid_goods_id(logged_in_session, base_url):
    """无效商品ID"""
    url = f"{base_url}/index.php?m=Home&c=Cart&a=ajaxAddCart"
    data = ADD_CART_DATA.copy()
    data["goods_id"] = 999999
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 无效商品ID测试通过: {result.get('msg')}")

def test_add_cart_duplicate(logged_in_session, base_url):
    """重复添加同一商品，购物车数量应累加"""
    url = f"{base_url}/index.php?m=Home&c=Cart&a=ajaxAddCart"
    # 第一次添加
    resp1 = logged_in_session.post(url, data=ADD_CART_DATA)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["status"] == 1
    # 第二次添加
    resp2 = logged_in_session.post(url, data=ADD_CART_DATA)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["status"] == 1
    # 验证数量增加（如果服务器返回的是总数量）
    if "result" in data1 and "result" in data2:
        assert int(data2["result"]) >= int(data1["result"])
    print(f"\n✅ 重复添加测试通过，第一次数量: {data1.get('result')}, 第二次: {data2.get('result')}")

# ==================== 查看购物车 ====================
def test_cart_full_page(logged_in_session, base_url):
    """访问完整购物车页面 /Home/Cart/index.html"""
    url = f"{base_url}/Home/Cart/index.html"
    resp = logged_in_session.get(url)
    assert resp.status_code == 200
    assert "购物车" in resp.text or "cart" in resp.text.lower()
    print("\n✅ 完整购物车页面可访问")

def test_cart_header_list(logged_in_session, base_url):
    """获取头部购物车列表（下拉菜单）"""
    url = f"{base_url}/index.php?m=Home&c=Cart&a=header_cart_list"
    resp = logged_in_session.get(url)
    assert resp.status_code == 200
    assert "cart" in resp.text.lower() or "购物车" in resp.text
    print("\n✅ 头部购物车列表可访问")

# ==================== 更新购物车 ====================
def get_first_cart_item_id(session, base_url):
    """从头部购物车列表中提取第一个商品的ID"""
    url = f"{base_url}/index.php?m=Home&c=Cart&a=header_cart_list"
    resp = session.get(url)
    assert resp.status_code == 200
    match = re.search(r'data-id="(\d+)"', resp.text)
    if not match:
        match = re.search(r'id="cart_item_(\d+)"', resp.text)
    if match:
        return match.group(1)
    return None

def test_update_cart_normal(logged_in_session, base_url):
    """正常更新购物车商品数量（需购物车非空）"""
    item_id = get_first_cart_item_id(logged_in_session, base_url)
    if item_id is None:
        pytest.skip("购物车为空，无法测试正常更新，请先添加商品到购物车")
    url = f"{base_url}/Home/Cart/AsyncUpdateCart.html"
    data = {
        "cart[0][id]": item_id,
        "cart[0][goods_num]": 1,
        "cart[0][selected]": 1
    }
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] == 1
    assert result["msg"] == "计算成功"
    print(f"\n✅ 更新购物车成功，新数量: {result['result']['goods_num']}")

def test_update_cart_missing_params(logged_in_session, base_url):
    """更新购物车时缺少必要参数"""
    url = f"{base_url}/Home/Cart/AsyncUpdateCart.html"
    resp = logged_in_session.post(url, data={})
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 缺少参数测试通过: {result.get('msg')}")

def test_update_cart_invalid_id(logged_in_session, base_url):
    """使用不存在的购物车项ID"""
    url = f"{base_url}/Home/Cart/AsyncUpdateCart.html"
    data = {
        "cart[0][id]": 999999,
        "cart[0][goods_num]": 1,
        "cart[0][selected]": 1
    }
    resp = logged_in_session.post(url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 无效ID测试通过: {result.get('msg')}")