NAME    := ec2-hibinit-agent
VERSION := $(shell grep '^Version:' packaging/al2023/ec2-hibinit-agent.spec | awk '{print $$2}')
SDIST   := ec2_hibinit_agent-$(VERSION).tar.gz
PYTHON  ?= python3

.PHONY: help sources rpm-al2 rpm-al2023 rpm-rhel rpm-sles clean

help: ## Show available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

sources: clean ## Create source tarball
	$(PYTHON) setup.py sdist --formats=gztar
	mv dist/$(SDIST) .
	rm -rf dist ec2_hibinit_agent.egg-info

rpm-al2: sources ## Build RPM for Amazon Linux 2
	$(call rpmbuild,packaging/al2/ec2-hibinit-agent.spec)

rpm-al2023: sources ## Build RPM for Amazon Linux 2023
	$(call rpmbuild,packaging/al2023/ec2-hibinit-agent.spec)

rpm-rhel: sources ## Build RPM for RHEL
	$(call rpmbuild,packaging/rhel/ec2-hibinit-agent.spec)

rpm-sles: sources ## Build RPM for SUSE Linux
	$(call rpmbuild,packaging/sles/ec2-hibernate-linux-agent.spec)

clean: ## Remove build artifacts
	rm -f *.tar.gz *.rpm
	rm -rf dist ec2_hibinit_agent.egg-info

define rpmbuild
	$(eval BUILDROOT := $(shell mktemp -d))
	mkdir -p $(BUILDROOT)/{SOURCES,SPECS}
	cp $(SDIST) $(BUILDROOT)/SOURCES/
	cp $(1) $(BUILDROOT)/SPECS/
	rpmbuild -bb --target=noarch --define '_topdir $(BUILDROOT)' $(BUILDROOT)/SPECS/$(notdir $(1))
	cp $(BUILDROOT)/RPMS/noarch/*.rpm .
	rm -rf $(BUILDROOT)
	@echo "Built: $$(ls *.rpm)"
endef
