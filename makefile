.PHONY: setup requirements system-update install-packages

setup: system-update install-packages requirements

system-update:
	@echo "시스템 패키지를 업데이트합니다..."
	sudo apt-get update

install-packages:
	@echo "필요한 패키지를 설치합니다..."
	sudo apt-get install -y pkg-config libmysqlclient-dev gcc build-essential

requirements:
	@echo "Python 패키지를 설치합니다..."
	pip install -r requirements.txt
