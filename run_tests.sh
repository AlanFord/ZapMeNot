for version in 3.11 3.12 3.13 3.14; do
    echo "=== Python $version ==="
    uv run --python $version --with pandas --with pytest pytest -m basic
    # uv run --python $version --with pandas pytest -m graphics
done
