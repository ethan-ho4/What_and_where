import argparse
import uvicorn

# This is necessary for Windows to avoid the multiprocessing issue.
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Start the Grounding DINO FastAPI Server")
    parser.add_argument("--cpu-only", action="store_true", help="Run model on CPU only.")
    args = parser.parse_args()

    # Set the CPU_ONLY variable in the main server script
    import main
    main.CPU_ONLY = args.cpu_only

    # Start the FastAPI server
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
