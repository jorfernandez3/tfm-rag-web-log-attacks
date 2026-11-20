#!/usr/bin/env python3
"""
Experiment runner for the four thesis configurations.
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class ExperimentRunner:
    def __init__(self, notebook_dir: str, results_dir: str):
        self.notebook_dir = Path(notebook_dir)
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.configurations = {
            'C1': 'C1_baseline_llm_only.ipynb',
            'C2': 'C2_llm_rag.ipynb',
            'C3': 'C3_llm_rag_secure_prompt.ipynb',
            'C4': 'C4_llm_rag_full_defense.ipynb',
        }
        
        self.results = {}
        self.start_time = datetime.now()
    
    def run_notebook(self, config_name: str, notebook_file: str) -> bool:
        """Run a single notebook using nbconvert"""
        notebook_path = self.notebook_dir / notebook_file
        output_file = self.results_dir / f"{config_name}_output.html"
        
        print(f"\n{'='*60}")
        print(f"Running {config_name}: {notebook_file}")
        print(f"{'='*60}")
        print(f"Output will be saved to: {output_file}")
        
        try:
            cmd = [
                sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'html',
                '--execute',
                '--ExecutePreprocessor.timeout=600',
                f'--output={output_file}',
                str(notebook_path)
            ]
            
            env = os.environ.copy()
            env['EXPERIMENT_RESULTS_DIR'] = str(self.results_dir.resolve())
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=1200, env=env
            )
            
            if result.returncode == 0:
                print(f"✓ {config_name} completed successfully")
                return True
            else:
                print(f"✗ {config_name} failed with return code {result.returncode}")
                print(f"Error output: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"✗ {config_name} timed out (>20 minutes)")
            return False
        except OSError as e:
            print(f"✗ {config_name} error: {str(e)}")
            return False
    
    def load_results(self, config_name: str) -> List[Dict[str, Any]] | None:
        """Load results from JSON output files"""
        result_file = self.results_dir / f"{config_name.lower()}_results.json"
        
        if result_file.exists():
            with open(result_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            if not isinstance(results, list):
                raise ValueError(f"Expected a list in {result_file}")
            return results
        return None
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate experiment summary"""
        summary = {
            'experiment_start': self.start_time.isoformat(),
            'experiment_end': datetime.now().isoformat(),
            'configurations': {}
        }
        
        for config_name in self.configurations:
            results = self.load_results(config_name) if self.results.get(config_name) else None

            if results is not None:
                successful = sum(1 for r in results if r.get('output_valid'))
                total = len(results)
                has_format_metrics = all(
                    isinstance(r.get('raw_output_valid'), bool)
                    and isinstance(r.get('markdown_recovered'), bool)
                    for r in results
                )
                raw_valid = sum(r['raw_output_valid'] for r in results) if has_format_metrics else None
                recovered = sum(r['markdown_recovered'] for r in results) if has_format_metrics else None
                
                summary['configurations'][config_name] = {
                    'status': 'completed',
                    'total_logs_processed': total,
                    'successful': successful,
                    'valid_output_rate': f"{(successful/total)*100:.1f}%" if total else "N/A",
                    'raw_valid_outputs': raw_valid,
                    'markdown_recovered_outputs': recovered,
                }
            else:
                summary['configurations'][config_name] = {
                    'status': 'failed',
                    'error': 'Notebook failed or results file not found'
                }
        
        return summary
    
    def run_all(self) -> bool:
        """Run all experimental configurations"""
        print(f"\n{'='*60}")
        print("TFM RAG Web Log Analysis - Experimental Runner")
        print(f"{'='*60}")
        print(f"Start time: {self.start_time}")
        print(f"Notebooks directory: {self.notebook_dir}")
        print(f"Results directory: {self.results_dir}")
        
        all_success = True
        
        for config_name, notebook_file in self.configurations.items():
            success = self.run_notebook(config_name, notebook_file)
            self.results[config_name] = success
            
            if not success:
                all_success = False
        
        print(f"\n{'='*60}")
        print("Experiment Summary")
        print(f"{'='*60}")
        
        for config_name, success in self.results.items():
            status = "✓ PASSED" if success else "✗ FAILED"
            print(f"{config_name}: {status}")
        
        # Generate and save summary
        summary = self.generate_summary()
        summary_file = self.results_dir / 'experiment_summary.json'
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nSummary saved to: {summary_file}")
        print(f"End time: {datetime.now()}")
        
        return all_success and all(
            item['status'] == 'completed'
            for item in summary['configurations'].values()
        )

def main():
    # Get paths
    notebook_dir = Path(__file__).parent
    results_dir = notebook_dir.parent / 'results'
    
    # Check environment
    try:
        import jupyter
    except ImportError:
        print("Error: Jupyter is not installed")
        print("Install with: pip install jupyter nbconvert")
        sys.exit(1)
    
    try:
        import langchain
    except ImportError:
        print("Error: LangChain is not installed")
        print("Install with: pip install langchain langchain-openai langchain-chroma")
        sys.exit(1)
    
    from dotenv import load_dotenv

    load_dotenv(notebook_dir.parent / '.env')

    # Check API key
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Run experiments
    runner = ExperimentRunner(str(notebook_dir), str(results_dir))
    success = runner.run_all()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
