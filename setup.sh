#!/bin/bash

echo "먼저 conda 가상환경을 실행시킨 후, conda install python==3.11 한 다음 아래를 sudo로 실행해주세요"

# 스크립트 실행에 필요한 최소 권한 확인
if [[ $EUID -ne 0 ]]; then
   echo "이 스크립트는 root 권한으로 실행되어야 합니다. sudo를 사용해 주세요."
   exit 1
fi

# 시스템 패키지 업데이트 및 필요한 패키지 설치
echo "시스템 패키지를 업데이트하고 필요한 패키지를 설치합니다..."
sudo apt-get update
sudo apt-get install -y pkg-config libmysqlclient-dev gcc build-essential

echo "pip install -r requirements.txt 를 입력해주세요"