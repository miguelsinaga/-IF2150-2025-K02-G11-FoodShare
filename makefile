.PHONY: install run clean setup

# Target default (jalan saat ketik 'make' saja)
all: run

# 1. Install dependencies (library)
install:
	uv sync

# 2. Jalankan Aplikasi
run:
	uv run python -m app

# 3. Bersihkan file cache (Opsional - syntax Windows)
clean:
	@echo "Membersihkan cache..."
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@echo "Selesai."

# 4. Bantuan setup data (Mengingatkan user)
setup:
	@echo "Pastikan Anda sudah memindahkan file CSV ke folder 'tests/data'."
	@echo "Gunakan perintah 'make install' lalu 'make run'."