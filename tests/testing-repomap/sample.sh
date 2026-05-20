#!/bin/bash
set -euo pipefail

setup_environment() {
    export APP_ENV="${APP_ENV:-production}"
    mkdir -p /var/log/app /var/run/app
}

check_dependencies() {
    local deps=("docker" "kubectl" "jq")
    for dep in "${deps[@]}"; do
        command -v "$dep" >/dev/null 2>&1 || { echo "Missing: $dep"; return 1; }
    done
}

deploy_service() {
    local name="$1"
    local image="${2:-latest}"
    echo "Deploying $name:$image"
    kubectl apply -f "manifests/$name.yaml"
}

wait_for_ready() {
    local name="$1"
    local timeout="${2:-60}"
    kubectl rollout status "deployment/$name" --timeout="${timeout}s"
}

cleanup() {
    rm -rf /tmp/build-*
    echo "Cleaned up temp files"
}

trap cleanup EXIT
