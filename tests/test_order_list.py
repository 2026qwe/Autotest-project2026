import pytest
import re

def test_order_list_page(logged_in_session, base_url):
    """访问订单列表页面，验证可访问"""
    url = f"{base_url}/Home/Order/order_list.html"
    resp = logged_in_session.get(url)
    assert resp.status_code == 200
    assert "订单" in resp.text or "order" in resp.text.lower()
    print("\n✅ 订单列表页面可访问")

def test_order_list_has_orders(logged_in_session, base_url):
    """验证订单列表中至少有一个订单（显示订单号）"""
    url = f"{base_url}/Home/Order/order_list.html"
    resp = logged_in_session.get(url)
    assert resp.status_code == 200
    # 匹配至少15位数字的订单号（避免匹配其他数字）
    matches = re.findall(r'\b\d{15,}\b', resp.text)
    assert len(matches) > 0, "订单列表为空，请先执行下单测试"
    print(f"\n✅ 订单列表包含订单，示例订单号: {matches[0]}")

def test_order_detail_link(logged_in_session, base_url):
    """验证订单详情链接可访问（取第一个订单）"""
    url = f"{base_url}/Home/Order/order_list.html"
    resp = logged_in_session.get(url)
    assert resp.status_code == 200
    # 精确匹配订单详情链接：包含 order_detail 和 order_id
    match = re.search(r'href="([^"]*order_detail[^"]*order_id=\d+[^"]*)"', resp.text)
    if not match:
        pytest.skip("未找到订单详情链接")
    detail_path = match.group(1)
    if detail_path.startswith('/'):
        detail_url = base_url + detail_path
    else:
        detail_url = detail_path
    resp2 = logged_in_session.get(detail_url)
    assert resp2.status_code == 200
    # 检查页面包含订单号或订单详情相关文字
    assert "订单号" in resp2.text or "订单详情" in resp2.text or "订单信息" in resp2.text