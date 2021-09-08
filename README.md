# Container Stats Collector

A tiny, quick-n-dirty Python program which can connect to a Docker host and collect data from the stats API for specific containers.

## Usage

Configure the following environment variables (by modifying the compose file):

* `DOCKER_HOST`: The address of the Docker host, `host.docker.internal` for the own host.
* `CONTAINER_NAMES`: The names of the containers for which stats will be collected, comma-separated list.
* `READ_INTERVAL`: The Docker stats API emits one JSON stats info object per container per second. Specifying the interval determines how many of these objects are saved by the application. An interval of 5 would result in every fifth stats object being saved.

Be aware that the Docker engine HTTP API on the target host must be enabled and available on the default port `2375` for this application to work.

The stats of the monitored containers are saved to a JSON file in the named volume specified in the compose file. Each container will have their own file. Be aware that the files are usually *broken*; they end with a trailing comma and miss a closing bracket. For fixing the file, you might have to replace this comma with a closing square bracket.
