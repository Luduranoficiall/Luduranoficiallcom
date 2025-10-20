import os
import zipfile
from pathlib import Path

REQUIRED_FILES = [
    "app.py",
    "requirements.txt",
    "Procfile",
    "runtime.txt",
]
REQUIRED_DIRS = [
    "templates",
    "static",
    "instance",
]

OUTPUT_ZIP = "deploy_package.zip"


def collect_paths(base_path: Path):
    missing = []
    included = []

    for rel_file in REQUIRED_FILES:
        target = base_path / rel_file
        if target.exists():
            included.append(target)
        else:
            missing.append(rel_file)

    for rel_dir in REQUIRED_DIRS:
        target = base_path / rel_dir
        if target.exists() and target.is_dir():
            for path in target.rglob("*"):
                if path.is_file():
                    included.append(path)
        else:
            missing.append(rel_dir)

    return included, missing


def create_zip(base_path: Path, files):
    zip_path = base_path / OUTPUT_ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(base_path))
    return zip_path


def main():
    base_path = Path(__file__).resolve().parent
    files, missing = collect_paths(base_path)

    if missing:
        print("⚠️  Aviso: Os itens abaixo não foram encontrados e ficarão fora do pacote:")
        for item in missing:
            print(f"  - {item}")
        print()

    if not files:
        print("Nenhum arquivo elegível encontrado. Nada foi gerado.")
        return

    zip_path = create_zip(base_path, files)
    total_size = sum(path.stat().st_size for path in files)

    print("✅ Pacote de deploy gerado com sucesso!")
    print(f"Arquivo: {zip_path}")
    print(f"Itens incluídos: {len(files)}")
    print(f"Tamanho aproximado: {total_size / 1024:.1f} KB")
    print("\nFaça upload desse arquivo em serviços como PythonAnywhere (Files → Upload) e extraia tudo na pasta do projeto antes de configurar o web app.")


if __name__ == "__main__":
    main()
