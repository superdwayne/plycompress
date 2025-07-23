# PLYCompress

PLYCompress is a web application built with Streamlit that allows users to reduce the number of vertices in a PLY file. This tool is useful for compressing 3D point cloud data while preserving essential properties.

## Features

- **File Upload**: Users can upload PLY files directly through the web interface.
- **Vertex Reduction**: Select a reduction factor to control the number of vertices retained.
- **Download**: Download the reduced PLY file after processing.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/superdwayne/plycompress.git
   cd plycompress
   ```

2. **Install Dependencies**

   Use the following command to install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Running the App Locally

To run the Streamlit app locally, execute the following command:
bash
streamlit run app.py


This will start a local server, and you can access the app in your web browser at `http://localhost:8501`.


## Usage

1. **Upload a PLY File**: Use the file uploader to select your PLY file.
2. **Select Reduction Factor**: Use the slider to choose how much to reduce the vertices (0.1 to 1.0).
3. **Download Reduced File**: After processing, download the reduced PLY file.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## API Usage

The application now includes a REST API endpoint for programmatic access.

### Starting the API
```bash
python api.py
