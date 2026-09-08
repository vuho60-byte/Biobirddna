#!/usr/bin/env bash
# Kiểm tài nguyên trước bước nặng: đĩa D:, RAM máy, RAM VM Docker, dung lượng data/. Dừng nếu D: trống < MIN_FREE_GB.
MIN_FREE_GB=${MIN_FREE_GB:-50}
free_gb=$(df -BG "D:/" 2>/dev/null | awk 'NR==2{gsub("G","",$4); print $4}')
echo "D: free ${free_gb} GB (ngưỡng dừng ${MIN_FREE_GB} GB)"
echo "data/: $(du -sh "D:/BIRDBIODNA project/data" 2>/dev/null | cut -f1)"
docker_info="$(docker info --format 'CPUs={{.NCPU}} MemTotal={{.MemTotal}}' 2>/dev/null)"
echo "Docker VM: ${docker_info:-KHONG KET NOI}"
case "$docker_info" in
  ""|*"CPUs=0"*) echo "STOP: Docker khong chay (mo Docker Desktop roi chay lai)"; exit 3 ;;
esac
docker stats --no-stream --format 'container {{.Name}} mem {{.MemUsage}} cpu {{.CPUPerc}}' 2>/dev/null | head -5
[ -n "$free_gb" ] && [ "$free_gb" -lt "$MIN_FREE_GB" ] && { echo "STOP: đĩa dưới ngưỡng"; exit 2; }
exit 0
