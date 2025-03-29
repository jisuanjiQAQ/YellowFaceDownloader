import os
import requests

def download_emojis(output_dir="emojis"):
    """
    爬取B站的小黄脸表情包并保存到本地
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # B站表情包API
    url = "https://api.bilibili.com/x/emote/package"
    # 表情包ID列表（小黄脸表情包的ID）
    emoji_ids = [1]

    params = {
        "business": "emoji",
        "jsonp": "jsonp",
        "ids": ",".join(map(str, emoji_ids))
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # 获取表情包数据
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        if data["code"] == 0:
            emojis = data["data"]["packages"][0]["emote"]
            print(f"找到 {len(emojis)} 个表情包")

            # 下载每个表情包
            for emoji in emojis:
                emoji_name = emoji["text"]
                emoji_url = emoji["url"]
                emoji_filename = f"{emoji_name}.png"

                # 下载表情包
                emoji_response = requests.get(emoji_url, headers=headers)
                emoji_response.raise_for_status()

                # 保存表情包
                with open(os.path.join(output_dir, emoji_filename), "wb") as f:
                    f.write(emoji_response.content)
                print(f"已保存: {emoji_filename}")

            print("所有表情包已下载完成！")
        else:
            print(f"API请求失败，错误码: {data['code']}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    download_emojis()