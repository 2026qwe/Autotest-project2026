import pytest
import random
import time

# ---------- 模块内 fixture（函数级别） ----------
@pytest.fixture
def register_prepared_session(anonymous_session, base_url):
    """
    执行注册前的所有 GET 请求（访问注册页、两个验证码接口），
    返回一个已经初始化好的 session（包含必要的 Cookie）。
    每个测试用例都会独立调用此 fixture，保证隔离。
    """
    # 1. 访问注册页面
    reg_page_url = f"{base_url}/index.php/Home/User/reg.html"
    anonymous_session.get(reg_page_url)

    # 2. 请求验证码接口（type/user_reg.html）
    verify_type_url = f"{base_url}/index.php/Home/User/verify/type/user_reg.html"
    anonymous_session.get(verify_type_url)

    # 3. 请求验证码接口（a=verify）
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)

    return anonymous_session

# ---------- 辅助函数 ----------
def generate_unique_mobile():
    """生成唯一手机号（基于时间戳+随机数）"""
    timestamp = int(time.time() * 1000) % 100000000
    suffix = random.randint(100, 999)
    return f"159{timestamp}{suffix}"[:11]

# ---------- 测试用例 ----------
def test_register_success(register_prepared_session, base_url):
    """正常注册（使用动态手机号）"""
    mobile = generate_unique_mobile()
    data = {
        "scene": 1,
        "username": mobile,
        "verify_code": "8888",
        "password": "aa123456",
        "password2": "aa123456",
        "invite": ""
    }
    reg_url = f"{base_url}/index.php/Home/User/reg.html"
    headers = {"Referer": f"{base_url}/index.php/Home/user/reg.html"}
    resp = register_prepared_session.post(reg_url, data=data, headers=headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] == 1
    assert result["msg"] == "注册成功"
    assert "user_id" in result["result"]
    assert "token" in result["result"]
    # 注册成功后会设置 user_id cookie
    assert "user_id" in register_prepared_session.cookies
    assert register_prepared_session.cookies.get("user_id") == str(result["result"]["user_id"])
    print(f"\n✅ 注册成功，手机号: {mobile}，用户ID: {result['result']['user_id']}")

def test_register_duplicate_mobile(register_prepared_session, base_url):
    """使用已存在的手机号（例如 15966661234）"""
    data = {
        "scene": 1,
        "username": "15966661234",
        "verify_code": "8888",
        "password": "aa123456",
        "password2": "aa123456",
        "invite": ""
    }
    reg_url = f"{base_url}/index.php/Home/User/reg.html"
    headers = {"Referer": f"{base_url}/index.php/Home/user/reg.html"}
    resp = register_prepared_session.post(reg_url, data=data, headers=headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    # 根据实际错误消息调整关键词
    msg = result.get("msg", "")
    assert "手机" in msg or "已存在" in msg
    print(f"\n✅ 重复手机号测试通过: {msg}")

def test_register_wrong_verify_code(register_prepared_session, base_url):
    """验证码错误（输入 0000）"""
    mobile = generate_unique_mobile()
    data = {
        "scene": 1,
        "username": mobile,
        "verify_code": "0000",
        "password": "aa123456",
        "password2": "aa123456",
        "invite": ""
    }
    reg_url = f"{base_url}/index.php/Home/User/reg.html"
    headers = {"Referer": f"{base_url}/index.php/Home/user/reg.html"}
    resp = register_prepared_session.post(reg_url, data=data, headers=headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    assert "验证码" in result.get("msg", "")
    print(f"\n✅ 验证码错误测试通过: {result.get('msg')}")

def test_register_password_mismatch(register_prepared_session, base_url):
    """两次输入的密码不一致"""
    mobile = generate_unique_mobile()
    data = {
        "scene": 1,
        "username": mobile,
        "verify_code": "8888",
        "password": "aa123456",
        "password2": "different",
        "invite": ""
    }
    reg_url = f"{base_url}/index.php/Home/User/reg.html"
    headers = {"Referer": f"{base_url}/index.php/Home/user/reg.html"}
    resp = register_prepared_session.post(reg_url, data=data, headers=headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    msg = result.get("msg", "")
    assert "密码" in msg and "一致" in msg
    print(f"\n✅ 密码不一致测试通过: {msg}")

def test_register_missing_username(register_prepared_session, base_url):
    """用户名为空"""
    data = {
        "scene": 1,
        "username": "",
        "verify_code": "8888",
        "password": "aa123456",
        "password2": "aa123456",
        "invite": ""
    }
    reg_url = f"{base_url}/index.php/Home/User/reg.html"
    headers = {"Referer": f"{base_url}/index.php/Home/user/reg.html"}
    resp = register_prepared_session.post(reg_url, data=data, headers=headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 用户名为空测试通过: {result.get('msg')}")

def test_register_missing_password(register_prepared_session, base_url):
    """密码为空"""
    mobile = generate_unique_mobile()
    data = {
        "scene": 1,
        "username": mobile,
        "verify_code": "8888",
        "password": "",
        "password2": "",
        "invite": ""
    }
    reg_url = f"{base_url}/index.php/Home/User/reg.html"
    headers = {"Referer": f"{base_url}/index.php/Home/user/reg.html"}
    resp = register_prepared_session.post(reg_url, data=data, headers=headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 密码为空测试通过: {result.get('msg')}")