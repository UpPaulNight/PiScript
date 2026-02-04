# Pi Scripts

This repository contains scripts and service files to let the Raspberry Pi
interact with the TV in a way that is at least somewhat graceful. It can turn
the TV on and off at scheduled times, it can correct the resolution of the
device, and it can restart the Pi if necessary.

It also contains something to set up a VS Code Tunnel. It's here because idk
where else to put it.

## Installation

The simplest installation method is to run the install.sh script. This will set
up the environment, install the required packages, and set up the service files.

Before running it, follow the [prerequisite steps](INSTALL.md#prerequisites).
Then run

```bash
bash install.sh
```

If after you want to set up the VS Code tunnel follow the [VS Code Tunnels
section](INSTALL.md#vs-code-tunnels) in the installation instructions.

### For detailed installation instructions

See the [INSTALL.md](INSTALL.md) file for detailed installation instructions.

## Scope Definition

The scope of this project is defined by the **service files** and the
**packages** needed by this project.

If the scope of this project changes, that constitutes a *major* change. Any
change that does not change that scope is considered a *minor* or *patch*
change.

Note that if the list of packages shrinks, then it does not need to be a major
change.

The reason for this decision is that any change in the packages or service files
will require a redeployment to all devices, which is a significant effort. Any
non-major changes can just be pulled.
