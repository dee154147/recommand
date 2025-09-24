#!/bin/bash

# 数据库备份脚本
# 使用方法: ./backup_database.sh

# 设置变量
DB_HOST="localhost"
DB_USER="liuzhichao"
DB_NAME="recommendation_db"
BACKUP_DIR="backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/recommendation_db_backup_${TIMESTAMP}.sql"

# 创建备份目录
mkdir -p ${BACKUP_DIR}

# 执行备份
echo "开始备份数据库..."
pg_dump -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} > ${BACKUP_FILE}

# 检查备份是否成功
if [ $? -eq 0 ]; then
    echo "✅ 数据库备份成功！"
    echo "📁 备份文件: ${BACKUP_FILE}"
    echo "📊 文件大小: $(du -h ${BACKUP_FILE} | cut -f1)"
    echo "🕒 备份时间: $(date)"
else
    echo "❌ 数据库备份失败！"
    exit 1
fi

# 显示备份文件信息
echo ""
echo "📋 备份文件信息:"
ls -lh ${BACKUP_FILE}

echo ""
echo "🔍 备份内容验证:"
echo "表数量: $(grep -c "COPY public\." ${BACKUP_FILE})"
echo "备份完整性: $(tail -3 ${BACKUP_FILE} | grep -q "PostgreSQL database dump complete" && echo "✅ 完整" || echo "❌ 不完整")"

echo ""
echo "💡 恢复命令:"
echo "psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} < ${BACKUP_FILE}"