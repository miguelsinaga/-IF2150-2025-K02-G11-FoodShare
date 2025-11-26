APP_ENTRY_POINT = app.py

# Nama environment virtual (default uv)
VENV_DIR = .venv

.PHONY: all install run clean test

# Default target jika hanya mengetik 'make'
all: install run

# 1. Install dependencies (akan membaca pyproject.toml)
install:
	@echo "Installing dependencies with uv..."
	uv sync

# 2. Menjalankan aplikasi
# PYTHONPATH=. memastikan folder 'src' terbaca sebagai module
run:
	@echo "Running FoodShare App..."
	uv run python $(APP_ENTRY_POINT)

# 3. Menjalankan Testing (karena saya lihat ada folder tests)
test:
	@echo "Running tests..."
	uv run pytest tests/

# 4. Membersihkan file cache
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/backend/__pycache__
	rm -rf .pytest_cache
	# Hapus .venv jika ingin install ulang dari nol:
	# rm -rf $(VENV_DIR)