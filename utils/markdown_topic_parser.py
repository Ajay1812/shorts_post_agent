import re
from typing import Optional
from langchain_community.document_loaders import UnstructuredMarkdownLoader

def extract_next_unposted_topic(file_path: str) -> Optional[str]:
    loader = UnstructuredMarkdownLoader(file_path=file_path)
    data = loader.load()
    pattern = re.compile(r"\[\s*\]\s*(.+)")
    matches = pattern.findall(data[0].page_content)

    if not matches:
        print("✅ All topics are completed or no unchecked topics found.")
        return None
    topic = matches[0].strip()
    print("💡Today's topic: ",topic)
    
    updated_content = data[0].page_content.replace(f"[ ] {topic}", f"[x] {topic}", 1)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"✅ Marked '{topic}' as done in the markdown file.")
    return topic


