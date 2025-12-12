# Fix Update Script Permissions

## Problem
`bash: ./update.sh: Permission denied`

This means the script doesn't have execute permissions.

## Solution

Run this command in PythonAnywhere Bash:

```bash
chmod +x ~/embroidery_service_webapp/update.sh
```

Or from the project directory:

```bash
cd ~/embroidery_service_webapp
chmod +x update.sh
```

## Verify It Worked

Check permissions:

```bash
ls -la ~/embroidery_service_webapp/update.sh
```

Should show `-rwxr-xr-x` (the `x` means executable).

## Then Run It

```bash
~/embroidery_service_webapp/update.sh
```

Or:

```bash
cd ~/embroidery_service_webapp
./update.sh
```

## Alternative: Run with Bash Explicitly

If permissions still don't work, you can always run:

```bash
bash ~/embroidery_service_webapp/update.sh
```

This doesn't require execute permissions.


