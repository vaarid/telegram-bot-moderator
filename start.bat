chcp 65001 >nul
@echo off
echo Запуск Docker-инфраструктуры...
docker-compose up --build
pause 