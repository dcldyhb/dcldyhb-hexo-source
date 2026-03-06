#!/bin/bash

# 定义源目录和目标目录
SOURCE_DIR="/Users/fangyan/Documents/notes"
TARGET_DIR="/Users/fangyan/Documents/dcldyhb/source/_posts/notes"

# 如果目标目录不存在，则创建
mkdir -p "$TARGET_DIR"

# 使用 rsync 同步文件 (排除 .DS_Store 等无关文件)
# --delete 选项意味着如果你在 notes 删除了文件，博客里也会同步删除
rsync -av --delete --exclude '.DS_Store' --exclude '.git' "$SOURCE_DIR/" "$TARGET_DIR/"

echo "笔记同步完成！"