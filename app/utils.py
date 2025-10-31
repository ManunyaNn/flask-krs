import re

def extract_youtube_id(youtube_url):
    #Извлекает YouTube ID из любой формы ссылки
    if not youtube_url:
        return None
        
    patterns = [
        # Стандартная ссылка: https://www.youtube.com/watch?v=VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        
        # Короткая ссылка: https://youtu.be/VIDEO_ID  
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
        
        # Embed ссылка: https://www.youtube.com/embed/VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
        
        # С таймкодом и другими параметрами
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    return None

def get_youtube_thumbnail(youtube_url, quality='hqdefault'):
    video_id = extract_youtube_id(youtube_url)
    if video_id:
        return f'https://img.youtube.com/vi/{video_id}/{quality}.jpg'
    
    return None
