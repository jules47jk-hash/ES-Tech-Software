# Fix PowerShell Execution Policy

## Problem
PowerShell scripts are blocked by Windows security policy.

## Solution Options

### Option 1: Use the Batch File (Easiest)

I've created `push_to_github.bat` that bypasses the policy. Just run:

```cmd
push_to_github.bat
```

Or double-click `push_to_github.bat` in File Explorer.

---

### Option 2: Bypass for This Script Only

Run PowerShell with bypass:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\push_to_github.ps1
```

---

### Option 3: Change Execution Policy (Current User)

Allow scripts for your user only (safer):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then you can run:
```powershell
.\push_to_github.ps1
```

**What this does:**
- `RemoteSigned` - Allows local scripts, requires signed scripts from internet
- `CurrentUser` - Only affects your user account, not system-wide

---

### Option 4: Change Execution Policy (Temporary)

For current PowerShell session only:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\push_to_github.ps1
```

This only affects the current PowerShell window.

---

## Recommendation

**Use Option 1 (Batch file)** - It's the easiest and doesn't require changing system settings.

Just run: `push_to_github.bat`

