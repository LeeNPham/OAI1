# Build & Deploy:

* ```
    pip install -r requirements.txt
    uvicorn main:app --reload

    #deploy
    pip install -r requirements.txt
    uvicorn main:app --host 0.0.0.0 --port 10000
    ```

# Reminders:
look into bringing fetch calls into server.ts and class typing various models
