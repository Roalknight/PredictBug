#!/bin/bash

# List of repos to download
repos=(
    "https://github.com/apache/ant"
    "https://github.com/apache/camel"
    "https://github.com/apache/camel-spring-boot"
    "https://github.com/apache/xalan-java"
    "https://github.com/apache/xerces2-j"
    "https://github.com/apache/dubbo"
    "https://github.com/apache/kafka"
    "https://github.com/apache/shenyu"
    "https://github.com/apache/iceberg"
    "https://github.com/apache/hadoop"
)

# Download and ETL the repos
for repo in ${repos[@]}; do
    ./repo_to_json.py "$repo" /tmp/code_etl/
done
