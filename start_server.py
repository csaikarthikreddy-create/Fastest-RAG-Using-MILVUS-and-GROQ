from beam import Image, Pod
import sys
import time

streamlit_server = Pod(
    image=Image().add_python_packages([
        "streamlit",
        "pymilvus[milvus_lite]",
        "milvus-lite",  # Explicitly include milvus-lite to ensure it's available
        "llama-index",
        "llama-index-embeddings-huggingface",
        "llama-index-llms-groq"
    ]),
    ports=[8501],  # Default port for streamlit
    # cpu=4,
    gpu="A10G",
    memory="2Gi",
)

print("Creating Streamlit server pod...")
res = streamlit_server.create(entrypoint=["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"])

# Wait a moment for the pod to initialize
print("Waiting for pod to be ready...")
time.sleep(2)

# Get the URL
if hasattr(res, 'url') and res.url:
    print(f"\n✨ Streamlit server hosted at: {res.url}")
elif hasattr(res, 'container_id'):
    print(f"\n✅ Pod created with container ID: {res.container_id}")
    print("⚠️  URL not immediately available. The pod may still be starting.")
    print("   Check the Beam dashboard or wait a few moments and check again.")
    # Try to get URL from container_id or other attributes
    print(f"\nResult object attributes: {[attr for attr in dir(res) if not attr.startswith('_')]}")
else:
    print("\n⚠️  Could not retrieve URL or container ID from result object.")
    print(f"Result object type: {type(res)}")
    print(f"Result object: {res}")