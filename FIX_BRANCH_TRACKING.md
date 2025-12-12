# Fix Branch Tracking Issue

## Problem
Git doesn't know which remote branch to pull from.

## Solution: Set Up Branch Tracking

Run this command in PythonAnywhere Bash:

```bash
git branch --set-upstream-to=origin/main main
```

Or use the shorter version:
```bash
git branch -u origin/main
```

Then verify:
```bash
git branch -vv
```

Should show `main` with `[origin/main]` next to it.

## After Setting Up Tracking

Now you can use:
```bash
git pull
```

Without specifying the remote and branch.

## Alternative: Pull with Explicit Branch

If you don't want to set up tracking, you can always use:
```bash
git pull origin main
```

