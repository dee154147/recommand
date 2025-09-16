#!/bin/bash

# 数据库备份脚本
# 用于备份PostgreSQL数据库

# 配置变量
DB_NAME="recommendation_db"
DB_USER="liuzhichao"
DB_HOST="localhost"
DB_PORT="5432"
BACKUP_DIR="/Users/liuzhichao/cursorProjects/recommand2/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# 创建备份目录（如果不存在）
mkdir -p "$BACKUP_DIR"

echo "开始备份数据库: $DB_NAME"
echo "时间戳: $TIMESTAMP"
echo "备份目录: $BACKUP_DIR"

# 生成备份文件名
SQL_BACKUP_FILE="${BACKUP_DIR}/recommendation_db_backup_${TIMESTAMP}.sql"
DUMP_BACKUP_FILE="${BACKUP_DIR}/recommendation_db_backup_${TIMESTAMP}.dump"

echo "创建SQL格式备份: $SQL_BACKUP_FILE"
# 使用pg_dump创建SQL格式备份
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --verbose \
    --no-password \
    --format=plain \
    --file="$SQL_BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "SQL备份创建成功: $SQL_BACKUP_FILE"
    echo "文件大小: $(ls -lh "$SQL_BACKUP_FILE" | awk '{print $5}')"
else
    echo "SQL备份创建失败"
    exit 1
fi

echo "创建自定义格式备份: $DUMP_BACKUP_FILE"
# 使用pg_dump创建自定义格式备份（压缩的二进制格式）
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --verbose \
    --no-password \
    --format=custom \
    --compress=9 \
    --file="$DUMP_BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "DUMP备份创建成功: $DUMP_BACKUP_FILE"
    echo "文件大小: $(ls -lh "$DUMP_BACKUP_FILE" | awk '{print $5}')"
else
    echo "DUMP备份创建失败"
    exit 1
fi

# 验证备份文件
echo "验证备份文件..."
if [ -f "$SQL_BACKUP_FILE" ] && [ -s "$SQL_BACKUP_FILE" ]; then
    echo "✓ SQL备份文件存在且不为空"
else
    echo "✗ SQL备份文件验证失败"
    exit 1
fi

if [ -f "$DUMP_BACKUP_FILE" ] && [ -s "$DUMP_BACKUP_FILE" ]; then
    echo "✓ DUMP备份文件存在且不为空"
else
    echo "✗ DUMP备份文件验证失败"
    exit 1
fi

# 显示备份统计信息
echo "备份完成统计:"
echo "数据库: $DB_NAME"
echo "备份时间: $(date)"
echo "SQL备份文件: $SQL_BACKUP_FILE"
echo "DUMP备份文件: $DUMP_BACKUP_FILE"
echo "备份目录总大小: $(du -sh "$BACKUP_DIR" | awk '{print $1}')"

# 清理旧备份（保留最近10个备份）
echo "清理旧备份文件..."
cd "$BACKUP_DIR"
ls -t recommendation_db_backup_*.sql | tail -n +11 | xargs -r rm -f
ls -t recommendation_db_backup_*.dump | tail -n +11 | xargs -r rm -f
echo "旧备份清理完成"

echo "数据库备份完成！"
