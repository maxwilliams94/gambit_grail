#! env bash

cd `dirname -- "$0"`
cd src/gambit/gambit
uvicorn main:app

