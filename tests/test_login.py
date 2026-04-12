import pytest
import random

# 注意：test_login_all_fields_empty 故意使用未定义的 BASE_URL，会引发 NameError，作为教学案例保留。

def test_login_success(anonymous_session, base_url, test_user):
    """正确账号、密码、验证码 -> 登录成功"""
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)
    login_url = f"{base_url}/index.php?m=Home&c=User&a=do_login"
    resp = anonymous_session.post(login_url, data=test_user)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == 1
    assert data["msg"] == "登陆成功"
    assert "user_id" in data["result"]
    assert "token" in data["result"]
    assert "user_id" in anonymous_session.cookies
    assert "uname" in anonymous_session.cookies
    print(f"\n✅ 登录成功，用户ID: {data['result']['user_id']}")


def test_login_empty_verify_code(anonymous_session, base_url, test_user):
    """验证码为空 -> 登录失败"""
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)
    data = test_user.copy()
    data["verify_code"] = ""
    login_url = f"{base_url}/index.php?m=Home&c=User&a=do_login"
    resp = anonymous_session.post(login_url, data=data)
    assert resp.status_code == 200
    result = resp.json()          # 确保定义了 result 变量
    assert result["status"] != 1
    print(f"\n✅ 验证码为空测试通过: {result.get('msg')}")


def test_login_wrong_verify_code(anonymous_session, base_url, test_user):
    """验证码错误 -> 登录失败"""
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)
    data = test_user.copy()
    data["verify_code"] = "0000"
    login_url = f"{base_url}/index.php?m=Home&c=User&a=do_login"
    resp = anonymous_session.post(login_url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 验证码错误测试通过: {result.get('msg')}")


def test_login_wrong_password(anonymous_session, base_url, test_user):
    """密码错误 -> 登录失败"""
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)
    data = test_user.copy()
    data["password"] = "wrong_password"
    login_url = f"{base_url}/index.php?m=Home&c=User&a=do_login"
    resp = anonymous_session.post(login_url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 错误密码测试通过: {result.get('msg')}")


def test_login_missing_username(anonymous_session, base_url):
    """缺少用户名 -> 登录失败"""
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)
    data = {"password": "aa123456", "verify_code": "8888"}
    login_url = f"{base_url}/index.php?m=Home&c=User&a=do_login"
    resp = anonymous_session.post(login_url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 缺少用户名测试通过: {result.get('msg')}")


def test_login_missing_password(anonymous_session, base_url):
    """缺少密码 -> 登录失败"""
    verify_url = f"{base_url}/index.php?m=Home&c=User&a=verify&r={random.random()}"
    anonymous_session.get(verify_url)
    data = {"username": "15866661234", "verify_code": "8888"}
    login_url = f"{base_url}/index.php?m=Home&c=User&a=do_login"
    resp = anonymous_session.post(login_url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 缺少密码测试通过: {result.get('msg')}")


def test_login_all_fields_empty(anonymous_session):
    """所有字段为空 -> 登录失败（故意使用未定义的 BASE_URL，保留错误作为教学案例）"""
    # 故意使用 BASE_URL 而不是 base_url，导致 NameError
    url = f"{BASE_URL}/index.php?m=Home&c=User&a=do_login"
    data = {"username": "", "password": "", "verify_code": ""}
    resp = anonymous_session.post(url, data=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] != 1
    print(f"\n✅ 空字段测试通过: {result.get('msg')}")