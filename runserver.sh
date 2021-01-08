#!/bin/bash
gunicorn server:app -w 2 -b 0.0.0.0:8000