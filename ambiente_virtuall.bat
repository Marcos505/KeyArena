@echo off
REM Nome da pasta virtualenv
set VENV_DIR=venv

REM Verificar se a pasta venv existe e excluí-la
if exist %VENV_DIR% (
    echo Excluindo a pasta %VENV_DIR%...
    rmdir /s /q %VENV_DIR%
)

REM Criar uma nova virtualenv
echo Criando uma nova venv...
python -m venv %VENV_DIR%

REM Ativar a nova venv
echo Ativando a venv...
call %VENV_DIR%\Scripts\activate

REM Instalar os requisitos a partir do requirements.txt
if exist requirements.txt (
    echo Instalando os requisitos do requirements.txt...
    pip install -r requirements.txt --quiet
) else (
    echo Arquivo requirements.txt não encontrado!
)

echo Processo finalizado.

REM Pausar por 2 segundos antes de fechar
timeout /t 2 /nobreak >nul
