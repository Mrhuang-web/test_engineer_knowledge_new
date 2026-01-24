cd /root
find . -name start.sh -type f -print0 | xargs -0 -I{} bash -c 'cd "$(dirname "{}")" && bash start.sh'