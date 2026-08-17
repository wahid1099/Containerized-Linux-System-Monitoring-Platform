Short Questions

What is the difference between a Docker image and a container?
Ans: A Docker image is a static, read-only template that contains everything needed to run an application, including the application files, binaries, libraries, and configuration. A Docker container is the running instance of that image. When a container runs, it gets a writable layer on top of the read-only image layers, so changes made inside the container are writable but are usually lost when the container is removed unless the data is stored in a volume.

What does 9090:80 mean?
Ans: 9090:80 means port 9090 on the host is mapped to port 80 inside the container. 9090 is the host port and 80 is the container port. So when a user accesses the server on port 9090 Docker forwards the request to port 80 of the container.

Why do containers need a Docker network?
ans:We need a Docker network to connect multiple containers and allow them to communicate with each other. In this project the Dashboard container communicates with the Metrics Collector container through the Docker network using the service name collector .

Why do we use Docker volumes?
ans: We use Docker volumes to persist data even if a container is deleted or recreated. For example, if a container stores logs or application data, the data would normally be lost when the container is removed. Docker volumes solve this problem by storing the data outside the container's writable layer.

What problem does Docker Compose solve?
ans:Docker Compose solves the problem of manually managing multiple containers, networks, volumes, ports, and configurations separately. It allows us to define the whole application in a single compose.yaml file and manage all the services together with simple commands like docker compose up -d and docker compose down.

Add a restart policy to the services and explain what it does.
Ans:The restart policy automatically restarts a container if it crashes or if the Docker service/server restarts. However, if I manually stop the container, Docker will keep it stopped until I start it again.



                Workflow

                
                Linux Server
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
        CPU         RAM         Disk
          │           │           │
          └───────────┼───────────┘
                      ↓
             Metrics Collector
                 Flask :6000
                      │
                /api/metrics
                      ↓
                  NGINX
                      ↓
               Web Dashboard
                      │
             ┌────────┼────────┐
             ↓        ↓        ↓
            CPU      RAM      Disk
            32%      61%      45%