# Imagem base leve com Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala ferramentas necessárias e o Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    fonts-liberation \
    libu2f-udev \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libgbm1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Instala o Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Instala as dependências do projeto
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Cria as pastas para volumes
RUN mkdir -p /app/data /app/image-graphics

# Variável para garantir saída dos prints
ENV PYTHONUNBUFFERED=1

# Comando que será executado ao rodar o container
CMD ["python", "main.py"]
