#!/bin/bash

echo "🧹 Git 정리 및 최적화"

# 1. Git 캐시에서 불필요한 파일들 제거
echo "📂 Git 캐시 정리 중..."

# 이미 추가된 불필요한 파일들을 Git에서 제거 (파일은 유지)
git rm -r --cached backend/venv/ 2>/dev/null || true
git rm -r --cached logs/ 2>/dev/null || true
git rm -r --cached **/__pycache__/ 2>/dev/null || true
git rm -r --cached **/*.pyc 2>/dev/null || true
git rm -r --cached **/*.pyo 2>/dev/null || true
git rm -r --cached **/*.pyd 2>/dev/null || true
git rm -r --cached .DS_Store 2>/dev/null || true
git rm -r --cached **/.DS_Store 2>/dev/null || true
git rm --cached backend/.env 2>/dev/null || true
git rm --cached *.log 2>/dev/null || true

# 2. 현재 상태 확인
echo ""
echo "📊 Git 상태:"
git status --porcelain | wc -l | xargs echo "변경된 파일 수:"

# 3. 추가할 파일들만 확인
echo ""
echo "📋 Git에 포함될 파일들:"
git ls-files | grep -v -E "(venv/|__pycache__|\.pyc|\.log|\.DS_Store)" | head -20

# 4. .gitignore 적용 확인
echo ""
echo "🚫 제외될 파일들 (샘플):"
find . -name "*.pyc" -o -name "__pycache__" -o -name ".DS_Store" | head -10

echo ""
echo "✅ Git 정리 완료!"
echo ""
echo "🚀 이제 커밋하세요:"
echo "   git add ."
echo "   git commit -m '차트봇 최적화 및 정리'"
echo "   git push"
