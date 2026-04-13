public class StravaActivity
{
    // 活動名稱
    public string Name { get; set; } = string.Empty;
    // 驗乗距離
    public double Distance { get; set; }
    // 移動時間
    public int MovingTime { get; set; }
    public string DisplayTime => 
        TimeSpan.FromSeconds(MovingTime) is var t && t.TotalHours >= 1 
        ? $"{(int)t.TotalHours}h {t.Minutes}m {t.Seconds}s" 
        : $"{t.Minutes}m {t.Seconds}s";
    // 爬升高度
    public double Elevation { get; set; }
    // 平均功率
    public int AverageWatts { get; set; }
    // 標準化功率
    public int WeightedAverageWatts { get; set; }
    // 最高瓦數
    public int MaxWatts { get; set; }
    // 消耗能量
    public int KiloJoules { get; set; }
    // 設備名稱
    public string DeviceName { get; set; } = string.Empty;
    // 開始時間
    public string StartDate { get; set; } = string.Empty;
    // 痛苦指數
    public int SufferScore { get; set; }
    // 路線
    public string SummaryPolyline { get; set; } = string.Empty;
}