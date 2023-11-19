#!/usr/bin/env bash

streamlit run \
	--server.address "${STREAMLIT_HOST:-0.0.0.0}" \
	--server.port "${STREAMLIT_PORT:-8080}" \
	/app/cybulde/streamlit_app.py
