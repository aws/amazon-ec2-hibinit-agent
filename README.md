The Amazon Linux hibernation agent.

The purpose of this agent is to create a setup for an instance to support hibernation feature. 
The setup is created only on supported instance types. This agent does several things:

1. Upon startup it checks for sufficient swap space to allow hibernate and fails
   if it's present but there's not enough of it.
2. If there's no swap space, it launches a background thread to create it and touch 
   all of its blocks to make sure that EBS volumes are pre-warmed if configured.This is configurable.
3. It updates the offset of the swap file in the kernel using SNAPSHOT_SET_SWAP_AREA ioctl.
4. It updates the resume offset and resume device in grub file.
