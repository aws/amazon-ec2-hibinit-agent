# Amazon EC2 Hibernation Agent

Sets up hibernation support for EC2 instances on supported instance types. On startup, the agent ensures a properly sized swap file exists and configures the kernel and bootloader for hibernation resume. On receiving an ACPI sleep event, the agent enables swap and initiates hibernation. On resume, the agent disables the swap file.

## Configuration

The agent is configured via [etc/hibinit-config.cfg](etc/hibinit-config.cfg).

| Option | Description |
|--------|-------------|
| `log-to-syslog` | Log output to syslog |
| `grub-update` | Update GRUB config with `resume_offset` for the swap file |
| `touch-swap` | Write all swap file blocks to pre-warm the EBS volume. Auto-detected for XFS |
| `btrfs-enabled` | Set No Copy-on-Write on the swap file. Auto-detected for btrfs |
| `state-dir` | Directory for agent state files |
| `percentage-of-ram` | Target swap size as a percentage of RAM |
| `target-size-mb` | Target swap size in MB. The larger of this and `percentage-of-ram` is used |
| `mkswap` | Command to initialize the swap file |
| `swapon` | Command to enable swap |
| `swapoff` | Command to disable swap |

## Building

Install development tools and build dependencies for your distro:

<details>
<summary>Amazon Linux 2</summary>

```
sudo yum group install "Development Tools"
sudo yum install python2-devel systemd
```
</details>

<details>
<summary>Amazon Linux 2023</summary>

```
sudo yum group install "Development Tools"
sudo yum install python3-devel systemd-rpm-macros
```
</details>

<details>
<summary>Red Hat</summary>

```
sudo dnf group install "Development Tools"
sudo yum install python3-devel selinux-policy-devel
```
</details>

<details>
<summary>SUSE Linux</summary>

```
sudo zypper install rpm-build python3-devel tuned python-rpm-generators
```
</details>

Then build the RPM for your target distro:

```
make rpm-al2 PYTHON=python2   # Amazon Linux 2
make rpm-al2023               # Amazon Linux 2023
make rpm-rhel                 # Red Hat Enterprise Linux
make rpm-sles                 # SUSE Linux
```

The RPM will be placed in the project root. Run `make` with no arguments to see all available targets.

> **Note:** Amazon Linux 2 [reaches end of life on 2026-06-30](https://aws.amazon.com/amazon-linux-2/faqs/#long-term-support--o3nq58:~:text=Amazon%20Linux%202%20end%20of%20support%20date%20(End%20of%20Life%2C%20or%20EOL)%20will%20be%20on%202026%2D06%2D30.).
