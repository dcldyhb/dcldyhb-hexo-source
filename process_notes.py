import shutil
import frontmatter
from pathlib import Path
import sys

# --- 路径配置 ---
# 从本地的、不受版本控制的 config.py 文件中导入笔记仓库的路径
try:
    from config import NOTES_DIR
except ImportError:
    print("[错误] 配置文件 'config.py' 未找到！")
    print("请在 dcldyhb-hexo-source 根目录下创建 config.py 文件，")
    print("并在其中定义您的笔记仓库路径，例如：")
    print('NOTES_DIR = r"C:\\path\\to\\your\\notes"')
    sys.exit(1) # 退出脚本

NOTES_SOURCE_DIR = Path(NOTES_DIR)
HEXO_SOURCE_REPO_ROOT = Path(__file__).parent.resolve()
HEXO_POSTS_DIR = HEXO_SOURCE_REPO_ROOT / "source/_posts"

# --- 主逻辑 ---
def transform_note_for_hexo(md_file_path):
    try:
        post = frontmatter.load(md_file_path)
        if not post.content: return frontmatter.dumps(post)
        
        lines = post.content.splitlines()
        h1_found_at_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('# '):
                h1_found_at_index = i
                print(f" -> 找到并移除H1: '{line.strip()[2:]}'", end="")
                break
        
        if h1_found_at_index != -1:
            del lines[h1_found_at_index]
            post.content = '\n'.join(lines).lstrip('\n')
        else:
            print(" -> 未找到H1，正文保持不变。", end="")
            
        return frontmatter.dumps(post)
    except Exception as e:
        print(f"\n[错误] 处理文件 {md_file_path.name} 时出错: {e}")
        return None

def sync_notes_to_hexo():
    print("--- 开始同步笔记到 Hexo (配置文件模式) ---\n")
    if not NOTES_SOURCE_DIR.is_dir():
        print(f"[错误] 在 config.py 中配置的笔记仓库目录未找到: {NOTES_SOURCE_DIR}")
        return

    print(f"正在清理目标目录: {HEXO_POSTS_DIR}")
    if HEXO_POSTS_DIR.exists(): shutil.rmtree(HEXO_POSTS_DIR)
    HEXO_POSTS_DIR.mkdir(parents=True)

    print(f"\n正在从 {NOTES_SOURCE_DIR} 复制和处理文件...")
    for md_file in NOTES_SOURCE_DIR.glob('**/*.md'):
        relative_path = md_file.relative_to(NOTES_SOURCE_DIR)
        print(f"处理文件: {relative_path}", end="")
        transformed_content = transform_note_for_hexo(md_file)
        if transformed_content:
            dest_file_path = HEXO_POSTS_DIR / relative_path
            dest_file_path.parent.mkdir(parents=True, exist_ok=True)
            dest_file_path.write_text(transformed_content, encoding='utf-8')
            print(" -> 完成")
    print("\n--- 同步成功! ---")

if __name__ == "__main__":
    sync_notes_to_hexo()