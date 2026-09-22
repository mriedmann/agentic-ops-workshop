#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
render_dir="$project_dir/.rendered"
target_dir="$project_dir/media"

mkdir -p "$render_dir" "$target_dir"
cd "$project_dir"

uv run manim -qm --format=mp4 --media_dir "$render_dir" animations.py \
  TokenPipeline AttentionOps NextToken AgentLoop TrustBoundary

source_dir="$render_dir/videos/animations/720p30"
cp "$source_dir/TokenPipeline.mp4" "$target_dir/token-pipeline.mp4"
cp "$source_dir/AttentionOps.mp4" "$target_dir/attention-ops.mp4"
cp "$source_dir/NextToken.mp4" "$target_dir/next-token.mp4"
cp "$source_dir/AgentLoop.mp4" "$target_dir/agent-loop.mp4"
cp "$source_dir/TrustBoundary.mp4" "$target_dir/trust-boundary.mp4"

# Step timestamps (media/*.steps.json) are written by animations.py itself.
echo "Rendered videos are available in $target_dir"
