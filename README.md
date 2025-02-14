# NYC Taxi Stats

This project computes a set of statistics from the publicly available dataset of New York taxis trips. The statistics include:
- The average price per mile traveled by the customers of taxis.
- The distribution of payment types (how many trips are paid with each type of payment).
- A custom indicator: (amount of tip + extra payment) / trip distance.

## Project Structure

- **main.py**: Entry point of the application.
- **data_loader.py**: Functions for loading and processing the CSV data.
- **metrics.py**: Functions to compute the required metrics.
- **utils.py**: Utility functions for various tasks.
- **config.py**: Configuration settings and constants.

- **data/**: Contains raw data files.
  - **raw/**: Directory for raw CSV data.
    - **sample_data.csv**: Sample dataset of yellow taxi trips.

- **output/**: Directory for output files.
  - **20210101_yellow_taxi_kpis.json**: Output JSON file for computed metrics.

- **requirements.txt**: Lists the dependencies required for the project.

- **Dockerfile**: Instructions to build a Docker image for the application.

- **docker-compose.yml**: Configuration for Docker Compose.

- **tests/**: Directory for test files.
  - **test_main.py**: Test file for the main application.

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerization)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/nyc-taxi-stats.git
   cd nyc-taxi-stats
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) Build and run the Docker container:
   ```
   docker build -t nyc-taxi-stats .
   docker run nyc-taxi-stats
   ```

## Usage

Run the application by executing the following command:
```
python src/main.py
```

## Metrics Computed

- **Average Price per Mile**: The average cost incurred by customers for each mile traveled.
- **Payment Type Distribution**: A breakdown of how many trips were paid using each payment method.
- **Custom Indicator**: Calculated as (amount of tip + extra payment) / trip distance, providing insight into customer tipping behavior relative to distance traveled.

## License

This project is licensed under the MIT License.

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install build-essential package
RUN apt-get update && apt-get install -y build-essential

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "src/main.py", "--date", "2024-12-01"]