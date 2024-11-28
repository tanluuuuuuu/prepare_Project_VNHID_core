# RUN SERVER

```console
curl -fsSL https://elastic.co/start-local | sh
```
OR
```console
bash server_start-local/start-local.sh
```
This will run a Elasticsearch cluster, together with Kibana to use the Dev Tools API Console. The output will look like this

![Description of the image](imgs/Screenshot%20from%202024-11-28%2010-25-14.png)


# Installation

```console
poetry install --no-root
poetry shell # Activate env
```

# Notes
File [docker-compose.yml](/elastic-stack/docker-compose.yml)
```console
environment:
  - discovery.type=single-node
  - bootstrap.memory_lock=true
  - xpack.security.enabled=false
  - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
```
1. discovery.type=single-node:
   - This setting tells Elasticsearch to run in single-node discovery mode.
   - It's used when you're running a single-node cluster, which is typical for development or testing environments.
   - In this mode, the node will form a single-node cluster on its own without attempting to discover other nodes.

2. bootstrap.memory_lock=true:
   - This setting enables memory locking for the Elasticsearch process.
   - When set to true, it prevents the operating system from swapping the Elasticsearch memory to disk.
   - This can improve performance by ensuring that the Elasticsearch heap stays in physical memory.

3. xpack.security.enabled=false:
   - This disables the X-Pack security features in Elasticsearch.
   - X-Pack is a pack of additional features for Elasticsearch, including security, monitoring, reporting, and more.
   - By setting this to false, you're running Elasticsearch without security features, which is not recommended for production environments but can be convenient for development or testing.

4. ES_JAVA_OPTS=-Xms512m -Xmx512m:
   - This sets Java options for the Elasticsearch JVM.
   - -Xms512m sets the initial heap size to 512 megabytes.
   - -Xmx512m sets the maximum heap size to 512 megabytes.
   - By setting both to the same value, you're telling the JVM to allocate all the memory upfront, which can help with performance.

```console
ulimits:
    memlock:
    soft: -1
    hard: -1
```   
This sets the ulimits for the container. It removes the memory lock limit, which is recommended when bootstrap.memory_lock=true is set.

```console 
volumes:
  elasticsearch_data:
    driver: local
```
This creates a named volume elasticsearch_data using the local driver, which is used by the Elasticsearch service for data persistence.
