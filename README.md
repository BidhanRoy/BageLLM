CleanBagel 🥯
An automated data preparation pipeline optimized for Llama 3.2 fine-tuning. CleanBagel streamlines the process of cleaning and annotating multi-modal datasets with a focus on quality and efficiency.
🚀 Features

Automated Cleaning Pipeline: Optimized for Llama 3.2 (1B, 3B, 11B, 90B)
Multi-Modal Support: Handles both text and image data
Quality Metrics Dashboard: Real-time insights into data quality
Smart Annotation: Automated annotation suggestions with human-in-the-loop capability
Comprehensive Quality Checks:

Completeness
Consistency
Validity
Timeliness
Syntactical cleaning
Uniqueness detection



🛠️ Tech Stack

Python with Flask/FastAPI
AWS Infrastructure:

EC2 with NVIDIA drivers
S3 for storage
DynamoDB/Postgres for metadata


Gradio for UI

📦 Installation
bashCopy# Clone the repository
git clone https://github.com/your-org/cleanbagel
cd cleanbagel

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify GPU setup
python -c "import torch; print(torch.cuda.is_available())"
⚡ Quick Start
pythonCopyfrom cleanbagel import DataProcessor

# Initialize processor
processor = DataProcessor(config_path='config.yaml')

# Process dataset
cleaned_data = processor.process_dataset('input_file.csv')
🔧 Configuration
Create a config.yaml file:
yamlCopymodel:
  name: "meta-llama/Llama-3.2-1B"
  max_length: 512
  batch_size: 32

processing:
  min_text_length: 20
  max_text_length: 1000
  quality_threshold: 0.8

monitoring:
  log_level: INFO
  metrics_interval: 60
🐋 Docker Deployment
bashCopy# Build image
docker build -t cleanbagel:latest .

# Run container
docker run -d -p 7860:7860 --gpus all cleanbagel:latest
📊 Metrics & Monitoring
CleanBagel provides real-time insights into:

Processing speed (samples/minute)
Cleaning accuracy
Annotation quality
Resource utilization
Data quality metrics

🤝 Contributing
We welcome contributions! Please check our Contributing Guidelines for details.
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙋‍♂️ Support

Documentation: docs/
Issues: GitHub Issues
Questions: GitHub Discussions

🏆 Acknowledgments
Built during the Llama 3.2 Hackathon 2024. Special thanks to all contributors and mentors!