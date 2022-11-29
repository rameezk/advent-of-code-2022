#!/usr/bin/env bash

echo "Downloading puzzle input for day {{cookiecutter.aoc_day}}"
url="https://adventofcode.com/2022/day/{{cookiecutter.aoc_day}}/input"
session=$(cat ../.session)
curl $url -H "Cookie: session=$session" --output input.txt --silent
