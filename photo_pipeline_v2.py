import shutil
from pathlib import Path
from datetime import datetime

INBOX = Path.home() / "Desktop" / "PhotoInbox"
DEST_ROOT = Path.home() / "Items"

RAW_EXTS = {".cr2", ".dng", ".nef", ".arw"}
JPG_EXTS = {".jpg", ".jpeg", ".png", ".heic"}

CHECKLISTS = {
    "clothing": [
        "Front (flat-lay / hanger)",
        "Back",
        "Tag (brand + size)",
        "Material/care tag",
        "Close-up of graphic/logo",
        "Flaws (pilling, stains, holes) if any",
        "Measurements photo: pit-to-pit",
        "Measurements photo: length",
    ],
    "electronics": [
        "Front",
        "Back",
        "All ports/connectors",
        "Serial/model label",
        "Accessories included (cables, controllers, etc.)",
        "Powered-on proof (if applicable)",
        "Flaws/cosmetic wear",
    ],
    "collectibles": [
        "Front",
        "Back",
        "Close-ups of key details/marks",
        "Flaws/edge wear",
        "Group shot of everything included",
        "Any authenticity markers/labels",
    ],
}

def slug(s: str) -> str:
    s = s.strip()
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in s)

def write_readme(folder: Path, sku: str, category: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    checklist = CHECKLISTS.get(category.lower(), CHECKLISTS["collectibles"])
    text = []
    text.append(f"SKU: {sku}")
    text.append(f"Category: {category}")
    text.append(f"Created: {now}")
    text.append("")
    text.append("Folders:")
    text.append(" - RAW/        (camera originals: CR2/DNG/etc.)")
    text.append(" - EXPORTS/    (Lightroom exports for eBay: JPG/PNG/HEIC)")
    text.append("")
    text.append("Photo checklist:")
    for item in checklist:
        text.append(f" [ ] {item}")
    text.append("")
    text.append("Listing notes:")
    text.append(" - Condition:")
    text.append(" - Key descriptors/keywords:")
    text.append(" - Defects disclosed:")
    text.append(" - Shipping plan (weight/box):")
    (folder / "README.txt").write_text("\n".join(text), encoding="utf-8")

def main():
    print("\n=== Photo Pipeline v2 (RAW-first) ===\n")
    print(f"INBOX: {INBOX}")
    print(f"DEST : {DEST_ROOT}\n")

    sku = slug(input("SKU (required): "))
    if not sku:
        print("SKU required. Exiting.")
        return

    category = slug(input("Category (clothing/electronics/collectibles) [collectibles]: "))
    if not category:
        category = "collectibles"

    item_folder = DEST_ROOT / sku
    raw_folder = item_folder / "RAW"
    exports_folder = item_folder / "EXPORTS"

    raw_folder.mkdir(parents=True, exist_ok=True)
    exports_folder.mkdir(parents=True, exist_ok=True)

    write_readme(item_folder, sku, category)

    moved_raw = 0
    moved_exports = 0
    skipped = []

    if not INBOX.exists():
        print(f"Missing inbox folder: {INBOX}")
        print("Create it with: mkdir -p ~/Desktop/PhotoInbox")
        return

    for f in sorted(INBOX.iterdir(), key=lambda p: p.name.lower()):
        if not f.is_file():
            continue
        ext = f.suffix.lower()

        if ext in RAW_EXTS:
            new_name = f"{sku}_{category}_{moved_raw+1:02d}{ext}"
            shutil.move(str(f), str(raw_folder / new_name))
            print(f"RAW moved: {f.name} -> RAW/{new_name}")
            moved_raw += 1
        elif ext in JPG_EXTS:
            # supports future RAW+JPG workflow; harmless if none present
            new_name = f"{sku}_{category}_{moved_exports+1:02d}{ext}"
            shutil.move(str(f), str(exports_folder / new_name))
            print(f"Export moved: {f.name} -> EXPORTS/{new_name}")
            moved_exports += 1
        else:
            skipped.append(f.name)

    print("\n--- Summary ---")
    print(f"RAW moved     : {moved_raw}")
    print(f"Exports moved : {moved_exports}")
    print(f"Item folder   : {item_folder}")

    if skipped:
        print("\nSkipped (unrecognized extension):")
        for name in skipped:
            print(" -", name)

    if moved_raw == 0 and moved_exports == 0:
        print("\nNo image files moved. If your RAW is CR2, confirm files end with .CR2/.Cr2 and are in PhotoInbox.")

    print("\nNext step:")
    print(f"1) Import {sku}/RAW into Lightroom.")
    print(f"2) Export listing JPGs into {sku}/EXPORTS.")
    print("3) Use README.txt as your shot/listing checklist.\n")

if __name__ == "__main__":
    main()
