"""
Benchmark script to evaluate the accuracy of the resume parser.
Calculates Precision, Recall, and F1 score against manual ground truth.
"""
import os
import re
from typing import Dict, List, Set, Tuple

# Import the parser functions
from ai.resume_parser import extract_text, extract_skills

# ---------------------------------------------------------
# GROUND TRUTH DICTIONARY
# ---------------------------------------------------------
# Manually fill in the correct list of skills for each resume file.
# Format: "filename.pdf": ["Skill 1", "Skill 2", ...]
# Example:
# GROUND_TRUTH = {
#     "john_doe_resume.pdf": ["Python", "Django", "PostgreSQL", "Docker", "Git"],
# }
GROUND_TRUTH: Dict[str, List[str]] = {
    # Add your resumes and their actual skills here:
}
# ---------------------------------------------------------

# Default directory for benchmark resumes
RESUME_DIR = os.path.join(os.path.dirname(__file__), "test_resumes")


def clean_source_tag(skill_with_tag: str) -> str:
    """Strip source tags like '(matched_from_dictionary)', '(detected_via_nlp)', or '(detected_via_llm)' from skill string."""
    cleaned = re.sub(r'\s*\((?:matched_from_dictionary|detected_via_nlp|detected_via_llm)\)$', '', skill_with_tag, flags=re.IGNORECASE)
    return cleaned.strip()


def calculate_metrics(extracted: Set[str], ground_truth: Set[str]) -> Tuple[float, float, float]:
    """
    Calculate Precision, Recall, and F1-Score (case-insensitive).
    """
    ext_lower = {s.lower() for s in extracted}
    gt_lower = {s.lower() for s in ground_truth}

    if not gt_lower:
        # Avoid division by zero if ground truth is empty
        return 0.0, 0.0, 0.0

    true_positives = len(ext_lower.intersection(gt_lower))
    
    precision = true_positives / len(ext_lower) if len(ext_lower) > 0 else 0.0
    recall = true_positives / len(gt_lower)
    
    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    return precision * 100, recall * 100, f1 * 100


def main():
    # Ensure the resumes directory exists
    if not os.path.exists(RESUME_DIR):
        os.makedirs(RESUME_DIR)
        print(f"Created directory: {RESUME_DIR}")
        print("Please place your 15-20 PDF/DOCX resumes inside this folder.")
        print("Then, fill in the GROUND_TRUTH dictionary at the top of this script and run it again.")
        return

    # Find resumes in the folder
    resume_files = [f for f in os.listdir(RESUME_DIR) if f.lower().endswith(('.pdf', '.docx', '.doc'))]

    if not resume_files:
        print(f"No resume files (.pdf, .docx, .doc) found in: {RESUME_DIR}")
        print("Please place your resumes in the folder and run again.")
        return

    # Check if ground truth is empty
    if not GROUND_TRUTH:
        print("The GROUND_TRUTH dictionary is currently empty.")
        print(f"Found {len(resume_files)} resume files in '{RESUME_DIR}':")
        for f in resume_files:
            print(f"  - {f}")
        print("\nPlease configure the GROUND_TRUTH mapping at the top of this script first.")
        return

    print("=" * 100)
    print(f"RUNNING PARSER ACCURACY BENCHMARK ON {len(resume_files)} RESUMES")
    print("=" * 100)
    
    # Table header
    header_fmt = "{:<30} | {:<12} | {:<12} | {:<10} | {:<10} | {:<10}"
    row_fmt = "{:<30} | {:<12} | {:<12} | {:<9.1f}% | {:<9.1f}% | {:<9.1f}%"
    
    print(header_fmt.format("Resume Filename", "GT Skills", "Ext Skills", "Precision", "Recall", "F1 Score"))
    print("-" * 100)

    total_precision = 0.0
    total_recall = 0.0
    total_f1 = 0.0
    evaluated_count = 0

    for filename in resume_files:
        file_path = os.path.join(RESUME_DIR, filename)
        
        # Check if we have ground truth for this file
        if filename not in GROUND_TRUTH:
            print(f"{filename:<30} | [No Ground Truth configured in script — skipping]")
            continue
            
        gt_skills = set(GROUND_TRUTH[filename])
        
        # Extract text and run parser
        try:
            text = extract_text(file_path)
            raw_extracted = extract_skills(text)
            # Strip source tags for comparison
            extracted_skills = {clean_source_tag(s) for s in raw_extracted}
        except Exception as e:
            print(f"{filename:<30} | Error running parser: {e}")
            continue

        precision, recall, f1 = calculate_metrics(extracted_skills, gt_skills)
        
        print(row_fmt.format(
            filename[:30], 
            len(gt_skills), 
            len(extracted_skills), 
            precision, 
            recall, 
            f1
        ))
        
        total_precision += precision
        total_recall += recall
        total_f1 += f1
        evaluated_count += 1

    print("-" * 100)
    if evaluated_count > 0:
        avg_precision = total_precision / evaluated_count
        avg_recall = total_recall / evaluated_count
        avg_f1 = total_f1 / evaluated_count
        
        print(row_fmt.format(
            f"AVERAGE ({evaluated_count} files)",
            "-",
            "-",
            avg_precision,
            avg_recall,
            avg_f1
        ))
    else:
        print("No files were successfully evaluated.")
    print("=" * 100)


if __name__ == "__main__":
    main()
