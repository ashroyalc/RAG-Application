# Simple RAG (Retrieval Augmented Generation) Application (beta)

This is a simple implementation of a Retrieval Augmented Generation (RAG) application using LangChain, Chroma, and the Google Generative AI API. The application allows users to upload a PDF file, which is then processed and stored in a Chroma vector database. Users can then query the uploaded data, and the application will retrieve relevant information from the PDF and generate an answer using the Google Generative AI model.

## Prerequisites

Before running this application, make sure you have the following prerequisites installed:

- Python 3.7 or later
- Google Cloud API key with access to the Generative AI API
- Required Python packages (listed in the `requirements.txt` file)

## Installation

1. Clone the repository:
  ```git clone https://github.com/ashroyalc/RAG-Application.git ```

2. Install the required Python packages:
  ```pip install -r requirements.txt ```

4. Set the `GOOGLE_API_KEY` environment variable with your Google Cloud API key:
   ``` export GOOGLE_API_KEY=your-api-key ```
## Usage

1. Run the Streamlit application:
``` streamlit run app.py```
2. In the Streamlit UI, upload a PDF file.
3. Once the PDF is processed, enter your query in the text input field.
4. The application will retrieve relevant information from the PDF and generate an answer using the Google Generative AI model.

## Code Structure

- `app.py`: Main application file containing the Streamlit UI and the RAG pipeline implementation.
- `requirements.txt`: List of required Python packages.

## Dependencies

The application uses the following main dependencies:

- `langchain`: A framework for building applications with large language models.
- `langchain-google-genai`: LangChain integrations for the Google Generative AI API.
- `langchain-community`: Community integrations for LangChain, including the Chroma vector store.
- `streamlit`: A framework for building data-centric web applications.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
