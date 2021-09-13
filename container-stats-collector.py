from datetime import datetime
import docker
import os
import threading

def save_stats(client, container_name, save_interval):
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  filename = 'data/stats-{0}-{1}.json'.format(timestamp, container_name)
  container_stats = client.stats(container_name)
  with open(filename, 'w', buffering=1) as file:
    file.write('[')
    try:
      counter = 1
      for stat in container_stats:
        if counter % save_interval == 0:
          file.write(stat.decode('utf-8') + ',')
          counter = 0
        counter += 1
    finally:
      file.write('{{}}]')

docker_ip = os.environ['DOCKER_HOST']
if docker_ip is None:
  raise ValueError('Missing docker host address')

container_names_str = os.environ['CONTAINER_NAMES']
if container_names_str is None:
  raise ValueError('Missing container names')
container_names = container_names_str.split(',')

save_interval_value = os.environ['SAVE_INTERVAL']
if save_interval_value is None:
  raise ValueError('Missing save interval')
save_interval_int = int(save_interval_value)
if save_interval_int < 1:
  raise ValueError('Interval must be greater than zero')

client = docker.APIClient(base_url='{0}:2375'.format(docker_ip))

threads = []

for name in container_names:
  thread = threading.Thread(target = save_stats, args = (client, name, save_interval_int))
  thread.start()
  threads.append(thread)
  print("Started thread for container \"{0}\"", name)

for t in threads:
  t.join()
