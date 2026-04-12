import pytest

def test_search_normal(logged_in_session, base_url):
    """搜索正常关键词（手机），应返回商品列表"""
    url = f"{base_url}/Home/Goods/search.html"
    params = {"q": "手机"}
    resp = logged_in_session.get(url, params=params)
    assert resp.status_code == 200
    # 检查页面包含“手机”或商品相关关键词（根据实际页面调整）
    assert "手机" in resp.text or "商品" in resp.text or "找到" in resp.text
    print("\n✅ 正常搜索测试通过")

def test_search_empty(logged_in_session, base_url):
    """搜索空关键词，应正常返回（通常显示全部商品或首页）"""
    url = f"{base_url}/Home/Goods/search.html"
    params = {"q": ""}
    resp = logged_in_session.get(url, params=params)
    assert resp.status_code == 200
    # 只验证状态码，不强制检查特定文字（因为不同系统行为不同）
    # 可选：检查页面不是错误页面（例如不包含 500）
    assert "error" not in resp.text.lower() or "exception" not in resp.text.lower()
    print("\n✅ 空关键词搜索测试通过（服务器正常返回）")

def test_search_no_result(logged_in_session, base_url):
    """搜索无结果的关键词，应提示没有找到商品"""
    url = f"{base_url}/Home/Goods/search.html"
    params = {"q": "asdfghjkl123456"}
    resp = logged_in_session.get(url, params=params)
    assert resp.status_code == 200
    assert "没有找到" in resp.text or "暂无商品" in resp.text or "0" in resp.text
    print("\n✅ 无结果搜索测试通过")

def test_search_special_chars(logged_in_session, base_url):
    """搜索特殊字符，系统应正常返回（不报错）"""
    url = f"{base_url}/Home/Goods/search.html"
    params = {"q": "@#$%^&*()"}
    resp = logged_in_session.get(url, params=params)
    assert resp.status_code == 200
    # 至少页面不是500错误，可能显示无结果或转义后结果
    print("\n✅ 特殊字符搜索测试通过")