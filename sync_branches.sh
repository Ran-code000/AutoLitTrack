#!/bin/bash

remote_branches=$(git branch -r | grep -vE "HEAD|main|master" | sed 's/origin\///')

for branch in $remote_branches; do
  echo "--------------------------Synchronizing branches: $branch ----------------------------"
  
  if git show-ref --quiet refs/heads/"$branch"; then
    git checkout "$branch"
    git pull origin "$branch"
  else
    git checkout -b "$branch" origin/"$branch"
  fi
done

git checkout - 