import shutil
from pathlib import Path

INBOX = Path.home() / "Desktop" / "PhotoInbox"
DEST = Path.home() / "Items"

# supports common camera + phone formats (case-insensitive via .lower())
VALID_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".cr2", ".dng", ".tif", ".tiff"}

def main():
    print("\nPhoto Pipeline Tool (CR2 + JPG + HEIC)\n")
    print(f"INBOX: {INBOX}")
    print(f"DEST : {DEST}\n")

    sku = input("Enter SKU: ").strip()
    category = input("Enter category (optional): ").strip()

    if not sku:
        print("SKU required.")
        return

    if not category:
        category = "item"

    dest_folder = DEST / sku
    dest_folder.mkdir(parents=True, exist_ok=True)

    moved = 0
    skipped = []

    for file in sorted(INBOX.iterdir(), key=lambda p: p.name.lower()):
        if not file.is_file():
            continue

        ext = file.suffix.lower()
        if ext in VALID_EXTS:
            new_name = f"{sku}_{category}_{moved+1:02d}{ext}"
            new_path = dest_folder / new_name
            shutil.move(str(file), str(new_path))
            print(f"Moved: {file.name} -> {new_name}")
            moved += 1
        else:
            skipped.append(file.name)

    print(f"\nDone. Moved {moved} file(s) to: {dest_folder}")
    if skipped:
        print("\nSkipped (not in VALID_EXTS):")
        for name in skipped:
            print(" -", name)

if __name__ == "__main__":
    main()
