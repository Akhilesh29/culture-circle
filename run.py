"""
Simple script to run the Outfit Recommendation API server.
"""
import uvicorn

if __name__ == "__main__":
    print("Starting Outfit Recommendation API...")
    print("API will be available at http://localhost:8000")
    print("Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

