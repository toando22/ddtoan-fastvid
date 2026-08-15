# Core extractor logic calling yt-dlp
import yt_dlp

def extract_video_info(url: str):
    # Cấu hình yt-dlp để ưu tiên lấy chất lượng tốt nhất
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "success": True,
                "title": info.get('title', 'Video không tên'),
                "thumbnail": info.get('thumbnail', ''),
                "download_url": info.get('url', ''),
                "platform": info.get('extractor', 'unknown')
            }
    except Exception as e:
        return {
            "success": False,
            "error": "Không thể bóc tách link này. Vui lòng kiểm tra lại URL."
        }