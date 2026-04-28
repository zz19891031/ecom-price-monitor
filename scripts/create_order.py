#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1: 创建订单脚本
职责：调用服务端 API 创建订单，返回订单信息
如果免费额度内，直接返回结果，无需支付
"""

import sys
import json
import urllib.request
import urllib.error

# Windows 编码设置
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 服务端 API 地址
SERVER_URL = "https://1257964133-2ejbwpe7le.ap-shanghai.tencentscf.com"


def create_order(question: str, user_id: str = "default") -> dict:
    """
    调用服务端创建订单接口

    Args:
        question: 用户输入的问题/命令
        user_id: 用户ID（用于免费额度判断）

    Returns:
        dict: 包含订单信息或免费额度结果
    """
    url = f"{SERVER_URL}/create_order"

    data = json.dumps({
        "question": question,
        "user_id": user_id
    }).encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        raise Exception(f"网络请求失败: {e.reason}")
    except json.JSONDecodeError as e:
        raise Exception(f"响应解析失败: {e}")
    except Exception as e:
        raise Exception(f"未知错误: {e}")


def main():
    if len(sys.argv) < 2:
        print("订单创建失败: 缺少必要参数 question")
        sys.exit(1)

    question = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else "default"

    try:
        result = create_order(question, user_id)

        # 检查服务端返回是否成功
        if result.get("responseCode") != "200":
            error_msg = result.get("responseMessage", "未知错误")
            print(f"订单创建失败: {error_msg}")
            sys.exit(1)

        # 检查是否在免费额度内
        if result.get("freeQuota"):
            # 免费额度内，直接输出结果
            print("FREE_QUOTA: True")
            print(f"ANSWER: {result.get('answer', '')}")
            sys.exit(0)

        # 需要付费，输出订单信息
        print(f"ORDER_NO={result['orderNo']}")
        print(f"AMOUNT={result['amount']}")
        print(f"ENCRYPTED_DATA={result['encryptedData']}")
        print(f"PAY_TO={result['payTo']}")
        print("FREE_QUOTA: False")

    except Exception as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
