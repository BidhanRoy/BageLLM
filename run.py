import os
from dotenv import load_dotenv
from src.pipeline.main import AnnotationPipeline
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting annotation pipeline")
        
        # Initialize and run pipeline
        pipeline = AnnotationPipeline(output_dir="data/processed")
        pipeline.run_pipeline()
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main() 