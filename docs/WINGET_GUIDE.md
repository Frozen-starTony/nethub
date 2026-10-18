# How to Publish NetHub to Windows Package Manager (winget)

Publishing NetHub to Microsoft's official `winget-pkgs` repository enables users to install and update NetHub with a single command in PowerShell or Windows Terminal:

```powershell
winget install Frozen-starTony.NetHub
```

---

## Method 1: Using the Official `wingetcreate` CLI (Easiest)

1. **Install `wingetcreate`:**
   ```powershell
   winget install Microsoft.WingetCreate
   ```

2. **Generate and submit in one command:**
   Run the submission command pointing to the latest release binary:
   ```powershell
   wingetcreate submit https://github.com/Frozen-starTony/nethub/releases/download/v1.0.0/NetHub.exe
   ```

3. `wingetcreate` will prompt you for your GitHub Personal Access Token (PAT) with `public_repo` permissions, automatically fork `microsoft/winget-pkgs`, commit the manifest files, and open a Pull Request!

4. Microsoft's automated CI will validate the package, test-install it in a clean Windows Sandbox, and merge the PR within 24–48 hours.

---

## Method 2: Manual Pull Request

The manifests are already pre-generated in the `winget/` directory of this repository:
- `winget/Frozen-starTony.NetHub.yaml`
- `winget/Frozen-starTony.NetHub.installer.yaml`
- `winget/Frozen-starTony.NetHub.locale.en-US.yaml`

Simply fork [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs), place these three files in `manifests/f/Frozen-starTony/NetHub/1.0.0/`, and submit a Pull Request!
