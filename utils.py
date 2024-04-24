def is_image_or_file(url):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp'}
    file_extensions = {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.zip', '.rar', '.tar', '.gz'}

    try:
        if any(url.endswith(ext) for ext in file_extensions):
            return True
        response = requests.head(url, allow_redirects=True, timeout=10)
        content_type = response.headers.get('content-type', '').lower()

        if content_type.startswith('image/') or any(url.endswith(ext) for ext in image_extensions):
            return True

        return False
    except requests.RequestException as e:
        print("Request to", url, "failed:", str(e))
        return False
    except Exception as e:
        print("An error occurred while checking content type for", url, ":", str(e))
        return False
