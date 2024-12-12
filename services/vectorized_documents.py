from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from services.ollama_embedding import OllamaEmbeddings
from chromadb.config import Settings
import chromadb
from bs4 import BeautifulSoup
import re

def clean_text(raw_text):

    soup = BeautifulSoup(raw_text, "html.parser")
    clean_text = soup.get_text()
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text

urls = [
    "https://www.tutorialsteacher.com/python",
    "https://www.tutorialsteacher.com/python/what-is-python",
    "https://www.tutorialsteacher.com/python/where-to-use-python",
    "https://www.tutorialsteacher.com/python/python-version-history",
    "https://www.tutorialsteacher.com/python/install-python",
    "https://www.tutorialsteacher.com/python/python-shell-repl",
    "https://www.tutorialsteacher.com/python/python-idle",
    "https://www.tutorialsteacher.com/python/python-editors",
    "https://www.tutorialsteacher.com/python/python-syntax",
    "https://www.tutorialsteacher.com/python/python-keywords",
    "https://www.tutorialsteacher.com/python/python-data-types",
    "https://www.tutorialsteacher.com/python/python-numbers",
    "https://www.tutorialsteacher.com/python/python-strings",
    "https://www.tutorialsteacher.com/python/python-lists",
    "https://www.tutorialsteacher.com/python/python-tuples",
    "https://www.tutorialsteacher.com/python/python-dictionaries",
    "https://www.tutorialsteacher.com/python/python-sets",
    "https://www.tutorialsteacher.com/python/python-variables",
    "https://www.tutorialsteacher.com/python/python-operators",
    "https://www.tutorialsteacher.com/python/python-conditional-statements",
    "https://www.tutorialsteacher.com/python/python-loops",
    "https://www.tutorialsteacher.com/python/python-functions",
    "https://www.tutorialsteacher.com/python/python-arguments",
    "https://www.tutorialsteacher.com/python/python-return",
    "https://www.tutorialsteacher.com/python/python-recursion",
    "https://www.tutorialsteacher.com/python/python-exceptions",
    "https://www.tutorialsteacher.com/python/python-try-except",
    "https://www.tutorialsteacher.com/python/python-else-finally",
    "https://www.tutorialsteacher.com/python/python-assertion",
    "https://www.tutorialsteacher.com/python/python-modules",
    "https://www.tutorialsteacher.com/python/python-import",
    "https://www.tutorialsteacher.com/python/python-packages",
    "https://www.tutorialsteacher.com/python/python-classes",
    "https://www.tutorialsteacher.com/python/python-objects",
    "https://www.tutorialsteacher.com/python/python-constructors",
    "https://www.tutorialsteacher.com/python/python-inheritance",
    "https://www.tutorialsteacher.com/python/python-polymorphism",
    "https://www.tutorialsteacher.com/python/python-abstraction",
    "https://www.tutorialsteacher.com/python/python-encapsulation",
    "https://www.tutorialsteacher.com/python/python-method-overriding",
    "https://www.tutorialsteacher.com/python/python-method-overloading",
    "https://www.tutorialsteacher.com/python/python-file-handling",
    "https://www.tutorialsteacher.com/python/python-read-write",
    "https://www.tutorialsteacher.com/python/python-pickle",
    "https://www.tutorialsteacher.com/python/python-json",
    "https://www.tutorialsteacher.com/python/python-regex",
    "https://www.tutorialsteacher.com/python/python-pandas",
    "https://www.tutorialsteacher.com/python/python-numpy",
    "https://www.tutorialsteacher.com/python/python-matplotlib",
    "https://www.tutorialsteacher.com/python/python-seaborn",
    "https://www.tutorialsteacher.com/python/python-tkinter",
    "https://www.tutorialsteacher.com/python/python-sqlite",
    "https://www.tutorialsteacher.com/python/python-mysql",
    "https://www.tutorialsteacher.com/python/python-sqlalchemy",
    "https://www.tutorialsteacher.com/python/python-django",
    "https://www.tutorialsteacher.com/python/python-flask",
    "https://www.tutorialsteacher.com/python/python-threads",
    "https://www.tutorialsteacher.com/python/python-socket-programming",
    "https://www.tutorialsteacher.com/python/python-unittest",
    "https://www.tutorialsteacher.com/python/python-interactive-shell",
    "https://www.tutorialsteacher.com/python/python-module",
    "https://www.tutorialsteacher.com/python/pip-in-python",
    "https://www.tutorialsteacher.com/python/public-private-protected-modifiers",
    "https://www.tutorialsteacher.com/python/main-in-python",
    "https://www.tutorialsteacher.com/python/python-tuple",
    "https://www.tutorialsteacher.com/python/create-gui-using-tkinter-python",
    "https://www.tutorialsteacher.com/python/input-function",
    "https://www.tutorialsteacher.com/python/classmethod-decorator",
    "https://www.tutorialsteacher.com/python/staticmethod-decorator",
    "https://www.tutorialsteacher.com/python/math-module",
    "https://www.tutorialsteacher.com/python/type-method",
    "https://www.tutorialsteacher.com/python/os-module",
    "https://www.tutorialsteacher.com/python/python-number-type#int",
    "https://www.tutorialsteacher.com/python/python-while-loop",
    "https://www.tutorialsteacher.com/python/python-for-loop",
    "https://www.tutorialsteacher.com/python/python-lambda-function",
    "https://www.tutorialsteacher.com/python/python-operators#arithmetic",
    "https://www.tutorialsteacher.com/python/python-list-comprehension",
    "https://www.tutorialsteacher.com/python/magic-methods-in-python",
    "https://www.tutorialsteacher.com/python/python-set",
    "https://www.tutorialsteacher.com/python/python-continue",
    "https://www.tutorialsteacher.com/python/python-operators#assignment",
    "https://www.tutorialsteacher.com/python/python-ides",
    "https://www.tutorialsteacher.com/python/python-else-loop",
    "https://www.tutorialsteacher.com/python/error-types-in-python",
    "https://www.tutorialsteacher.com/python/python-break",
    "https://www.tutorialsteacher.com/python/python-operators#identity",
    "https://www.tutorialsteacher.com/python/collections-module",
    "https://www.tutorialsteacher.com/python/python-variables",
    "https://www.tutorialsteacher.com/python/python-number-type",
    "https://www.tutorialsteacher.com/python/python-if-elif",
    "https://www.tutorialsteacher.com/python/python-idle",
    "https://www.tutorialsteacher.com/python/python-number-type#float",
    "https://www.tutorialsteacher.com/python/python-pass",
    "https://www.tutorialsteacher.com/python/python-operators#membership-test",
    "https://www.tutorialsteacher.com/python/inheritance-in-python",
    "https://www.tutorialsteacher.com/python/python-class",
    "https://www.tutorialsteacher.com/python/decorators",
    "https://www.tutorialsteacher.com/python/regex-in-python",
    "https://www.tutorialsteacher.com/python/python-package",
    "https://www.tutorialsteacher.com/python/python-builtin-modules",
    "https://www.tutorialsteacher.com/python/python-number-type#complex",
    "https://www.tutorialsteacher.com/python/sys-module",
    "https://www.tutorialsteacher.com/python/recursion-in-python",
    "https://www.tutorialsteacher.com/python/python-assert",
    "https://www.tutorialsteacher.com/python/database-crud-operation-in-python",
    "https://www.tutorialsteacher.com/python/python-overview",
    "https://www.tutorialsteacher.com/python/random-module",
    "https://www.tutorialsteacher.com/python/python-course",
    "https://www.tutorialsteacher.com/python/print-function",
    "https://www.tutorialsteacher.com/python/python-operators#logical",
    "https://www.tutorialsteacher.com/python/python-list",
    "https://www.tutorialsteacher.com/python/exception-handling-in-python",
    "https://www.tutorialsteacher.com/python/python-dictionary",
    "https://www.tutorialsteacher.com/python/python-generator",
    "https://www.tutorialsteacher.com/python/python-operators#bitwise",
    "https://www.tutorialsteacher.com/python/local-and-global-variables-in-python",
    "https://www.tutorialsteacher.com/python/python-user-defined-function",
    "https://www.tutorialsteacher.com/python/property-decorator",
    "https://www.tutorialsteacher.com/python/python-read-write-file",
    "https://www.tutorialsteacher.com/python/statistics-module",
    "https://www.tutorialsteacher.com/python/python-string",
    "https://www.tutorialsteacher.com/python/python-operators#comparison",
    "https://www.tutorialsteacher.com/python/python-data-types",
    "https://www.tutorialsteacher.com/python/python-module-attributes",
]



persist_directory = "vector_db_dir"
settings = Settings(
    chroma_db_impl="duckdb+parquet",  
    persist_directory=persist_directory  
)  
collection_name = "my_collection"
vectordb = None  

try:

    client = chromadb.PersistentClient(path=persist_directory)

    existing_collections = client.list_collections()
    if collection_name in [col.name for col in existing_collections]:
        print(f"Collection '{collection_name}' already exists. Skipping embedding process.")
        collection = client.get_collection(collection_name)
    else:
        loader = WebBaseLoader(web_paths=urls)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)

        data = loader.load()
        if data:
            # data chunking
            for doc in data:
                doc.page_content = clean_text(doc.page_content)

            text_chunks = text_splitter.split_documents(data)
            collection = client.get_or_create_collection(name=collection_name)

            print(f"Collection '{collection.name}' is ready.")

            # embed and add data to the collection
            embeddings = OllamaEmbeddings()
            vectordb = Chroma(
                collection_name=collection.name,
                embedding_function=embeddings,
                client=client
            )
            vectordb.add_documents(text_chunks)

            print(f"Documents successfully added to collection '{collection.name}'.")
        else:
            print("No data loaded.")

    if vectordb is None:  
        vectordb = Chroma(
            collection_name=collection_name,
            embedding_function=OllamaEmbeddings(),
            client=client
        )


    
except Exception as e:
    print(f"An error occurred: {e}")
