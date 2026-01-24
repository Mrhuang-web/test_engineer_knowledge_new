cat > install_packages.sh << 'EOF'
#!/bin/bash
set -e  # 出错即停止

pip install lxml-5.2.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip install tornado-6.4-cp38-abi3-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip install typing_extensions-4.11.0-py3-none-any.whl
pip install greenlet-3.0.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux2014_x86_64.whl
pip install --no-index --find-links=. SQLAlchemy
pip install PyMySQL-1.1.0-py3-none-any.whl
pip install charset_normalizer-3.3.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip install idna-3.7-py3-none-any.whl
pip install urllib3-2.2.1-py3-none-any.whl
pip install certifi-2024.2.2-py3-none-any.whl
pip install --no-index --find-links=. requests
EOF