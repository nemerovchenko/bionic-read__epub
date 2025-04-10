import zipfile
import os

def read_epub(epub_path):
    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        return {name: zip_ref.read(name) for name in zip_ref.namelist()}

def write_epub(epub_path, content_dict):
    with zipfile.ZipFile(epub_path, 'w') as zip_out:
        for name, content in content_dict.items():
            zip_out.writestr(name, content)

def extract_text_from_epub(epub_content):
    text_content = []
    for name, content in epub_content.items():
        if name.endswith(('.html', '.xhtml', '.htm')):
            text_content.append(content.decode('utf-8'))
    return text_content

def get_epub_metadata(epub_content):
    metadata = {}
    if 'META-INF/container.xml' in epub_content:
        container_xml = epub_content['META-INF/container.xml'].decode('utf-8')
        # Logic to parse the container.xml and extract metadata can be added here
    return metadata