The Amazon Linux hibernation agent.

The purpose of this agent is to create a setup for an instance to support hibernation feature. 
The setup is created only on supported instance types. 

This agent does several things upon startup:
1. It checks for sufficient swap space to allow hibernation and fails if not enough space
2. If there's no swap file or the existing swap file isn't of a sufficient size, a swap file is created
     1. If `touch-swap` is enabled, all the swap file's blocks will be touched
        so that the root EBS volume is pre-warmed.
3. It updates the offset of the swap file in the kernel using `snapshot_set_swap_area` ioctl.
4. It updates the resume offset and resume device in grub file.

## Building in Red hat

1- Install Development Tools in Red Hat to build the RPM package
```
sudo dnf group install "Development Tools"
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
```
2- Install required build packages for ec2-hibernate-linux-agent.

```
sudo yum install python3-devel
sudo yum install selinux-policy-devel
```

3- Download the package from github repository. You can replace `1.0.3` with any release version number.

```
echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros
wget https://github.com/aws/amazon-ec2-hibinit-agent/archive/v1.0.3/ec2-hibinit-agent-1.0.3.tar.gz
tar -xf ec2-hibinit-agent-1.0.3.tar.gz 
```

4- Copy spec file to SPEC directory.

```
cd ~/rpmbuild//SPECS
cp ~/rpmbuild/SOURCES/amazon-ec2-hibinit-agent-1.0.3/packaging/rhel/ec2-hibinit-agent.spec ~/rpmbuild/SPECS/

```
5- Build the Spec file 

```
nohup rpmbuild -bb --target=noarch ec2-hibinit-agent.spec
```
You will find the RPM package generated at `~/rpmbuild/RPMS/noarch/` directory



## Building in SUSE Linux 

1- Install Development Tools in Suse Linux to build the RPM package
```
sudo zypper install rpm-build
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
```
2- Install required build packages for ec2-hibernate-linux-agent.

```
sudo zypper install python3-devel
sudo zypper install tuned
sudo zypper install python-rpm-generators
```

3- Download the package from github repository. You can replace `1.0.3` with any release version number.

```
echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros
cd ~/rpmbuild/SOURCES
wget https://github.com/aws/amazon-ec2-hibinit-agent/archive/v1.0.3/ec2-hibinit-agent-1.0.3.tar.gz
tar -xf ec2-hibinit-agent-1.0.3.tar.gz 
```

4- Copy spec file to SPEC directory. You can replace `1.0.3` with any release version number.

```
cd ~/rpmbuild//SPECS
cp ~/rpmbuild/SOURCES/amazon-ec2-hibinit-agent-1.0.3/packaging/sles/ec2-hibinit-agent.spec ~/rpmbuild/SPECS/

```
5- Build the Spec file 

```
nohup rpmbuild -bb --target=noarch ec2-hibernate-linux-agent.spec
```
You will find the RPM package generated at `~/rpmbuild/RPMS/noarch/` directory

