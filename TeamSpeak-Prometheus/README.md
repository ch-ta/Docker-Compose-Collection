1. Open the terminal or command prompt.

2. Navigate to the directory where your Dockerfile is located using the cd command. This directory is known as the build context.

```bash
cd path/to/teamspeak-prometheus
```

3. Build the image using the docker build command:

```bash
docker build -t teamspeak-prometheus:latest .
```
   - -t (tag) flag names and optionally tags the image in a human-readable format (e.g., my-application:1.0). If you don't provide a tag, Docker uses latest by default.
   - The single dot (.) at the end specifies that the current directory is the build context, where Docker will look for the Dockerfile and other necessary files.

4. Verify the image was created successfully by listing the local Docker images:

```bash
docker images
```

You should see the newly created image listed in the output.

**OR**

Run `ts-prometheus-build.py`
