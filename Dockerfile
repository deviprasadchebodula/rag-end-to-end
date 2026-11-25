FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN python -m pip install --upgrade pip

# Install CPU-only PyTorch
RUN python -m pip install torch==2.15.0 \
    --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

# Verify CPU-only installation
RUN python -c "import torch; assert torch.version.cuda is None; print('CPU PyTorch:', torch.__version__)"

RUN python -m pip check

COPY . .

RUN mkdir -p uploads

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]