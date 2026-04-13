import os
import sys
from core import clean, process_resume


def run(resumes_dir: str, jd: str):
    jd_clean = clean(jd)
    files = [f for f in os.listdir(resumes_dir) if f.endswith(".pdf")]

    if not files:
        print("No PDF files found in:", resumes_dir)
        return

    results = [
        process_resume(os.path.join(resumes_dir, f), jd_clean, f)
        for f in files
    ]

    results.sort(key=lambda r: r.score, reverse=True)

    print("\n" + "=" * 50)
    print("RESUME SCREENING RESULTS")
    print("=" * 50)

    for r in results:
        if r.error:
            print(f"\n[ERROR] {r.filename}: {r.error}")
            continue
        print(f"\nCandidate : {r.filename}")
        print(f"Score     : {r.score}%")
        print(f"Skills    : {', '.join(r.matched_skills) if r.matched_skills else 'None matched'}")
        print("-" * 50)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <resumes_folder>")
        print("Paste job description below (Ctrl+D to submit):\n")
        jd = sys.stdin.read()
        resumes_dir = "resumes"
    else:
        resumes_dir = sys.argv[1]
        print("Paste job description (Ctrl+D to submit):\n")
        jd = sys.stdin.read()

    run(resumes_dir, jd)
