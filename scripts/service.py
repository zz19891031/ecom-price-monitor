#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3: 服务执行脚本
职责：调用服务端 API 验证支付凭证并执行服务
"""

import sys
import json
import urllib.request
import urllib.error

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 服务端 API 地址
SERVER_URL = "https://1257964133-2ejbwpe7le.ap-shanghai.tencentscf.com"


def execute_service(question: str, order_no: str, credential: str, user_id: str = "default") -> dict:
    """
    调用服务端执行服务接口
    """
    url = f"{SERVER_URL}/get_service_result"
    
    data = json.dumps({
        "question": question,
        "orderNo": order_no,
        "credential": credential,
        "user_id": user_id
    }).encode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        raise Exception(f"网络请求失败: {e.reason}")
    except json.JSONDecodeError as e:
        raise Exception(f"响应解析失败: {e}")
    except Exception as e:
        raise Exception(f"未知错误: {e}")


def main():
    if len(sys.argv) < 4:
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: 缺少必要参数: question, order_no, credential")
        sys.exit(1)
    
    question = sys.argv[1]
    order_no = sys.argv[2]
    credential = sys.argv[3]
    user_id = sys.argv[4] if len(sys.argv) > 4 else "default"
    
    try:
        result = execute_service(question, order_no, credential, user_id)
        
        # 获取支付状态
        pay_status = result.get("payStatus", "ERROR")
        
        if pay_status == "SUCCESS":
            print("PAY_STATUS: SUCCESS")
            # 输出服务结果
            if "answer" in result:
                # 移除 emoji 避免编码问题
                answer = result['answer'].replace('📖', '[帮助]').replace('•', '-')
                print(f"ANSWER: {answer}")
            elif "output" in result:
                output = result['output'].replace('📖', '[帮助]').replace('•', '-')
                print(f"ANSWER: {output}")
        else:
            print(f"PAY_STATUS: {pay_status}")
            if "errorInfo" in result:
                print(f"ERROR_INFO: {result['errorInfo']}")
            elif "error" in result:
                print(f"ERROR_INFO: {result['error']}")
        
    except Exception as e:
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
