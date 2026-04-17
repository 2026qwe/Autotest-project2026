# Autotest project
# Autotest project
一、被测系统原始信息
框架：ThinkPHP 5

服务器环境：WAMP（Windows + Apache 2.4 + MySQL + PHP 5.4）

本地访问地址：http://www.myshop.com

入口文件：/index.php

路由规则（从 route.php 确认）：

简洁路由：/goodsInfo/77.html → home/goods/goodsInfo

完整路径：/home/goods/goodsInfo/id/77.html

后台入口：/index.php/Admin/Admin/login.html

项目根目录：D:/phpstudy/WWW（PHP 项目）

关键接口（抓包确认）：

登录：POST /index.php?m=Home&c=User&a=do_login（参数：username, password, verify_code=8888）

注册：POST /index.php/Home/User/reg.html（参数：scene, username, verify_code, password, password2, invite）

搜索：GET /Home/Goods/search.html?q=关键词

添加购物车：POST /index.php?m=Home&c=Cart&a=ajaxAddCart（含 goods_id, goods_num 等）

更新购物车：POST /Home/Cart/AsyncUpdateCart.html（cart[0][id]等）

地址列表：GET /Home/User/address_list.html

新增地址：POST /index.php?m=Home&c=User&a=add_address

下单：POST /Home/Cart/cart3.html（含 address_id, goods_id, act=submit_order）

支付：POST /index.php/Home/Payment/getCode.html（pay_radio, order_id）

订单列表：GET /Home/Order/order_list.html

二、自动化测试项目最终结构
项目根目录：D:\Python\Autotest project

text
D:\Python\Autotest project\
├── pytest.ini
├── reports\
└── tests\
    ├── conftest.py
    ├── test_login.py
    ├── test_register.py
    ├── test_search.py
    ├── test_cart.py
    ├── test_address.py
    ├── test_order.py
    ├── test_payment.py
    └── test_order_list.py
