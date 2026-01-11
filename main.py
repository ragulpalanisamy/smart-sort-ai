import os
import shutil
import argparse
from typing import List, Dict
from datetime import datetime

# Third-party imports
try:
    from sentence_transformers import SentenceTransformer, util
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    from rich.panel import Panel
except ImportError:
    print("❌ Missing dependencies. Run: pip install -r requirements.txt")
    exit(1)

# --- CONFIGURATION ---
console = Console()
MODEL_NAME = 'all-MiniLM-L6-v2'

# Define your categories with descriptions for better AI context
CATEGORIES = {
    "Finance & Bills": "Invoices, receipts, bank statements, tax documents, budget spreadsheets",
    "Work & Projects": "Meeting notes, project proposals, contracts, professional slides, work reports",
    "Personal & Media": "Photos, holiday plans, family documents, personal notes, hobbies",
    "Programming & Tech": "Python scripts, javascript code, repositories, technical documentation, config files",
    "Education & Research": "University assignments, thesis papers, course materials, lecture notes, academic papers",
    "Archive": "Old documents, miscellaneous items, unsorted files"
}

class SmartSorter:
    def __init__(self, source_folder: str, confidence_threshold: float = 0.3, dry_run: bool = False):
        self.source_folder = os.path.abspath(source_folder)
        self.threshold = confidence_threshold
        self.dry_run = dry_run
        self.model = None
        self.category_names = list(CATEGORIES.keys())
        self.category_descriptions = list(CATEGORIES.values())

    def initialize_model(self):
        with console.status("[bold green]🧠 Initializing AI Model (Local)..."):
            self.model = SentenceTransformer(MODEL_NAME)
        console.print(f"[bold blue]✅ Model '{MODEL_NAME}' loaded successfully.[/]\n")

    def clean_filename(self, filename: str) -> str:
        """Removes extensions and replaces separators with spaces for better embedding."""
        name, _ = os.path.splitext(filename)
        return name.replace('_', ' ').replace('-', ' ').replace('.', ' ')

    def organize(self, recursive: bool = False):
        if not os.path.exists(self.source_folder):
            console.print(f"[bold red]❌ Error: Folder '{self.source_folder}' not found.[/]")
            return

        self.initialize_model()

        category_embeddings = self.model.encode(self.category_descriptions, convert_to_tensor=True)

        # Better file discovery
        all_files = []
        if recursive:
            for root, _, filenames in os.walk(self.source_folder):
                # Don't sort files already inside category folders
                if any(cat in root for cat in self.category_names):
                    continue
                for f in filenames:
                    all_files.append(os.path.join(root, f))
        else:
            all_files = [os.path.join(self.source_folder, f) for f in os.listdir(self.source_folder) 
                         if os.path.isfile(os.path.join(self.source_folder, f))]
        
        # Filter hidden files
        files = [f for f in all_files if not os.path.basename(f).startswith('.')]

        if not files:
            console.print("[yellow]📂 No files found to sort.[/]")
            return

        table = Table(title=f"Sorting {len(files)} Files{' (DRY RUN)' if self.dry_run else ''}")
        table.add_column("File", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Confidence", justify="right", style="green")
        table.add_column("Action", style="dim")

        for file_path in track(files, description="Processing..."):
            filename = os.path.basename(file_path)
            cleaned_name = self.clean_filename(filename)
            file_embedding = self.model.encode(cleaned_name, convert_to_tensor=True)

            cosine_scores = util.cos_sim(file_embedding, category_embeddings)
            best_match_idx = int(cosine_scores.argmax())
            best_score = float(cosine_scores[0][best_match_idx])
            best_category = self.category_names[best_match_idx]

            if best_score > self.threshold:
                action = "To be moved" if self.dry_run else "Moved"
                table.add_row(filename, best_category, f"{best_score:.2f}", action)
                
                if not self.dry_run:
                    dest_path = os.path.join(self.source_folder, best_category)
                    os.makedirs(dest_path, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest_path, filename))
            else:
                table.add_row(filename, "[dim]None[/]", f"{best_score:.2f}", "[yellow]Skipped[/]")

        console.print(table)
        
        if self.dry_run:
            console.print("\n[bold yellow]ℹ️ DRY RUN complete. No files were moved.[/]")
        else:
            console.print("\n[bold green]✨ Desktop Zen achieved![/]")

def main():
    parser = argparse.ArgumentParser(description="Smart Sort AI: Organize files by meaning.")
    parser.add_argument("path", type=str, help="Path to the folder to organize")
    parser.add_argument("--threshold", type=float, default=0.3, help="Confidence threshold (0.0 to 1.0)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without moving files")
    parser.add_argument("--recursive", "-r", action="store_true", help="Search in subdirectories")
    
    args = parser.parse_args()

    console.print(Panel.fit(
        "[bold cyan]🧠 Smart Sort AI[/]\n[dim]The intelligent file organizer[/]",
        border_style="blue"
    ))

    sorter = SmartSorter(args.path, args.threshold, args.dry_run)
    sorter.organize(recursive=args.recursive)

if __name__ == "__main__":
    main()
