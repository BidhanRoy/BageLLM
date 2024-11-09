from typing import Tuple, List
from pathlib import Path
from typing import List, Dict
import logging
import pandas as pd
from annotator import DataAnnotator
from s3_connector import S3Connector
class AnnotationPipeline:
    def __init__(self, output_dir: str = "annotated_data"):
        print('init')
        self.annotator = DataAnnotator()
        self.connector = S3Connector()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def process_datasets(self):
        """Process eachdataset"""
        print('process_dataset')
        try:

            datasets = self.connector.list_datasets()
            for dataset in datasets:
                # Create temporary file path
                temp_path = self.output_dir / f"temp_{Path(dataset).name}"
                
                # Download dataset
                self.connector.download_dataset(dataset, str(temp_path))
                
                # Read and process the dataset
                df, text_columns = self._read_dataset(temp_path)
                
                # declare output csv
                output_csv = self.output_dir / f"annotated_{Path(dataset).name}"
                
                for index, value in df.items():
                    if isinstance(value, pd.Series):
                        for content in value:
                            if not isinstance(content, float) and not isinstance(content, int) and content is not None:
                                # print(content)
                                annotated_data = self.annotator.process_batch(content)

                                # Add new columns for annotations
                                column_name = f"{index}_annotations"
                                row_idx = df.index[df[index] == content][0]
                                
                                # Extract specific fields from annotations (modify as needed)
                                if annotated_data:
                                    # Example: Extract sentiment scores
                                    sentiments = [item.get('sentiment', 0) for item in annotated_data]
                                    df.at[row_idx, column_name] = str(sentiments)
                                    
                # check if df is in proper format
                if not df.empty:
                    # Save the complete annotated dataframe
                    self._save_results(df, output_csv, 'csv')
                
                # Cleanup
                temp_path.unlink()

                break

        except Exception as e:
            self.logger.error(f"Error processing dataset {dataset}: {e}")
            raise

    def _read_dataset(self, file_path: Path) -> Tuple[pd.DataFrame, List[str]]:
        """
        Read dataset and identify text columns.
        
        Args:
            file_path (Path): Path to the dataset file
            
        Returns:
            Tuple[pd.DataFrame, List[str]]: 
                - The loaded dataframe
                - List of column names containing text data
        """
        ext = file_path.suffix.lower()
        try:
            # Read the file based on extension
            if ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext == '.json':
                df = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            # Detect text columns
            text_columns = []
            for column in df.columns:
                # Check if column is object type (string)
                if df[column].dtype == 'object':
                    # Additional checks to confirm it's actually text
                    sample = df[column].dropna().iloc[0] if not df[column].empty else None
                    if sample and isinstance(sample, str):
                        # Check if it's a reasonably sized text (not just a category)
                        avg_length = df[column].str.len().mean()
                        if avg_length > 10:  # Adjustable threshold
                            text_columns.append(column)
            
            if not text_columns:
                self.logger.warning(f"No text columns found. Available columns: {df.columns.tolist()}")
            else:
                self.logger.info(f"Detected text columns: {text_columns}")
            
            return df, text_columns
            
        except Exception as e:
            self.logger.error(f"Error reading dataset {file_path}: {e}")
            raise 

    def _save_results(self, annotated_data: List[Dict], output_path: Path, datatype: str):
        """Save annotated results"""
        print('save_results')
        df = pd.DataFrame(annotated_data)
        if datatype == 'csv': 
            df.to_csv(output_path, index=False)
        elif datatype == 'json':
            df.to_json(output_path, orient='records', lines=True) 