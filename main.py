# Standard library imports
import os
import shutil
import argparse
import sys
from typing import List, Dict, Optional
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
    sys.exit(1)

# --- CONFIGURATION ---
VERSION = "1.0.0"
console = Console()

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
    """Class to handle the intelligent sorting of files using local AI embeddings."""
    
    def __init__(self, source_folder: str, confidence_threshold: float = 0.3, dry_run: bool = False):
        """
        Initialize the SmartSorter.
        
        Args:
            source_folder (str): The directory to organize.
            confidence_threshold (float): Only move files if AI confidence is above this.
            dry_run (bool): If True, files won't actually be moved.
        """
        self.source_folder = os.path.abspath(source_folder)
        self.threshold = confidence_threshold
        self.dry_run = dry_run
        self.model: Optional[SentenceTransformer] = None
        self.category_names = list(CATEGORIES.keys())
        self.category_descriptions = list(CATEGORIES.values())

    def initialize_model(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Load the SentenceTransformer model locally."""
        with console.status(f"[bold green]🧠 Initializing AI Model ({model_name})..."):
            self.model = SentenceTransformer(model_name)
        console.print(f"[bold blue]✅ Model '{model_name}' ready.[/]\n")

    def clean_filename(self, filename: str) -> str:
        """
        Clean filename for better semantic understanding.
        Removes extensions and replaces common delimiters with spaces.
        """
        name, _ = os.path.splitext(filename)
        return name.replace('_', ' ').replace('-', ' ').replace('.', ' ')

    def organize(self, recursive: bool = False):
        """
        Execute the organization logic.
        
        Args:
            recursive (bool): Whether to search through subdirectories.
        """
        if not os.path.exists(self.source_folder):
            console.print(f"[bold red]❌ Error: Path '{self.source_folder}' does not exist.[/]")
            return

        self.initialize_model()

        if self.model is None:
            console.print("[bold red]❌ Failed to initialize AI model.[/]")
            return

        # Pre-encode category descriptions for efficiency
        category_embeddings = self.model.encode(self.category_descriptions, convert_to_tensor=True)

        # File discovery logic
        all_files = []
        if recursive:
            for root, _, filenames in os.walk(self.source_folder):
                # Skip files already in a category folder to avoid loops
                if any(cat in root for cat in self.category_names):
                    continue
                for f in filenames:
                    all_files.append(os.path.join(root, f))
        else:
            all_files = [os.path.join(self.source_folder, f) for f in os.listdir(self.source_folder) 
                         if os.path.isfile(os.path.join(self.source_folder, f))]
        
        # Skip hidden OS files
        files = [f for f in all_files if not os.path.basename(f).startswith('.')]

        if not files:
            console.print("[yellow]📂 No documents found to organize.[/]")
            return

        # Prepare summary table
        table = Table(title=f"Smart Sort Summary - {len(files)} files found")
        table.add_column("File", style="cyan", no_wrap=True)
        table.add_column("Target Category", style="magenta")
        table.add_column("Conf.", justify="right", style="green")
        table.add_column("Status", style="dim")

        for file_path in track(files, description="Analyzing files..."):
            filename = os.path.basename(file_path)
            cleaned_name = self.clean_filename(filename)
            
            # Semantic matching
            file_embedding = self.model.encode(cleaned_name, convert_to_tensor=True)
            cosine_scores = util.cos_sim(file_embedding, category_embeddings)
            best_match_idx = int(cosine_scores.argmax())
            best_score = float(cosine_scores[0][best_match_idx])
            best_category = self.category_names[best_match_idx]

            if best_score > self.threshold:
                if self.dry_run:
                    table.add_row(filename, best_category, f"{best_score:.2f}", "[yellow]Wait-list[/]")
                else:
                    try:
                        dest_path = os.path.join(self.source_folder, best_category)
                        os.makedirs(dest_path, exist_ok=True)
                        shutil.move(file_path, os.path.join(dest_path, filename))
                        table.add_row(filename, best_category, f"{best_score:.2f}", "[green]Moved[/]")
                    except Exception as e:
                        table.add_row(filename, best_category, f"{best_score:.2f}", f"[red]Error: {str(e)}[/]")
            else:
                table.add_row(filename, "Uncategorized", f"{best_score:.2f}", "[dim]Ignored[/]")

        console.print(table)
        
        if self.dry_run:
            console.print("\n[bold yellow]ℹ️ Dry Run Mode: Files remain untouched.[/]")
        else:
            console.print("\n[bold green]✨ Done! Your digital workspace is now organized.[/]")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description=f"Smart Sort AI v{VERSION}: Semantic file organizer powered by local AI."
    )
    parser.add_argument("path", type=str, help="Directory to organize")
    parser.add_argument("--threshold", "-t", type=float, default=0.3, help="Min confidence (0.00-1.00)")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Preview mode (no files moved)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Organize subdirectories")
    
    args = parser.parse_args()

    console.print(Panel.fit(
        f"[bold cyan]🧠 Smart Sort AI v{VERSION}[/]\n[dim]Professional AI-powered file organization[/]",
        border_style="blue"
    ))

    sorter = SmartSorter(args.path, args.threshold, args.dry_run)
    sorter.organize(recursive=args.recursive)

if __name__ == "__main__":
    main()
