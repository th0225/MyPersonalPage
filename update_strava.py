import requests
import json
import os

CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('STRAVA_REFRESH_TOKEN')

def update_stats():
    # 1. 換取 Access Token
    auth_url = "https://www.strava.com/oauth/token"
    auth_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }

    print("正在請求新的 Access Token...")
    auth_res = requests.post(auth_url, data=auth_data).json()
    access_token = auth_res['access_token']

    # 2. 抓取最新活動
    activities_url = \
        "https://www.strava.com/api/v3/athlete/activities?per_page=1"
    headers = {'Authorization': f'Bearer {access_token}'}

    print("正在抓取 Strava 最新活動...")
    activities = requests.get(activities_url, headers=headers).json()

    if not activities:
        print("沒有找到任何活動")
        return
    
    latest = activities[0]

    # 3. 整理成 Blazor 要用的格式
    processed_data = {
        # 活動名稱
        "name": latest['name'],
        # 騎乘距離
        "distance": round(latest['distance'] / 1000, 1),
        # 移動時間
        "movingTime": latest['moving_time'],
        # 爬升高度
        "elevation": int(latest['total_elevation_gain']),
        # 平均功率
        "averageWatts": int(latest.get('average_watts', 0)),
        # 標準化功率
        "weightedAverageWatts": int(latest.get('weighted_average_watts', 0)),
        # 最高瓦數
        "maxWatts": int(latest.get('max_watts', 0)),
        # 消耗能量
        "kilojoules": int(latest.get('kilojoules', 0)),
        # 紀錄設備
        "deviceName": latest.get('device_name', 'Garmin'),
        # 開始時間
        "startDate": latest['start_date_local'],
        # 痛苦指數
        "sufferScore": int(latest.get('suffer_score', 0)),
        # 路線
        "summaryPolyline": latest.get('map', {}).get('summary_polyline', '')
    }

    # 4. 寫入檔案
    file_path = 'wwwroot/data/strava.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    
    print(f"成功更新數據:{processed_data['name']}")

if __name__ == "__main__":
    update_stats()